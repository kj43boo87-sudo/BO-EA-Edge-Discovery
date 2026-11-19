#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GSR-2026W48 STAGE 2: GSR-TKYFIX-002 IS STATISTICAL, CONTAMINATION-REMOVAL ABLATION & COARSE DISJOINT VERIFIER (v1.0.0)
Pipeline Case ID       : GSR-2026W48 (Stage 2 Record ID: GSR-202611-W4-WED)
Evaluated Candidate ID : GSR-TKYFIX-002 (Parent: GSR-TKYFIX-001)
Target Market & Domain : USDJPY M1 / BO_STANDARD (09:54 JST Signal -> 09:55 JST = 00:55 UTC Open[t+1] Entry -> 10:00 JST = 01:00 UTC Open[t+6] 5-min Expiry)

Enforced Verification Contract:
  1. Gate 1 (OOS Lock & Confirmed SHA256 Reconciliation):
     - profile_is_market_structure_gsr_2026w48_v1_0.py : 2b2c6f7201f23ac1ec0f886468a8727355d423d51a3c07034e60671edf18603d
     - is_2015_2021_opportunity_ledger_gsr_2026w48.csv : 4bd7471194c5a534863a81216e73ccc4317bcd25ebead831bbaa7b82d4278cf2
     - is_2015_2021_opportunity_ledger_gsr_2026w48_masked_v22.csv : 279992b79c510fb68ab8ac556543ec37908b4ffbc9d9a54d298e35b4ce942e23
     - stage1_to_stage2_handover_manifest_gsr_2026w48.json : 120bba20aed68ec7181471a54ab83fcc7d0168121b6ccb87deadb3c625687274
     - 2026.10.16USDJPY(3)-M1-No Session.csv           : aa778785e1a0210a17b5a9c8198664cf34f698c139b02b92322118366e929c29
     - Sample Conservation (1,177 rows, 0 'unknown'): PURE_STRONG = 360, WEAK_SUB = 201, NONE (CONTROL_ONLY) = 616
  2. Gate 2, Gate 4 & Gate 5 (Execution, Strict 5-Min Expiry & Friction Stress):
     - Entry = Open[t+1] (00:55:00 UTC / 09:55:00 JST), Expiry = Open[t+6] (01:00:00 UTC / 10:00:00 JST), Tie (Draw) = LOSE
     - Payout = 1.85 (Breakeven WR = 54.054054%), Median Signed Move (pips), +0.0 / +0.1 / +0.2 / +0.3 pip friction stress
     - Newey-West HAC (Bartlett kernel, max_lag=5) 97.5% one-sided lower confidence bound (CLB_97.5%)
  3. Gate 3 (Experiments A, B, C — Non-Cumulative Disjoint Evaluation):
     - Experiment A (TRAP-06 Removal): NONE (n=616), WEAK_SUB (n=201), PURE_STRONG (n=360), and non-cumulative intervals
       [0.25, 0.40) (n=97), [0.40, 0.55) (n=135), [0.55, 1.00] (n=128).
     - Experiment B (Low-Volatility Attenuation Separation): Non-cumulative disjoint slices of pre_15m_range_pips
       ([0, 6.0), [6.0, 9.0), [9.0, 13.0), [13.0, inf)) and pre_15m_body_pips ([0, 3.0), [3.0, 4.5), [4.5, 7.0), [7.0, inf)),
       plus bin_axis_1_move15m_atr and bin_axis_2_atr14.
     - Experiment C (TRAP-07 Removal — Coarse Disjoint Slices on PURE_STRONG n=360):
       (1) Direction (BUY vs SELL), (2) Gotobi flag (1 vs 0), (3) Day of week (Mon..Fri),
       (4) ATR regime (atr14_pips < 2.0p vs >= 2.0p), (5) Yearly stability (2015..2021).
