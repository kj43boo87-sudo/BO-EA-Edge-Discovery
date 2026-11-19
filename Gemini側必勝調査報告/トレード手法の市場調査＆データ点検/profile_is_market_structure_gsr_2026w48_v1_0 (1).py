#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GSR-2026W48 Stage 1: GSR-TKYFIX-002 Label-Free Opportunity Ledger Generator (v1.0.1)
Remediation: Strict Raw M1 OHLC Measurement (Zero Proxy Constants / Zero Bin-Reverse Synthesis)
"""

import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timezone, timedelta
import numpy as np
import pandas as pd

SCRIPT_VERSION = "1.0.1"
CASE_ID = "GSR-2026W48"
TARGET_CANDIDATE_ID = "GSR-TKYFIX-002"
PARENT_CANDIDATE_ID = "GSR-TKYFIX-001"
SYMBOL = "USDJPY"
PIP_SIZE = 0.01

DEFAULT_RAW_M1_PATH = r"G:\マイドライブ\通貨ペア\Dukascopy 1分足\USDJPY\2026.10.16USDJPY(3)-M1-No Session.csv"
DEFAULT_W47_LEDGER_PATH = r"G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\トレード手法の市場調査＆データ点検\is_2015_2021_opportunity_ledger_gsr_2026w47.csv"
DEFAULT_STAGE1_DIR = r"G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\トレード手法の市場調査＆データ点検"
EXPECTED_RAW_M1_SHA256 = "aa778785e1a0210a17b5a9c8198664cf34f698c139b02b92322118366e929c29"

IS_START_UTC = "2015-01-01 00:00:00"
IS_END_UTC = "2021-12-31 23:59:59"
OOS_BOUNDARY_UTC = "2022-01-01 00:00:00"


def compute_sha256(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def classify_bin_axis_1(move15m_atr: float) -> str:
    if move15m_atr < 2.0:
        return "B1_1.5_2.0"
    elif move15m_atr < 2.6:
        return "B2_2.0_2.6"
    elif move15m_atr < 3.5:
        return "B3_2.6_3.5"
    else:
        return "B4_3.5_up"


def classify_bin_axis_2(atr14_pips: float) -> str:
    if atr14_pips < 1.5:
        return "B1_sub1.5"
    elif atr14_pips < 2.5:
        return "B2_1.5_2.5"
    elif atr14_pips < 4.0:
        return "B3_2.5_4.0"
    else:
        return "B4_4.0_up"


def classify_bin_axis_3(wick_ratio: float) -> str:
    if wick_ratio < 0.25:
        return "B1_sub0.25"
    elif wick_ratio < 0.40:
        return "B2_0.25_0.40"
    elif wick_ratio < 0.55:
        return "B3_0.40_0.55"
    else:
        return "B4_0.55_up"


def classify_wick_grade_and_role(wick_ratio: float, move15m_atr: float, bar54_body_dir_matches_move: bool) -> tuple:
    if wick_ratio >= 0.25:
        return "PURE_STRONG", "CANDIDATE"
    elif wick_ratio >= 0.12 and not bar54_body_dir_matches_move:
        return "WEAK_SUB", "CANDIDATE"
    else:
        return "NONE", "CONTROL_ONLY"


def load_raw_m1_is_only(raw_csv_path: str) -> tuple:
    if not os.path.exists(raw_csv_path):
        raise FileNotFoundError(f"Raw M1 CSV not found: {raw_csv_path}")

    raw_sha256 = compute_sha256(raw_csv_path)
    raw_bytes = os.path.getsize(raw_csv_path)

    total_raw_rows = 0
    dropped_pre_2015 = 0
    dropped_post_2021_oos = 0
    kept_rows = []

    with open(raw_csv_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        for row in reader:
            total_raw_rows += 1
            if len(row) < 6:
                continue
            d_raw, t_raw = row[0].strip(), row[1].strip()
            if not d_raw or not d_raw[0].isdigit():
                continue
            d_iso = d_raw.replace(".", "-")
            if d_iso < "2015-01-01":
                dropped_pre_2015 += 1
                continue
            if d_iso >= "2022-01-01":
                dropped_post_2021_oos += 1
                continue
            if "00:20" <= t_raw <= "01:05":
                kept_rows.append((
                    f"{d_iso} {t_raw}:00",
                    d_iso,
                    f"{t_raw}:00",
                    float(row[2]),
                    float(row[3]),
                    float(row[4]),
                    float(row[5]),
                ))

    df = pd.DataFrame(
        kept_rows,
        columns=["dt_str", "trade_date", "time_utc", "open", "high", "low", "close"]
    )
    df["dt"] = pd.to_datetime(df["dt_str"])
    df = df.sort_values("dt").reset_index(drop=True)
    df["range_pips"] = (df["high"] - df["low"]) / PIP_SIZE
    df["atr14_pips"] = df.groupby("trade_date")["range_pips"].transform(
        lambda s: s.rolling(14, min_periods=14).mean()
    )

    audit_meta = {
        "file_path": raw_csv_path,
        "sha256": raw_sha256,
        "sha256_matches_expected": (raw_sha256 == EXPECTED_RAW_M1_SHA256),
        "bytes": raw_bytes,
        "total_raw_rows": total_raw_rows,
        "dropped_pre_2015_rows": dropped_pre_2015,
        "dropped_post_2021_oos_rows": dropped_post_2021_oos,
        "window_filtered_is_rows": len(df),
    }
    return df, audit_meta


def load_w47_reference_rows(w47_csv_path: str) -> dict:
    ref = {}
    if not os.path.exists(w47_csv_path):
        return ref
    with open(w47_csv_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r.get("candidate_id") == PARENT_CANDIDATE_ID:
                ref[r["session_date_utc"]] = r
    return ref


def assert_no_proxy_constants(df_12: pd.DataFrame) -> dict:
    proxy_wick_set = {0.08, 0.195, 0.295, 0.325, 0.475, 0.68}
    unique_wicks = set(df_12["wick_rejection_ratio"].round(4).unique())
    unique_ranges = df_12["pre_15m_range_pips"].nunique()
    unique_bodies = df_12["pre_15m_body_pips"].nunique()
    range_ge_body_all = bool((df_12["pre_15m_range_pips"] >= df_12["pre_15m_body_pips"] - 1e-9).all())

    if len(unique_wicks) <= 10 or unique_wicks.issubset(proxy_wick_set):
        raise AssertionError(f"FAIL: Proxy constant synthesis detected in wick_rejection_ratio! Unique={unique_wicks}")
    if not range_ge_body_all:
        raise AssertionError("FAIL: Found rows where pre_15m_range_pips < pre_15m_body_pips!")

    return {
        "unique_wick_rejection_ratio_count": int(len(unique_wicks)),
        "unique_pre_15m_range_pips_count": int(unique_ranges),
        "unique_pre_15m_body_pips_count": int(unique_bodies),
        "range_ge_body_100pct": range_ge_body_all,
        "proxy_constant_synthesis_detected": False,
    }


def build_ledgers(df_m1: pd.DataFrame, w47_ref: dict) -> tuple:
    req_15m = [f"00:{m:02d}:00" for m in range(40, 55)]
    req_6bar = [f"00:{m:02d}:00" for m in range(55, 60)] + ["01:00:00"]

    rows_12 = []
    rows_27 = []
    seq_id = 0

    for trade_date, grp in df_m1.groupby("trade_date", sort=True):
        if w47_ref and trade_date not in w47_ref:
            continue

        idx_grp = grp.set_index("time_utc")
        if not all(t in idx_grp.index for t in req_15m):
            continue

        win_15m = idx_grp.loc[req_15m]
        bar_40 = idx_grp.loc["00:40:00"]
        bar_54 = idx_grp.loc["00:54:00"]
        atr14 = float(bar_54["atr14_pips"])
        if np.isnan(atr14) or atr14 <= 0:
            continue

        pre_15m_range_pips = round(float((win_15m["high"].max() - win_15m["low"].min()) / PIP_SIZE), 4)
        signed_move_pips = float((bar_54["close"] - bar_40["open"]) / PIP_SIZE)
        pre_15m_body_pips = round(abs(signed_move_pips), 4)
        move15m_atr = pre_15m_body_pips / atr14

        if not w47_ref and move15m_atr < 1.5:
            continue

        if signed_move_pips > 0:
            direction = "SELL"
            counter_wick = float(bar_54["high"] - max(bar_54["open"], bar_54["close"]))
            bar54_same_dir = (float(bar_54["close"]) > float(bar_54["open"]))
        elif signed_move_pips < 0:
            direction = "BUY"
            counter_wick = float(min(bar_54["open"], bar_54["close"]) - bar_54["low"])
            bar54_same_dir = (float(bar_54["close"]) < float(bar_54["open"]))
        else:
            if not w47_ref:
                continue
            direction = w47_ref[trade_date]["direction"]
            counter_wick = 0.0
            bar54_same_dir = False

        bar54_range = float(bar_54["high"] - bar_54["low"])
        wick_rejection_ratio = round((counter_wick / bar54_range) if bar54_range > 0 else 0.0, 4)

        m1_cont_pass = 1 if all(t in idx_grp.index for t in req_6bar) else 0
        cont_status = "PASS_6BAR_COMPLETE" if m1_cont_pass == 1 else "FAIL_MISSING_BAR"

        dt_obj = datetime.strptime(trade_date, "%Y-%m-%d")
        dow_int = dt_obj.weekday()
        dow_str = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dow_int]
        day_num = dt_obj.day
        gotobi_flag = 1 if (day_num % 5 == 0 or (dow_int == 4 and (day_num + 1) % 5 == 0) or (dow_int == 4 and (day_num + 2) % 5 == 0)) else 0

        if trade_date in w47_ref:
            w = w47_ref[trade_date]
            gotobi_flag = int(w["gotobi_flag"])
            cohort_role = w["cohort_role"]
            bin1 = classify_bin_axis_1(move15m_atr)
            bin2 = classify_bin_axis_2(atr14)
            bin3 = classify_bin_axis_3(wick_rejection_ratio)
            if cohort_role == "CONTROL_ONLY":
                wick_grade = "NONE"
            elif wick_rejection_ratio >= 0.25:
                wick_grade = "PURE_STRONG"
            else:
                wick_grade = "WEAK_SUB"
        else:
            bin1 = classify_bin_axis_1(move15m_atr)
            bin2 = classify_bin_axis_2(atr14)
            bin3 = classify_bin_axis_3(wick_rejection_ratio)
            wick_grade, cohort_role = classify_wick_grade_and_role(wick_rejection_ratio, move15m_atr, bar54_same_dir)

        seq_id += 1
        opp_id_str = f"GSR-TKYFIX-002-{seq_id:04d}"

        rows_12.append({
            "opportunity_id": seq_id,
            "trade_date": trade_date,
            "entry_time": "09:55:00",
            "eval_end_time": "10:00:00",
            "direction": direction,
            "pre_15m_range_pips": pre_15m_range_pips,
            "pre_15m_body_pips": pre_15m_body_pips,
            "wick_rejection_ratio": wick_rejection_ratio,
            "wick_rejection_grade": wick_grade,
            "day_of_week": dow_int,
            "gotobi_flag": gotobi_flag,
            "m1_continuity_pass": m1_cont_pass,
        })

        rows_27.append({
            "opportunity_id": opp_id_str,
            "case_id": TARGET_CANDIDATE_ID,
            "parent_case_id": PARENT_CANDIDATE_ID,
            "symbol": SYMBOL,
            "trade_date": trade_date,
            "decision_open_utc": f"{trade_date} 00:40:00",
            "signal_utc": f"{trade_date} 00:54:00",
            "expected_entry_utc": f"{trade_date} 00:55:00",
            "expected_expiry_utc": f"{trade_date} 01:00:00",
            "entry_time": "09:55:00",
            "eval_end_time": "10:00:00",
            "direction": direction,
            "cohort_role": cohort_role,
            "wick_rejection_grade": wick_grade,
            "wick_rejection_ratio": wick_rejection_ratio,
            "pre_15m_range_pips": pre_15m_range_pips,
            "pre_15m_body_pips": pre_15m_body_pips,
            "atr14_pips": round(atr14, 4),
            "day_of_week": dow_str,
            "gotobi_flag": gotobi_flag,
            "m1_continuity_pass": m1_cont_pass,
            "continuity_6bar_status": cont_status,
            "bin_axis_1_move15m_atr": bin1,
            "bin_axis_2_atr14": bin2,
            "bin_axis_3_wick_ratio": bin3,
            "win_loss_label": "MASKED_STAGE1",
            "net_pips_result": "MASKED_STAGE1",
        })

    return pd.DataFrame(rows_12), pd.DataFrame(rows_27)


def main():
    raw_m1_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_RAW_M1_PATH
    stage1_dir = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_STAGE1_DIR
    w47_ledger_path = os.path.join(stage1_dir, "is_2015_2021_opportunity_ledger_gsr_2026w47.csv")
    if not os.path.exists(w47_ledger_path):
        w47_ledger_path = DEFAULT_W47_LEDGER_PATH

    os.makedirs(stage1_dir, exist_ok=True)

    df_m1, raw_audit = load_raw_m1_is_only(raw_m1_path)
    w47_ref = load_w47_reference_rows(w47_ledger_path)
    df_12, df_27 = build_ledgers(df_m1, w47_ref)
    falsification_check = assert_no_proxy_constants(df_12)

    out_csv_12 = os.path.join(stage1_dir, "is_2015_2021_opportunity_ledger_gsr_2026w48.csv")
    out_csv_27 = os.path.join(stage1_dir, "is_2015_2021_opportunity_ledger_gsr_2026w48_masked_v22.csv")
    out_manifest = os.path.join(stage1_dir, "stage1_to_stage2_handover_manifest_gsr_2026w48.json")
    out_handover = os.path.join(stage1_dir, "HANDOVER_GSR_2026W48_STAGE1.md")

    df_12.to_csv(out_csv_12, index=False, float_format="%.4f")
    df_27.to_csv(out_csv_27, index=False, float_format="%.4f")

    sha_script = compute_sha256(os.path.abspath(__file__))
    sha_12 = compute_sha256(out_csv_12)
    sha_27 = compute_sha256(out_csv_27)

    exp_a_counts = df_27["wick_rejection_grade"].value_counts().to_dict()
    cand_df = df_27[df_27["cohort_role"] == "CANDIDATE"]
    exp_b_body_thresholds = {
        f"body_ge_{th:.1f}pips": int((cand_df["pre_15m_body_pips"] >= th).sum())
        for th in [3.0, 4.0, 5.0, 6.0, 8.0, 10.0]
    }
    exp_b_range_thresholds = {
        f"range_ge_{th:.1f}pips": int((cand_df["pre_15m_range_pips"] >= th).sum())
        for th in [4.0, 6.0, 8.0, 10.0, 12.0]
    }
    exp_c_coarse = {
        "axis1_move15m_atr": cand_df["bin_axis_1_move15m_atr"].value_counts().to_dict(),
        "axis2_atr14": cand_df["bin_axis_2_atr14"].value_counts().to_dict(),
        "axis3_wick_ratio": cand_df["bin_axis_3_wick_ratio"].value_counts().to_dict(),
    }

    manifest = {
        "manifest_version": "1.0.1",
        "script_version": SCRIPT_VERSION,
        "case_id": CASE_ID,
        "target_candidate_id": TARGET_CANDIDATE_ID,
        "parent_candidate_id": PARENT_CANDIDATE_ID,
        "executed_at_jst": datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds"),
        "is_period_gate": f"{IS_START_UTC} <= dt <= {IS_END_UTC} (2022+ strictly blocked)",
        "label_free_mode": True,
        "raw_m1_audit": raw_audit,
        "self_falsification_gate1": falsification_check,
        "deliverables": {
            "script": {
                "filename": os.path.basename(__file__),
                "sha256": sha_script,
                "bytes": os.path.getsize(os.path.abspath(__file__)),
            },
            "opportunity_ledger_12col": {
                "filename": os.path.basename(out_csv_12),
                "sha256": sha_12,
                "bytes": os.path.getsize(out_csv_12),
                "rows": int(len(df_12)),
            },
            "opportunity_ledger_27col_masked_v22": {
                "filename": os.path.basename(out_csv_27),
                "sha256": sha_27,
                "bytes": os.path.getsize(out_csv_27),
                "rows": int(len(df_27)),
            },
        },
        "experiment_cohort_summary": {
            "total_rows": int(len(df_27)),
            "candidate_rows": int(len(cand_df)),
            "control_only_rows": int((df_27["cohort_role"] == "CONTROL_ONLY").sum()),
            "experiment_A_wick_grades": exp_a_counts,
            "experiment_B_candidate_body_pips_thresholds": exp_b_body_thresholds,
            "experiment_B_candidate_range_pips_thresholds": exp_b_range_thresholds,
            "experiment_C_candidate_coarse_slices": exp_c_coarse,
        },
        "preview_top20_rows": df_12.head(20).to_dict(orient="records"),
    }

    with open(out_manifest, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    sha_manifest = compute_sha256(out_manifest)

    # Auto-generate HANDOVER_GSR_2026W48_STAGE1.md with verified real hashes and top 20 rows
    top20_md_lines = [
        "| opportunity_id | trade_date | entry_time | eval_end_time | direction | pre_15m_range_pips | pre_15m_body_pips | wick_rejection_ratio | wick_rejection_grade | day_of_week | gotobi_flag | m1_continuity_pass |",
        "|---:|:---|:---|:---|:---|---:|---:|---:|:---|---:|---:|---:|"
    ]
    for r in df_12.head(20).to_dict(orient="records"):
        top20_md_lines.append(
            f"| {r['opportunity_id']} | {r['trade_date']} | {r['entry_time']} | {r['eval_end_time']} | {r['direction']} | {r['pre_15m_range_pips']:.4f} | {r['pre_15m_body_pips']:.4f} | {r['wick_rejection_ratio']:.4f} | {r['wick_rejection_grade']} | {r['day_of_week']} | {r['gotobi_flag']} | {r['m1_continuity_pass']} |"
        )

    handover_md = f"""# GSR-2026W48 第1工程→第2工程 引き継ぎ書（v1.0.1 生M1実測再計算版）

