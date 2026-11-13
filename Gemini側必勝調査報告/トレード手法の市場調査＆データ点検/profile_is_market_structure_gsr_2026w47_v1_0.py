import hashlib, json
from pathlib import Path
from datetime import datetime, timezone, timedelta
import numpy as np
import pandas as pd

SCRIPT_VERSION = "1.0.2"
PIPELINE_CASE_ID = "GSR-2026W47"
JST = timezone(timedelta(hours=9))

BASE_DRIVE = Path(r"G:\マイドライブ")
STAGE1_DIR = BASE_DRIVE / r"AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\トレード手法の市場調査＆データ点検"
DATA_ROOT = BASE_DRIVE / r"通貨ペア\Dukascopy 1分足"

IS_START_UTC = pd.Timestamp("2015-01-01 00:00:00")
IS_END_UTC = pd.Timestamp("2021-12-31 23:59:59")

def calc_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def find_m1_csv(symbol: str):
    """最もファイルサイズが大きい全期間M1生データを選択する"""
    sym_dir = DATA_ROOT / symbol
    if not sym_dir.exists():
        return None
    csvs = [p for p in sym_dir.glob("*.csv") if p.is_file()]
    if not csvs:
        return None
    return max(csvs, key=lambda p: p.stat().st_size)

def read_m1_flexible(csv_path: Path) -> pd.DataFrame:
    """ヘッダあり/なし、日時1列(6列)/日付+時刻2列(7列)を自動判別して高速読み込みする"""
    with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
        first_line = f.readline().strip()
    parts = [p.strip() for p in first_line.split(",")]
    has_header = any(any(k in p.lower() for k in ["open", "high", "low", "close", "time", "date"]) for p in parts)

    if has_header:
        raw_df = pd.read_csv(csv_path)
        col_map = {c.lower().strip(): c for c in raw_df.columns}
        if "date" in col_map and "time" in col_map and "gmt time" not in col_map:
            dt_str = raw_df[col_map["date"]].astype(str) + " " + raw_df[col_map["time"]].astype(str)
        else:
            t_col = col_map.get("gmt time") or col_map.get("time") or col_map.get("timestamp") or col_map.get("datetime") or list(raw_df.columns)[0]
            dt_str = raw_df[t_col].astype(str)
        df = pd.DataFrame({
            "dt_str": dt_str,
            "open": raw_df[col_map.get("open", list(raw_df.columns)[1])].astype(float),
            "high": raw_df[col_map.get("high", list(raw_df.columns)[2])].astype(float),
            "low": raw_df[col_map.get("low", list(raw_df.columns)[3])].astype(float),
            "close": raw_df[col_map.get("close", list(raw_df.columns)[4])].astype(float),
        })
    else:
        raw_df = pd.read_csv(csv_path, header=None)
        if raw_df.shape[1] >= 7 and ":" in str(raw_df.iloc[0, 1]):
            dt_str = raw_df[0].astype(str) + " " + raw_df[1].astype(str)
            o_idx, h_idx, l_idx, c_idx = 2, 3, 4, 5
        else:
            dt_str = raw_df[0].astype(str)
            o_idx, h_idx, l_idx, c_idx = 1, 2, 3, 4
        df = pd.DataFrame({
            "dt_str": dt_str,
            "open": raw_df[o_idx].astype(float),
            "high": raw_df[h_idx].astype(float),
            "low": raw_df[l_idx].astype(float),
            "close": raw_df[c_idx].astype(float),
        })
    return df