"""

import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
import numpy as np
import pandas as pd

SCRIPT_VERSION = "1.0.0"
PIPELINE_CASE_ID = "GSR-2026W48"
RECORD_ID = "GSR-202611-W4-WED"
TARGET_CANDIDATE_ID = "GSR-TKYFIX-002"
PARENT_CANDIDATE_ID = "GSR-TKYFIX-001"
SYMBOL = "USDJPY"
PIP_SIZE = 0.01
PAYOUT = 0.85
BREAKEVEN_WR = 1.0 / (1.0 + PAYOUT)  # 0.5405405405...
JST = timezone(timedelta(hours=9))

BASE_DRIVE = Path(r"G:\マイドライブ")
STAGE1_DIR = BASE_DRIVE / r"AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\トレード手法の市場調査＆データ点検"
STAGE2_DIR = BASE_DRIVE / r"AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\機会台帳突合＆IS統計\Plateau検証"
if not STAGE2_DIR.exists():
    STAGE2_DIR = BASE_DRIVE / r"AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証"
RAW_M1_PATH = BASE_DRIVE / r"通貨ペア\Dukascopy 1分足\USDJPY\2026.10.16USDJPY(3)-M1-No Session.csv"

EXPECTED_SHA256 = {
    "governance_v12": "0caca9b9759cc28dfad5a50ef3952f2fac9b868d933b68b11d5592b36345dae9",
    "stage1_py": "2b2c6f7201f23ac1ec0f886468a8727355d423d51a3c07034e60671edf18603d",
    "csv12": "4bd7471194c5a534863a81216e73ccc4317bcd25ebead831bbaa7b82d4278cf2",
    "csv27": "279992b79c510fb68ab8ac556543ec37908b4ffbc9d9a54d298e35b4ce942e23",
    "stage1_manifest": "120bba20aed68ec7181471a54ab83fcc7d0168121b6ccb87deadb3c625687274",
    "raw_m1": "aa778785e1a0210a17b5a9c8198664cf34f698c139b02b92322118366e929c29",
}

OOS_LOCK_CUTOFF_UTC = pd.Timestamp("2022-01-01 00:00:00")


def calc_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_gate1_integrity(df12: pd.DataFrame, df27: pd.DataFrame) -> dict:
    u12 = int((df12.astype(str) == "unknown").sum().sum())
    u27 = int((df27.astype(str) == "unknown").sum().sum())
    if u12 > 0 or u27 > 0:
        raise AssertionError(f"Gate 1 FAIL: 'unknown' cells found (csv12={u12}, csv27={u27}).")
    uniq_wicks = int(df27["wick_rejection_ratio"].nunique())
    if uniq_wicks <= 10:
        raise AssertionError(f"Gate 1 FAIL: Proxy constants suspected (unique wick ratios={uniq_wicks}).")
    bad_rng = int((df27["pre_15m_range_pips"] < df27["pre_15m_body_pips"] - 1e-9).sum())
    if bad_rng > 0:
        raise AssertionError(f"Gate 1 FAIL: {bad_rng} rows violate pre_15m_range_pips >= pre_15m_body_pips.")
    grade_counts = df27["wick_rejection_grade"].value_counts().to_dict()
    if grade_counts.get("PURE_STRONG") != 360 or grade_counts.get("WEAK_SUB") != 201 or grade_counts.get("NONE") != 616:
        raise AssertionError(f"Gate 1 FAIL: Unexpected grade counts: {grade_counts}")
    return {
        "total_rows": int(len(df27)),
        "unknown_cells_csv12": u12,
        "unknown_cells_csv27": u27,
        "unique_wick_ratios": uniq_wicks,
        "range_ge_body_violations": bad_rng,
        "counts": {
            "PURE_STRONG": int(grade_counts["PURE_STRONG"]),
            "WEAK_SUB": int(grade_counts["WEAK_SUB"]),
            "NONE": int(grade_counts["NONE"]),
        },
        "win_loss_label_masked": bool((df27["win_loss_label"] == "HOLD_LABEL_FREE").all()),
        "net_pips_result_masked": bool((df27["net_pips_result"] == "HOLD_LABEL_FREE").all()),
    }


def load_is_m1_open_prices(csv_path: Path) -> dict:
    """Scan 00:55 and 01:00 UTC M1 Open prices strictly within IS (2015-2021), blocking 2022+ OOS."""
    open_lookup = {}
    with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
        for ln in f:
            if not ln or ln[0] not in "12":
                continue
            p = [x.strip() for x in ln.split(",")]
            if " " in p[0]:
                dt_part, tm_part, o_idx = p[0].split()[0], p[0].split()[1], 1
            else:
                dt_part, tm_part, o_idx = p[0], p[1], 2
            yr = dt_part[:4]
            if yr < "2015" or yr > "2021":
                continue
            hm = ("0" + tm_part if tm_part[1] == ":" else tm_part)[:5]
            if hm in ("00:55", "01:00"):
                d_iso = dt_part.replace(".", "-").replace("/", "-")
                open_lookup[f"{d_iso} {hm}:00"] = float(p[o_idx])
    return open_lookup


def hac_metrics_from_wins(wins: np.ndarray, max_lag: int = 5) -> dict:
    n = int(len(wins))
    if n == 0:
        return {
            "n": 0, "wins": 0, "losses": 0, "win_rate_pct": 0.0,
            "ev": -1.0, "se_hac": 0.0, "clb975_ev": -1.0, "clb975_wr_pct": 0.0,
            "t_stat": 0.0, "exceeds_be": False, "clb_positive": False
        }
    w_cnt = int(np.sum(wins))
    l_cnt = n - w_cnt
    wr = float(w_cnt / n)
    payoffs = np.where(wins == 1, PAYOUT, -1.0)
    ev = float(np.mean(payoffs))
    if n < 10:
        return {
            "n": n, "wins": w_cnt, "losses": l_cnt, "win_rate_pct": round(wr * 100.0, 4),
            "ev": round(ev, 6), "se_hac": 0.0, "clb975_ev": -1.0, "clb975_wr_pct": 0.0,
            "t_stat": 0.0, "exceeds_be": bool(wr > BREAKEVEN_WR), "clb_positive": False
        }
    u = payoffs - ev
    gamma0 = float(np.dot(u, u) / n)
    var_hac = gamma0
    L = min(max_lag, n - 1)
    for lag in range(1, L + 1):
        w = 1.0 - lag / (L + 1.0)
        cov = float(np.dot(u[lag:], u[:-lag]) / n)
        var_hac += 2.0 * w * cov
    var_hac = max(var_hac * (n / max(n - 1, 1)), 1e-12)
    se_ev = float(np.sqrt(var_hac / n))
    clb_ev = float(ev - 1.959964 * se_ev)
    t_stat = float(ev / se_ev) if se_ev > 0 else 0.0
    clb_wr = (clb_ev + 1.0) / (1.0 + PAYOUT)
    return {
        "n": n, "wins": w_cnt, "losses": l_cnt,
        "win_rate_pct": round(wr * 100.0, 4),
        "ev": round(ev, 6),
        "se_hac": round(se_ev, 6),
        "clb975_ev": round(clb_ev, 6),
        "clb975_wr_pct": round(clb_wr * 100.0, 4),
        "t_stat": round(t_stat, 4),
        "exceeds_be": bool(wr > BREAKEVEN_WR),
        "clb_positive": bool(clb_ev > 0.0),
    }


def evaluate_slice(df_sub: pd.DataFrame, exp_tag: str, dimension: str, slice_label: str, ctrl_wr01: float, ctrl_ev01: float) -> dict:
    m0 = hac_metrics_from_wins(df_sub["win_00pip"].to_numpy())
    m1 = hac_metrics_from_wins(df_sub["win_01pip"].to_numpy())
    m2 = hac_metrics_from_wins(df_sub["win_02pip"].to_numpy())
    m3 = hac_metrics_from_wins(df_sub["win_03pip"].to_numpy())
    med_pips = round(float(df_sub["signed_move_pips"].median()), 4) if len(df_sub) > 0 else 0.0
    return {
        "case_id": TARGET_CANDIDATE_ID,
        "symbol": SYMBOL,
        "experiment": exp_tag,
        "dimension": dimension,
        "slice_value": slice_label,
        "n_valid": m1["n"],
        "wins_00pip": m0["wins"],
        "wr_00pip_pct": m0["win_rate_pct"],
        "ev_00pip": m0["ev"],
        "wins_01pip": m1["wins"],
        "losses_01pip": m1["losses"],
        "wr_01pip_pct": m1["win_rate_pct"],
        "ev_01pip": m1["ev"],
        "se_hac_01pip": m1["se_hac"],
        "clb975_ev_01pip": m1["clb975_ev"],
        "clb975_wr_01pip_pct": m1["clb975_wr_pct"],
        "t_stat_01pip": m1["t_stat"],
        "wins_02pip": m2["wins"],
        "wr_02pip_pct": m2["win_rate_pct"],
        "ev_02pip": m2["ev"],
        "clb975_ev_02pip": m2["clb975_ev"],
        "wins_03pip": m3["wins"],
        "wr_03pip_pct": m3["win_rate_pct"],
        "ev_03pip": m3["ev"],
        "clb975_ev_03pip": m3["clb975_ev"],
        "median_signed_move_pips": med_pips,
        "ablation_wr01_vs_none_pctpt": round(m1["win_rate_pct"] - ctrl_wr01, 4),
        "ablation_ev01_vs_none": round(m1["ev"] - ctrl_ev01, 6),
        "exceeds_be_01pip": m1["exceeds_be"],
        "clb_positive_01pip": m1["clb_positive"],
        "exceeds_be_02pip": m2["exceeds_be"],
        "exceeds_be_03pip": m3["exceeds_be"],
    }


def main() -> None:
    gov_v12_path = STAGE1_DIR / "MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md"
    if not gov_v12_path.exists():
        gov_v12_path = STAGE1_DIR.parent / "MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md"
    s1_py_path = STAGE1_DIR / "profile_is_market_structure_gsr_2026w48_v1_0.py"
    csv12_path = STAGE1_DIR / "is_2015_2021_opportunity_ledger_gsr_2026w48.csv"
    csv27_path = STAGE1_DIR / "is_2015_2021_opportunity_ledger_gsr_2026w48_masked_v22.csv"
    s1_man_path = STAGE1_DIR / "stage1_to_stage2_handover_manifest_gsr_2026w48.json"

    actual_hashes = {
        "governance_v12": calc_sha256(gov_v12_path),
        "stage1_py": calc_sha256(s1_py_path),
        "csv12": calc_sha256(csv12_path),
        "csv27": calc_sha256(csv27_path),
        "stage1_manifest": calc_sha256(s1_man_path),
        "raw_m1": calc_sha256(RAW_M1_PATH),
    }
    for k, exp_h in EXPECTED_SHA256.items():
        if actual_hashes[k] != exp_h:
            raise RuntimeError(f"Gate 1 SHA256 Mismatch on {k}: actual={actual_hashes[k]} != expected={exp_h}")

    df12 = pd.read_csv(csv12_path)
    df27 = pd.read_csv(csv27_path)
    gate1_info = verify_gate1_integrity(df12, df27)

    df27["entry_dt_utc"] = pd.to_datetime(df27["expected_entry_utc"])
    df27["expiry_dt_utc"] = pd.to_datetime(df27["expected_expiry_utc"])
    if df27["entry_dt_utc"].max() >= OOS_LOCK_CUTOFF_UTC:
        raise RuntimeError("Gate 1 FAIL: OOS timestamp detected in ledger!")

    open_lookup = load_is_m1_open_prices(RAW_M1_PATH)
    df27["entry_open"] = df27["expected_entry_utc"].map(open_lookup)
    df27["expiry_open"] = df27["expected_expiry_utc"].map(open_lookup)

    valid = df27[(df27["continuity_6bar_status"] == "PASS") & df27["entry_open"].notna() & df27["expiry_open"].notna()].copy()
    valid = valid.sort_values("entry_dt_utc").reset_index(drop=True)

    dir_sign = np.where(valid["direction"] == "SELL", -1.0, 1.0)
    valid["signed_move_pips"] = np.round((valid["expiry_open"] - valid["entry_open"]) * dir_sign / PIP_SIZE, 4)
    for fp, col in [(0.0, "win_00pip"), (0.1, "win_01pip"), (0.2, "win_02pip"), (0.3, "win_03pip")]:
        valid[col] = (valid["signed_move_pips"] > fp + 1e-9).astype(int)

    valid["year"] = valid["entry_dt_utc"].dt.year

    # Baseline NONE (CONTROL_ONLY)
    none_df = valid[valid["wick_rejection_grade"] == "NONE"]
    weak_df = valid[valid["wick_rejection_grade"] == "WEAK_SUB"]
    pure_df = valid[valid["wick_rejection_grade"] == "PURE_STRONG"].copy()
    cand_df = valid[valid["cohort_role"] == "CANDIDATE"]

    none_m1 = hac_metrics_from_wins(none_df["win_01pip"].to_numpy())
    ctrl_wr01, ctrl_ev01 = none_m1["win_rate_pct"], none_m1["ev"]

    # 1. Standalone & Experiment A Ablation Summary
    standalone_rows = [
        evaluate_slice(valid, "BASELINE", "cohort", "ALL_POOLED (n=1177)", ctrl_wr01, ctrl_ev01),
        evaluate_slice(none_df, "EXPERIMENT_A", "wick_rejection_grade", "NONE (CONTROL_ONLY, n=616)", ctrl_wr01, ctrl_ev01),
        evaluate_slice(cand_df, "BASELINE", "cohort", "CANDIDATE_ALL (PURE_STRONG+WEAK_SUB, n=561)", ctrl_wr01, ctrl_ev01),
        evaluate_slice(weak_df, "EXPERIMENT_A", "wick_rejection_grade", "WEAK_SUB (0 <= wick < 0.25, n=201)", ctrl_wr01, ctrl_ev01),
        evaluate_slice(pure_df, "EXPERIMENT_A", "wick_rejection_grade", "PURE_STRONG (wick >= 0.25, n=360)", ctrl_wr01, ctrl_ev01),
        evaluate_slice(pure_df[(pure_df["wick_rejection_ratio"] >= 0.25) & (pure_df["wick_rejection_ratio"] < 0.40)], "EXPERIMENT_A_DISJOINT", "wick_interval", "[0.25, 0.40) (B2_0.25_0.40, n=97)", ctrl_wr01, ctrl_ev01),
        evaluate_slice(pure_df[(pure_df["wick_rejection_ratio"] >= 0.40) & (pure_df["wick_rejection_ratio"] < 0.55)], "EXPERIMENT_A_DISJOINT", "wick_interval", "[0.40, 0.55) (B3_0.40_0.55, n=135)", ctrl_wr01, ctrl_ev01),
        evaluate_slice(pure_df[pure_df["wick_rejection_ratio"] >= 0.55], "EXPERIMENT_A_DISJOINT", "wick_interval", "[0.55, 1.00] (B4_0.55_up, n=128)", ctrl_wr01, ctrl_ev01),
        evaluate_slice(pure_df[pure_df["wick_rejection_ratio"] >= 0.40], "EXPERIMENT_A_HIGH_WICK", "wick_interval", "HIGH_WICK (wick >= 0.40, n=263)", ctrl_wr01, ctrl_ev01),
    ]

    # 2. Non-Cumulative Marginals & Yearly Breakdown (Experiments A, B, C)
    marginal_rows = []
    # Experiment A Disjoint Wick Bins
    for b3, grp in cand_df.groupby("bin_axis_3_wick_ratio"):
        marginal_rows.append(evaluate_slice(grp, "EXP_A_WICK_DISJOINT", "bin_axis_3_wick_ratio", str(b3), ctrl_wr01, ctrl_ev01))

    # Experiment B: Non-cumulative pre_15m_body_pips and pre_15m_range_pips on PURE_STRONG (n=360)
    pure_df["body_disjoint_bin"] = pd.cut(
        pure_df["pre_15m_body_pips"],
        bins=[0.0, 3.0, 4.5, 7.0, 999.0],
        right=False,
        labels=["B1_body_lt_3.0p", "B2_body_3.0_4.5p", "B3_body_4.5_7.0p", "B4_body_ge_7.0p"]
    )
    for b_lbl, grp in pure_df.groupby("body_disjoint_bin", observed=False):
        marginal_rows.append(evaluate_slice(grp, "EXP_B_PRE15M_BODY_DISJOINT", "pre_15m_body_pips", str(b_lbl), ctrl_wr01, ctrl_ev01))

    pure_df["range_disjoint_bin"] = pd.cut(
        pure_df["pre_15m_range_pips"],
        bins=[0.0, 6.0, 9.0, 13.0, 999.0],
        right=False,
        labels=["B1_range_lt_6.0p", "B2_range_6.0_9.0p", "B3_range_9.0_13.0p", "B4_range_ge_13.0p"]
    )
    for r_lbl, grp in pure_df.groupby("range_disjoint_bin", observed=False):
        marginal_rows.append(evaluate_slice(grp, "EXP_B_PRE15M_RANGE_DISJOINT", "pre_15m_range_pips", str(r_lbl), ctrl_wr01, ctrl_ev01))

    for b1, grp in pure_df.groupby("bin_axis_1_move15m_atr"):
        marginal_rows.append(evaluate_slice(grp, "EXP_B_MOVE15M_ATR_DISJOINT", "bin_axis_1_move15m_atr", str(b1), ctrl_wr01, ctrl_ev01))
    for b2, grp in pure_df.groupby("bin_axis_2_atr14"):
        marginal_rows.append(evaluate_slice(grp, "EXP_B_ATR14_DISJOINT", "bin_axis_2_atr14", str(b2), ctrl_wr01, ctrl_ev01))

    # Experiment C: Coarse Disjoint Slices on PURE_STRONG (n=360)
    for d_val in ["SELL", "BUY"]:
        marginal_rows.append(evaluate_slice(pure_df[pure_df["direction"] == d_val], "EXP_C_DIRECTION", "direction", d_val, ctrl_wr01, ctrl_ev01))
    for g_val in [1, 0]:
        marginal_rows.append(evaluate_slice(pure_df[pure_df["gotobi_flag"] == g_val], "EXP_C_GOTOBI", "gotobi_flag", f"gotobi_{g_val}", ctrl_wr01, ctrl_ev01))
    dow_names = {0: "0_Mon", 1: "1_Tue", 2: "2_Wed", 3: "3_Thu", 4: "4_Fri"}
    for dow_k, dow_lbl in dow_names.items():
        marginal_rows.append(evaluate_slice(pure_df[pure_df["day_of_week"] == dow_k], "EXP_C_DAY_OF_WEEK", "day_of_week", dow_lbl, ctrl_wr01, ctrl_ev01))

    pure_df["atr_regime_2p"] = np.where(pure_df["atr14_pips"] < 2.0, "ATR14_lt_2.0p", "ATR14_ge_2.0p")
    for ar_lbl in ["ATR14_lt_2.0p", "ATR14_ge_2.0p"]:
        marginal_rows.append(evaluate_slice(pure_df[pure_df["atr_regime_2p"] == ar_lbl], "EXP_C_ATR_REGIME", "atr14_2.0p_split", ar_lbl, ctrl_wr01, ctrl_ev01))

    for yr in sorted(pure_df["year"].unique()):
        marginal_rows.append(evaluate_slice(pure_df[pure_df["year"] == yr], "EXP_C_YEARLY_PURE_STRONG", "year", str(yr), ctrl_wr01, ctrl_ev01))
    for yr in sorted(cand_df["year"].unique()):
        marginal_rows.append(evaluate_slice(cand_df[cand_df["year"] == yr], "EXP_C_YEARLY_CANDIDATE_ALL", "year", str(yr), ctrl_wr01, ctrl_ev01))

    ts_str = datetime.now(JST).strftime("%Y%m%d_%H%M%S")
    out_dir = STAGE2_DIR / f"output_gsr_2026w48_is_tkyfix002_{ts_str}"
    out_dir.mkdir(parents=True, exist_ok=True)

    sa_csv = out_dir / "is_standalone_and_ablation_summary_gsr_2026w48.csv"
    mg_csv = out_dir / "is_non_cumulative_marginals_and_yearly_gsr_2026w48.csv"
    pd.DataFrame(standalone_rows).to_csv(sa_csv, index=False, encoding="utf-8")
    pd.DataFrame(marginal_rows).to_csv(mg_csv, index=False, encoding="utf-8")

    (STAGE2_DIR / sa_csv.name).write_bytes(sa_csv.read_bytes())
    (STAGE2_DIR / mg_csv.name).write_bytes(mg_csv.read_bytes())

    manifest = {
        "schema_version": "2.2",
        "pipeline_case_id": PIPELINE_CASE_ID,
        "record_id": RECORD_ID,
        "evaluated_candidate_id": TARGET_CANDIDATE_ID,
        "parent_candidate_id": PARENT_CANDIDATE_ID,
        "script_version": SCRIPT_VERSION,
        "generated_at_jst": datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S"),
        "verification_status": "LOCAL_FULL_258MB_VERIFIED",
        "gate1_audit": {
            "confirmed_sha256": actual_hashes,
            "sha256_all_match": True,
            "oos_locked": True,
            "ledger_integrity": gate1_info,
        },
        "output_files": {
            "output_dir": out_dir.name,
            "verifier_script": Path(__file__).name,
            "verifier_script_sha256": calc_sha256(Path(__file__)),
            "standalone_csv": sa_csv.name,
            "standalone_sha256": calc_sha256(sa_csv),
            "marginals_yearly_csv": mg_csv.name,
            "marginals_yearly_sha256": calc_sha256(mg_csv),
        },
        "standalone_summary": standalone_rows,
    }
    man_path = out_dir / "spark_audit_handover_manifest_gsr_2026w48.json"
    man_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (STAGE2_DIR / "spark_audit_handover_manifest_gsr_2026w48.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
