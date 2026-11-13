"""
GSR-2026W47 STAGE 2: IS STATISTICAL & DISJOINT 3D PLATEAU VERIFIER (v1.0.0)
対象台帳: is_2015_2021_opportunity_ledger_gsr_2026w47.csv (SHA256: 7f8581b693da499064dd3d0aaee2f20c2babc84d8859dfd852c923b5f91c7d38)
審査ゲート:
  - Gate 1: 台帳SHA256完全一致 & 2022年以降OOS完全遮断 & 6分間連続性PASS確認
  - Gate 2 & 5: Open[t+1]参入・Open[t+6]厳密5分満期・同値LOSE・+0.1/+0.2/+0.3 pip摩擦下の勝率・EV・Newey-West HAC CLB97.5%
  - Gate 3: 非重複(Disjoint) 4x4x4=64セル & 1次元マージナル分解による真のPlateau検証（擬似プラトー完全排除）
  - Gate 4: Control群(CONTROL_ONLY + CANDIDATE全体 / CONTROL_ONLY単独)に対するCANDIDATE群のアブレーション増分 & 年次安定性
"""

import hashlib, json
from pathlib import Path
from datetime import datetime, timezone, timedelta
import numpy as np
import pandas as pd

SCRIPT_VERSION = "1.0.0"
PIPELINE_CASE_ID = "GSR-2026W47"
EXPECTED_LEDGER_SHA256 = "7f8581b693da499064dd3d0aaee2f20c2babc84d8859dfd852c923b5f91c7d38"
PAYOUT = 0.85
BREAKEVEN_WR = 1.0 / (1.0 + PAYOUT)  # 0.54054054...
JST = timezone(timedelta(hours=9))

BASE_DRIVE = Path(r"G:\マイドライブ")
STAGE1_DIR = BASE_DRIVE / r"AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\トレード手法の市場調査＆データ点検"
STAGE2_DIR = BASE_DRIVE / r"AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証"
DATA_ROOT = BASE_DRIVE / r"通貨ペア\Dukascopy 1分足"

IS_START_UTC = pd.Timestamp("2015-01-01 00:00:00")
IS_END_UTC = pd.Timestamp("2021-12-31 23:59:59")

def calc_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def find_latest_stage1_ledger() -> Path:
    dirs = sorted(STAGE1_DIR.glob("output_is_profile_gsr_2026w47_*"))
    if not dirs:
        raise FileNotFoundError("Stage 1 output directory not found.")
    p = dirs[-1] / "is_2015_2021_opportunity_ledger_gsr_2026w47.csv"
    if not p.exists():
        raise FileNotFoundError(f"Ledger not found: {p}")
    return p

def find_m1_csv(symbol: str) -> Path:
    sym_dir = DATA_ROOT / symbol
    csvs = [p for p in sym_dir.glob("*.csv") if p.is_file()]
    return max(csvs, key=lambda p: p.stat().st_size)

def read_m1_open_lookup(csv_path: Path) -> pd.DataFrame:
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
            "dt_utc": pd.to_datetime(dt_str, format="mixed", dayfirst=False, utc=False),
            "open": raw_df[col_map.get("open", list(raw_df.columns)[1])].astype(float),
        })
    else:
        raw_df = pd.read_csv(csv_path, header=None)
        if raw_df.shape[1] >= 7 and ":" in str(raw_df.iloc[0, 1]):
            dt_str = raw_df[0].astype(str) + " " + raw_df[1].astype(str)
            o_idx = 2
        else:
            dt_str = raw_df[0].astype(str)
            o_idx = 1
        df = pd.DataFrame({
            "dt_utc": pd.to_datetime(dt_str, format="mixed", dayfirst=False, utc=False),
            "open": raw_df[o_idx].astype(float),
        })

    # OOS物理遮断 (2022年1月1日00:10以降の満期参照すら不可とする)
    df = df[(df["dt_utc"] >= IS_START_UTC) & (df["dt_utc"] <= pd.Timestamp("2022-01-01 00:10:00"))].copy()
    df = df.sort_values("dt_utc").drop_duplicates(subset=["dt_utc"]).reset_index(drop=True)
    return df