def load_and_lock_is_m1(csv_path: Path, pip_size: float):
    raw_df = read_m1_flexible(csv_path)
    total_raw_rows = len(raw_df)
    raw_df["dt_utc"] = pd.to_datetime(raw_df["dt_str"], format="mixed", dayfirst=False, utc=False)

    pre_2015_rows = int((raw_df["dt_utc"] < IS_START_UTC).sum())
    oos_2022_plus_rows = int((raw_df["dt_utc"] > IS_END_UTC).sum())

    # OOS物理遮断: IS期間(2015-2021)のみ抽出
    df = raw_df[(raw_df["dt_utc"] >= IS_START_UTC) & (raw_df["dt_utc"] <= IS_END_UTC)].copy()
    del raw_df

    df = df.sort_values("dt_utc").drop_duplicates(subset=["dt_utc"]).reset_index(drop=True)

    bad_ohlc = (df["high"] < df[["open", "close"]].max(axis=1)) | (df["low"] > df[["open", "close"]].min(axis=1))
    df["ohlc_valid"] = ~bad_ohlc

    t_now = df["dt_utc"]
    t_plus_1 = df["dt_utc"].shift(-1)
    t_plus_6 = df["dt_utc"].shift(-6)
    strict_6bar = (
        (t_plus_1 - t_now == pd.Timedelta(minutes=1))
        & (t_plus_6 - t_now == pd.Timedelta(minutes=6))
        & df["ohlc_valid"]
        & df["ohlc_valid"].shift(-1, fill_value=False)
        & df["ohlc_valid"].shift(-6, fill_value=False)
    )
    df["continuity_6bar_status"] = np.where(strict_6bar, "PASS", "GAP_OR_INVALID_T1_T6")

    df["range_pips"] = (df["high"] - df["low"]) / pip_size
    df["body_pips"] = (df["close"] - df["open"]).abs() / pip_size
    df["dir_bar"] = np.where(df["close"] > df["open"], 1, np.where(df["close"] < df["open"], -1, 0))
    df["atr14_pips"] = df["range_pips"].rolling(14, min_periods=14).mean()

    bb_mid = df["close"].rolling(20, min_periods=20).mean()
    bb_std = df["close"].rolling(20, min_periods=20).std(ddof=0)
    df["bb_zscore"] = np.where(bb_std > 0, (df["close"] - bb_mid) / bb_std, 0.0)

    m5 = (
        df.set_index("dt_utc")[["open", "high", "low", "close"]]
        .resample("5min", label="left", closed="left")
        .agg({"open": "first", "high": "max", "low": "min", "close": "last"})
        .dropna()
        .reset_index()
    )
    m5["m5_close_utc"] = m5["dt_utc"] + pd.Timedelta(minutes=5)
    m5_mid = m5["close"].rolling(20, min_periods=20).mean()
    m5_std = m5["close"].rolling(20, min_periods=20).std(ddof=0)
    m5["m5_bbw_pips"] = (4.0 * m5_std) / pip_size
    m5["m5_slope3_pips"] = (m5_mid - m5_mid.shift(3)) / pip_size
    m5["abs_m5_slope3_pips"] = m5["m5_slope3_pips"].abs()

    df["signal_utc"] = df["dt_utc"] + pd.Timedelta(minutes=1)
    df = pd.merge_asof(
        df.sort_values("signal_utc"),
        m5[["m5_close_utc", "m5_bbw_pips", "abs_m5_slope3_pips"]].sort_values("m5_close_utc"),
        left_on="signal_utc",
        right_on="m5_close_utc",
        direction="backward",
    )

    stats = {
        "csv_name": csv_path.name,
        "sha256": calc_sha256(csv_path),
        "total_raw_rows": int(total_raw_rows),
        "pre_2015_excluded": int(pre_2015_rows),
        "oos_2022_plus_blocked": int(oos_2022_plus_rows),
        "is_adopted_rows": int(len(df)),
        "ohlc_violations_in_is": int(bad_ohlc.sum()),
    }
    return df, stats

def assign_disjoint_bin(series: pd.Series, edges: list, labels: list) -> pd.Series:
    return pd.cut(series, bins=edges, labels=labels, right=True, include_lowest=True).astype(str)