- **案件ID**: `{CASE_ID}`（検証対象: `{TARGET_CANDIDATE_ID}` / 親案件: `{PARENT_CANDIDATE_ID}`）
- **スクリプトバージョン**: `{SCRIPT_VERSION}`（Proxy定数合成完全排除・生M1 OHLC実測版）
- **対象データ期間**: `{IS_START_UTC}` 〜 `{IS_END_UTC}`（2022年以降OOS完全遮断）
- **生M1データSHA256**: `{raw_audit['sha256']}`（一致判定: `{raw_audit['sha256_matches_expected']}`）

## 1. 成果物SHA256・サイズ・行数一覧

| ファイル名 | SHA256 | サイズ (Bytes) | 行数 |
|:---|:---|---:|---:|
| `profile_is_market_structure_gsr_2026w48_v1_0.py` | `{sha_script}` | {os.path.getsize(os.path.abspath(__file__))} | - |
| `is_2015_2021_opportunity_ledger_gsr_2026w48.csv` | `{sha_12}` | {os.path.getsize(out_csv_12)} | {len(df_12)} |
| `is_2015_2021_opportunity_ledger_gsr_2026w48_masked_v22.csv` | `{sha_27}` | {os.path.getsize(out_csv_27)} | {len(df_27)} |
| `stage1_to_stage2_handover_manifest_gsr_2026w48.json` | `{sha_manifest}` | {os.path.getsize(out_manifest)} | - |

## 2. 実験A・B・C 実測コホート件数サマリ（Label-Free）

- **総機会行数**: `{len(df_27)}` 行（CANDIDATE `{len(cand_df)}` 行 / CONTROL_ONLY `{(df_27['cohort_role'] == 'CONTROL_ONLY').sum()}` 行）
- **実験A（ヒゲ拒絶純度区分）**: `{json.dumps(exp_a_counts, ensure_ascii=False)}`
- **実験B（CANDIDATE内 `pre_15m_body_pips` 下限別件数）**: `{json.dumps(exp_b_body_thresholds, ensure_ascii=False)}`
- **実験B（CANDIDATE内 `pre_15m_range_pips` 下限別件数）**: `{json.dumps(exp_b_range_thresholds, ensure_ascii=False)}`
- **実験C（CANDIDATE内 非重複粗視化スライス件数）**: `{json.dumps(exp_c_coarse, ensure_ascii=False)}`

## 3. 先頭20行 生M1実測プレビュー

""" + "\n".join(top20_md_lines) + "\n"

    with open(out_handover, "w", encoding="utf-8") as f:
        f.write(handover_md)

    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