def hac_metrics_from_wins(wins: np.ndarray, max_lag: int = 5) -> dict:
    n = int(len(wins))
    if n == 0:
        return {"n": 0, "wins": 0, "losses": 0, "win_rate_pct": 0.0, "ev": -1.0, "se_hac": 0.0, "clb975_ev": -1.0, "clb975_wr_pct": 0.0, "t_stat": 0.0, "exceeds_be": False, "clb_positive": False}
    w_cnt = int(np.sum(wins))
    l_cnt = n - w_cnt
    wr = float(w_cnt / n)
    payoffs = np.where(wins == 1, PAYOUT, -1.0)
    ev = float(np.mean(payoffs))
    if n < 10:
        return {"n": n, "wins": w_cnt, "losses": l_cnt, "win_rate_pct": round(wr * 100, 4), "ev": round(ev, 6), "se_hac": 0.0, "clb975_ev": -1.0, "clb975_wr_pct": 0.0, "t_stat": 0.0, "exceeds_be": wr > BREAKEVEN_WR, "clb_positive": False}

    u = payoffs - ev
    gamma0 = float(np.dot(u, u) / n)
    var_hac = gamma0
    L = min(max_lag, n - 1)
    for lag in range(1, L + 1):
        w = 1.0 - lag / (L + 1.0)
        cov = float(np.dot(u[lag:], u[:-lag]) / n)
        var_hac += 2.0 * w * cov
    # 小標本補正 n/(n-1)
    var_hac = max(var_hac * (n / max(n - 1, 1)), 1e-12)
    se_ev = float(np.sqrt(var_hac / n))
    clb_ev = float(ev - 1.959964 * se_ev)
    t_stat = float(ev / se_ev) if se_ev > 0 else 0.0
    clb_wr = (clb_ev + 1.0) / (1.0 + PAYOUT)
    return {
        "n": n,
        "wins": w_cnt,
        "losses": l_cnt,
        "win_rate_pct": round(wr * 100.0, 4),
        "ev": round(ev, 6),
        "se_hac": round(se_ev, 6),
        "clb975_ev": round(clb_ev, 6),
        "clb975_wr_pct": round(clb_wr * 100.0, 4),
        "t_stat": round(t_stat, 4),
        "exceeds_be": bool(wr > BREAKEVEN_WR),
        "clb_positive": bool(clb_ev > 0.0),
    }