def extract_candidates_for_symbol(df: pd.DataFrame, symbol: str, pip_size: float) -> pd.DataFrame:
    records = []
    dt_jst = df["signal_utc"] + pd.Timedelta(hours=9)
    df["jst_hour"] = dt_jst.dt.hour
    df["jst_min"] = dt_jst.dt.minute

    if symbol == "USDJPY":
        move_15m = (df["close"] - df["open"].shift(14)) / pip_size
        move_15m_atr = move_15m.abs() / df["atr14_pips"].replace(0, np.nan)
        upper_wick = (df["high"] - df[["open", "close"]].max(axis=1)) / (df["range_pips"].replace(0, np.nan) * pip_size)
        lower_wick = (df[["open", "close"]].min(axis=1) - df["low"]) / (df["range_pips"].replace(0, np.nan) * pip_size)

        is_0955_jst = (df["jst_hour"] == 9) & (df["jst_min"] == 55)
        cond_ctrl = is_0955_jst & (move_15m_atr >= 1.5) & df["m5_bbw_pips"].notna()
        sub = df[cond_ctrl].copy()
        if not sub.empty:
            m15_signed = move_15m.loc[sub.index]
            stall_ratio = np.where(m15_signed > 0, upper_wick.loc[sub.index], lower_wick.loc[sub.index])
            is_cand = (stall_ratio >= 0.35) | (np.sign(m15_signed) != sub["dir_bar"])
            sub["case_id"] = "GSR-TKYFIX-001"
            sub["symbol"] = symbol
            sub["cohort_role"] = np.where(is_cand, "CANDIDATE", "CONTROL_ONLY")
            sub["direction"] = np.where(m15_signed > 0, -1, 1)
            sub["bin_axis_1"] = assign_disjoint_bin(move_15m_atr.loc[sub.index], [1.5, 2.0, 2.6, 3.5, 999.0], ["B1_1.5_2.0", "B2_2.0_2.6", "B3_2.6_3.5", "B4_3.5_up"])
            sub["bin_axis_2"] = assign_disjoint_bin(sub["atr14_pips"], [0.0, 1.5, 2.5, 4.0, 999.0], ["B1_sub1.5", "B2_1.5_2.5", "B3_2.5_4.0", "B4_4.0_up"])
            sub["bin_axis_3"] = assign_disjoint_bin(pd.Series(stall_ratio, index=sub.index), [-1.0, 0.25, 0.40, 0.55, 999.0], ["B1_sub0.25", "B2_0.25_0.40", "B3_0.40_0.55", "B4_0.55_up"])
            records.append(sub)

    prev_z = df["bb_zscore"].shift(1)
    prev_high = df["high"].shift(1)
    prev_low = df["low"].shift(1)
    prev_range = df["range_pips"].shift(1).replace(0, np.nan)
    body_rev_ratio = df["body_pips"] / prev_range

    up_exhaust = (prev_z >= 2.5) & (df["high"] <= prev_high) & (df["dir_bar"] == -1)
    dn_exhaust = (prev_z <= -2.5) & (df["low"] >= prev_low) & (df["dir_bar"] == 1)
    cond_ex = (up_exhaust | dn_exhaust) & df["m5_bbw_pips"].notna() & (df["atr14_pips"] >= 1.0)
    sub_ex = df[cond_ex].copy()
    if not sub_ex.empty:
        is_cand_ex = (body_rev_ratio.loc[sub_ex.index] >= 0.30) & (sub_ex["abs_m5_slope3_pips"] <= 2.5)
        sub_ex["case_id"] = "GSR-EXHAUST-001"
        sub_ex["symbol"] = symbol
        sub_ex["cohort_role"] = np.where(is_cand_ex, "CANDIDATE", "CONTROL_ONLY")
        sub_ex["direction"] = np.where(up_exhaust.loc[sub_ex.index], -1, 1)
        sub_ex["bin_axis_1"] = assign_disjoint_bin(prev_z.loc[sub_ex.index].abs(), [2.5, 2.8, 3.1, 3.5, 999.0], ["B1_2.5_2.8", "B2_2.8_3.1", "B3_3.1_3.5", "B4_3.5_up"])
        sub_ex["bin_axis_2"] = assign_disjoint_bin(body_rev_ratio.loc[sub_ex.index], [0.0, 0.30, 0.50, 0.75, 999.0], ["B1_sub0.30", "B2_0.30_0.50", "B3_0.50_0.75", "B4_0.75_up"])
        sub_ex["bin_axis_3"] = assign_disjoint_bin(sub_ex["abs_m5_slope3_pips"], [0.0, 0.8, 1.6, 2.5, 999.0], ["B1_sub0.8", "B2_0.8_1.6", "B3_1.6_2.5", "B4_2.5_up"])
        records.append(sub_ex)

    prev_body_atr = df["body_pips"].shift(1) / df["atr14_pips"].shift(1).replace(0, np.nan)
    prev_body_share = df["body_pips"].shift(1) / prev_range
    prev_dir = df["dir_bar"].shift(1)
    decay_ratio = df["range_pips"] / prev_range

    cond_sh = (prev_body_atr >= 2.2) & (prev_body_share >= 0.75) & (decay_ratio <= 0.65) & df["m5_bbw_pips"].notna()
    sub_sh = df[cond_sh].copy()
    if not sub_sh.empty:
        is_cand_sh = (decay_ratio.loc[sub_sh.index] <= 0.45) & (sub_sh["dir_bar"] != prev_dir.loc[sub_sh.index])
        sub_sh["case_id"] = "GSR-SHOCKDECAY-001"
        sub_sh["symbol"] = symbol
        sub_sh["cohort_role"] = np.where(is_cand_sh, "CANDIDATE", "CONTROL_ONLY")
        sub_sh["direction"] = -prev_dir.loc[sub_sh.index].astype(int)
        sub_sh["bin_axis_1"] = assign_disjoint_bin(prev_body_atr.loc[sub_sh.index], [2.2, 2.6, 3.2, 4.0, 999.0], ["B1_2.2_2.6", "B2_2.6_3.2", "B3_3.2_4.0", "B4_4.0_up"])
        sub_sh["bin_axis_2"] = assign_disjoint_bin(decay_ratio.loc[sub_sh.index], [0.0, 0.25, 0.35, 0.45, 0.65], ["B1_sub0.25", "B2_0.25_0.35", "B3_0.35_0.45", "B4_0.45_0.65"])
        sub_sh["bin_axis_3"] = assign_disjoint_bin(sub_sh["atr14_pips"], [0.0, 1.5, 2.5, 3.5, 999.0], ["B1_sub1.5", "B2_1.5_2.5", "B3_2.5_3.5", "B4_3.5_up"])
        records.append(sub_sh)

    if not records:
        return pd.DataFrame()

    out = pd.concat(records, ignore_index=True)
    out["decision_open_utc"] = out["dt_utc"]
    out["expected_entry_utc"] = out["signal_utc"]
    out["expected_expiry_utc"] = out["signal_utc"] + pd.Timedelta(minutes=5)
    out["win_loss_label"] = "HOLD_LABEL_FREE"
    out["net_pips_result"] = "HOLD_LABEL_FREE"

    keep_cols = [
        "case_id", "symbol", "cohort_role", "direction",
        "decision_open_utc", "signal_utc", "expected_entry_utc", "expected_expiry_utc",
        "m5_close_utc", "continuity_6bar_status",
        "atr14_pips", "m5_bbw_pips", "abs_m5_slope3_pips",
        "bin_axis_1", "bin_axis_2", "bin_axis_3",
        "win_loss_label", "net_pips_result",
    ]
    return out[keep_cols]

def main() -> None:
    ts_str = datetime.now(JST).strftime("%Y%m%d_%H%M%S")
    out_dir = STAGE1_DIR / f"output_is_profile_gsr_2026w47_{ts_str}"
    out_dir.mkdir(parents=True, exist_ok=True)

    symbols_spec = [("USDJPY", 0.01), ("EURUSD", 0.0001)]
    all_ledgers = []
    data_audit = {}

    for sym, pip_sz in symbols_spec:
        csv_p = find_m1_csv(sym)
        if csv_p is None or csv_p.stat().st_size < 50_000_000:
            data_audit[sym] = {
                "status": "skipped_no_full_is_file",
                "found_file": csv_p.name if csv_p else "none"
            }
            continue
        df_is, st = load_and_lock_is_m1(csv_p, pip_sz)
        data_audit[sym] = st
        if len(df_is) > 0:
            cand_df = extract_candidates_for_symbol(df_is, sym, pip_sz)
            if not cand_df.empty:
                all_ledgers.append(cand_df)

    ledger_path = out_dir / "is_2015_2021_opportunity_ledger_gsr_2026w47.csv"
    if all_ledgers:
        full_ledger = pd.concat(all_ledgers, ignore_index=True)
        full_ledger.to_csv(ledger_path, index=False, encoding="utf-8")
        ledger_sha = calc_sha256(ledger_path)
        summary_counts = {}
        for (cid, sym, role, status), cnt in full_ledger.groupby(["case_id", "symbol", "cohort_role", "continuity_6bar_status"]).size().items():
            key = f"{cid} | {sym} | {role} | {status}"
            summary_counts[key] = int(cnt)
    else:
        ledger_sha = "unknown"
        summary_counts = {}

    manifest = {
        "pipeline_case_id": PIPELINE_CASE_ID,
        "script_version": SCRIPT_VERSION,
        "domain_mode": "WEEKLY_SURVEY_STAGE1",
        "generated_at_jst": datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S"),
        "oos_lock_enforced": True,
        "label_free_verified": True,
        "data_integrity_audit": data_audit,
        "opportunity_ledger_csv": ledger_path.name if all_ledgers else "unknown",
        "opportunity_ledger_sha256": ledger_sha,
        "candidate_counts_summary": summary_counts,
    }
    manifest_path = out_dir / "stage1_to_stage2_handover_manifest_gsr_2026w47.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()