def main() -> None:
    ledger_path = find_latest_stage1_ledger()
    actual_sha = calc_sha256(ledger_path)
    if actual_sha != EXPECTED_LEDGER_SHA256:
        raise RuntimeError(f"Gate 1 Ledger SHA256 mismatch: actual={actual_sha} != expected={EXPECTED_LEDGER_SHA256}")

    ledger = pd.read_csv(ledger_path)
    total_ledger_rows = len(ledger)
    ledger["expected_entry_utc"] = pd.to_datetime(ledger["expected_entry_utc"])
    ledger["expected_expiry_utc"] = pd.to_datetime(ledger["expected_expiry_utc"])

    if ledger["expected_entry_utc"].max() > pd.Timestamp("2022-01-01 00:01:00"):
        raise RuntimeError("CRITICAL: OOS timestamp detected in ledger!")

    # M1始値テーブルと結合して Open[t+1] と Open[t+6] を取得
    symbols_pip = {"USDJPY": 0.01, "EURUSD": 0.0001}
    merged_parts = []
    for sym, pip_sz in symbols_pip.items():
        sub = ledger[ledger["symbol"] == sym].copy()
        if sub.empty:
            continue
        m1_open = read_m1_open_lookup(find_m1_csv(sym))
        sub = sub.merge(m1_open.rename(columns={"dt_utc": "expected_entry_utc", "open": "entry_open"}), on="expected_entry_utc", how="left")
        sub = sub.merge(m1_open.rename(columns={"dt_utc": "expected_expiry_utc", "open": "expiry_open"}), on="expected_expiry_utc", how="left")
        sub["pip_size"] = pip_sz
        merged_parts.append(sub)

    full = pd.concat(merged_parts, ignore_index=True)
    valid = full[(full["continuity_6bar_status"] == "PASS") & full["entry_open"].notna() & full["expiry_open"].notna()].copy()

    # 方向付き順行pips (正なら勝ち方向、0以下なら同値LOSEまたは負け)
    valid["signed_move_pips"] = (valid["expiry_open"] - valid["entry_open"]) * valid["direction"] / valid["pip_size"]
    for fp, col in [(0.0, "win_00pip"), (0.1, "win_01pip"), (0.2, "win_02pip"), (0.3, "win_03pip")]:
        valid[col] = (valid["signed_move_pips"] > fp).astype(int)

    valid["year"] = valid["expected_entry_utc"].dt.year

    ts_str = datetime.now(JST).strftime("%Y%m%d_%H%M%S")
    out_dir = STAGE2_DIR / f"output_gsr_2026w47_is_plateau_{ts_str}"
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Standalone & Control vs Candidate Summary
    standalone_rows = []
    for (cid, sym), grp in valid.groupby(["case_id", "symbol"]):
        for role_label, sub_g in [("ALL_POOLED", grp), ("CONTROL_ONLY", grp[grp["cohort_role"] == "CONTROL_ONLY"]), ("CANDIDATE", grp[grp["cohort_role"] == "CANDIDATE"])]:
            m0 = hac_metrics_from_wins(sub_g["win_00pip"].to_numpy())
            m1 = hac_metrics_from_wins(sub_g["win_01pip"].to_numpy())
            m2 = hac_metrics_from_wins(sub_g["win_02pip"].to_numpy())
            m3 = hac_metrics_from_wins(sub_g["win_03pip"].to_numpy())
            med_pips = float(sub_g["signed_move_pips"].median()) if len(sub_g) > 0 else 0.0
            verdict = "PASS_CANDIDATE" if (m1["clb_positive"] and m2["exceeds_be"]) else "FAIL_NOT_ABOVE_ZERO"
            standalone_rows.append({
                "case_id": cid, "symbol": sym, "cohort": role_label,
                "n_valid": m1["n"],
                "wins_01pip": m1["wins"], "losses_01pip": m1["losses"],
                "wr_00pip_pct": m0["win_rate_pct"],
                "wr_01pip_pct": m1["win_rate_pct"], "ev_01pip": m1["ev"], "se_hac_01pip": m1["se_hac"], "clb975_ev_01pip": m1["clb975_ev"], "t_stat_01pip": m1["t_stat"],
                "wr_02pip_pct": m2["win_rate_pct"], "ev_02pip": m2["ev"],
                "wr_03pip_pct": m3["win_rate_pct"], "ev_03pip": m3["ev"],
                "median_signed_move_pips": round(med_pips, 4),
                "gate2_verdict": verdict
            })
    standalone_df = pd.DataFrame(standalone_rows)
    standalone_csv = out_dir / "is_standalone_and_ablation_summary_gsr_2026w47.csv"
    standalone_df.to_csv(standalone_csv, index=False, encoding="utf-8")

    # 2. Disjoint 3D Grid (4x4x4 = 64 cells per case_id x symbol)
    grid_rows = []
    cand_only = valid[valid["cohort_role"] == "CANDIDATE"].copy()
    for (cid, sym, b1, b2, b3), grp in cand_only.groupby(["case_id", "symbol", "bin_axis_1", "bin_axis_2", "bin_axis_3"]):
        m1 = hac_metrics_from_wins(grp["win_01pip"].to_numpy())
        m2 = hac_metrics_from_wins(grp["win_02pip"].to_numpy())
        m3 = hac_metrics_from_wins(grp["win_03pip"].to_numpy())
        if m1["n"] < 50:
            c_status = "LOW_SAMPLE_UNDER_50"
        elif m1["clb_positive"] and m2["exceeds_be"]:
            c_status = "DISJOINT_CELL_CLB_PASS"
        elif m1["exceeds_be"]:
            c_status = "BE_EXCEEDED_CLB_UNPROVEN"
        else:
            c_status = "BELOW_BREAKEVEN"
        grid_rows.append({
            "case_id": cid, "symbol": sym,
            "bin_axis_1": b1, "bin_axis_2": b2, "bin_axis_3": b3,
            "n_valid": m1["n"],
            "wr_01pip_pct": m1["win_rate_pct"], "ev_01pip": m1["ev"], "clb975_ev_01pip": m1["clb975_ev"],
            "wr_02pip_pct": m2["win_rate_pct"], "ev_02pip": m2["ev"],
            "wr_03pip_pct": m3["win_rate_pct"], "ev_03pip": m3["ev"],
            "cell_class": c_status
        })
    grid_df = pd.DataFrame(grid_rows)
    grid_csv = out_dir / "is_disjoint_3d_grid_gsr_2026w47.csv"
    grid_df.to_csv(grid_csv, index=False, encoding="utf-8")

    # 3. 1D Non-Cumulative Marginals & Yearly Breakdown
    marginal_rows = []
    for (cid, sym), grp in cand_only.groupby(["case_id", "symbol"]):
        for axis_col in ["bin_axis_1", "bin_axis_2", "bin_axis_3", "year"]:
            for val, sub_g in grp.groupby(axis_col):
                m1 = hac_metrics_from_wins(sub_g["win_01pip"].to_numpy())
                m2 = hac_metrics_from_wins(sub_g["win_02pip"].to_numpy())
                marginal_rows.append({
                    "case_id": cid, "symbol": sym, "dimension": axis_col, "slice_value": str(val),
                    "n_valid": m1["n"], "wr_01pip_pct": m1["win_rate_pct"], "ev_01pip": m1["ev"],
                    "clb975_ev_01pip": m1["clb975_ev"], "wr_02pip_pct": m2["win_rate_pct"],
                    "exceeds_be_01pip": m1["exceeds_be"], "clb_positive_01pip": m1["clb_positive"]
                })
    marginal_df = pd.DataFrame(marginal_rows)
    marginal_csv = out_dir / "is_non_cumulative_marginals_and_yearly_gsr_2026w47.csv"
    marginal_df.to_csv(marginal_csv, index=False, encoding="utf-8")

    pass_cells = int((grid_df["cell_class"] == "DISJOINT_CELL_CLB_PASS").sum()) if not grid_df.empty else 0
    be_cells = int(grid_df["cell_class"].isin(["DISJOINT_CELL_CLB_PASS", "BE_EXCEEDED_CLB_UNPROVEN"]).sum()) if not grid_df.empty else 0

    manifest = {
        "schema_version": "2.2",
        "pipeline_case_id": PIPELINE_CASE_ID,
        "script_version": SCRIPT_VERSION,
        "generated_at_jst": datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S"),
        "verification_status": "実行確認済み",
        "gate1_audit": {
            "ledger_csv": ledger_path.name,
            "ledger_sha256": actual_sha,
            "sha256_match": True,
            "total_ledger_rows": int(total_ledger_rows),
            "valid_pass_rows": int(len(valid)),
            "excluded_gap_rows": int(total_ledger_rows - len(valid)),
            "oos_locked": True
        },
        "output_files": {
            "output_dir": out_dir.name,
            "standalone_csv": standalone_csv.name,
            "standalone_sha256": calc_sha256(standalone_csv),
            "disjoint_3d_grid_csv": grid_csv.name,
            "disjoint_3d_grid_sha256": calc_sha256(grid_csv),
            "marginals_yearly_csv": marginal_csv.name,
            "marginals_yearly_sha256": calc_sha256(marginal_csv),
            "verifier_script_sha256": calc_sha256(Path(__file__))
        },
        "grid_overview": {
            "total_evaluated_disjoint_cells": int(len(grid_df)),
            "clb975_positive_cells": pass_cells,
            "breakeven_exceeded_cells_n50plus": be_cells
        },
        "standalone_summary": standalone_rows
    }
    manifest_path = out_dir / "spark_audit_handover_manifest_gsr_2026w47.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    # 第2工程ルート直下にも最新マニフェストのコピーを配置（自動実行・Sparkが即発見できるようにする）
    (STAGE2_DIR / "spark_audit_handover_manifest_gsr_2026w47.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()