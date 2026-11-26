#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GSR-2026W49 STAGE 2: TRACK A (GSR-TKYFIX-002 ONE-SHOT OOS) & TRACK B (MULTI-FIX IS) VERIFIER (v1.0.0)
Pipeline Case ID : GSR-2026W49 (Stage 2 Record ID: GSR-202611-W5-WED)
Governance       : MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md (SHA256: 0caca9b9759cc28dfad5a50ef3952f2fac9b868d933b68b11d5592b36345dae9)

Enforced Verification Contract:
  1. Gate 1: Exact SHA256 verification of all 8 canonical input files (governance v1.2, stage1 script,
     Track A OOS ledger, Track B IS ledger, exclusions log, and 3 raw M1 CSVs: USDJPY/EURUSD/GBPUSD).
     Strictly exclude FAIL_GAP_T+6 (1 row in GSR-NYCUT-001|USDJPY) so Track B evaluates exactly 5,532 PASS rows.
  2. Gate 2, 4, 5: Open[t+1] entry -> Open[t+6] strict 300s expiry, Tie (Draw) = LOSE, Payout = 1.85
     (Breakeven WR = 54.054054%), +0.0 / +0.1 / +0.2 / +0.3 pip adverse spread friction, median signed move (pips),
     Newey-West HAC (Bartlett kernel, max_lag=5) SE_HAC & 97.5% one-sided CLB (both Normal z=1.959964 and Student-t df=n-1).
  3. Track A (Authorized One-Shot OOS 2022-01-02..2026-10-15 for GSR-TKYFIX-002 ONLY):
     - Primary Contract: PURE_STRONG (n=256, SELL+BUY pooled) vs NONE (n=428) & WEAK_SUB (n=90)
     - Pre-Registered Diagnostics: Direction, Gotobi, Day of Week, ATR (<2.0p vs >=2.0p), Year (2022..2026),
       Non-cumulative 3 wick bins ([0.25,0.40), [0.40,0.55), [0.55,1.00]), Covariate Shift (IS vs OOS),
       and Practical Baseline Capital Simulation (Init 50,000 JPY, Fixed 1,000 JPY stake, No Martingale, DD<=25% check).
  4. Track B (Strict IS 2015-2021 ONLY, oos_locked_for_track_b=True):
     - GSR-TKYFIX-003 (USDJPY, n=1,173): Non-cumulative Q1..Q4 quartiles for eta_range, theta_peak, psi_reject, phi_urp
       + phi_urp Q1..Q4 monotonicity within PURE_STRONG (n=359).
     - GSR-LDNFIX-001 (EURUSD n=1,127 / GBPUSD n=1,157) & GSR-NYCUT-001 (USDJPY n=1,027 / EURUSD n=1,048):
       Standalone/Ablation, phi_urp Q1..Q4, DST regime (BST/EDT vs GMT/EST), Direction, Yearly (2015..2021).
"""

import hashlib
import json
import math
from pathlib import Path
from datetime import datetime, timezone, timedelta
import numpy as np
import pandas as pd

try:
    from scipy.stats import t as student_t
except Exception:
    student_t = None

SCRIPT_VERSION = "1.0.0"
PIPELINE_CASE_ID = "GSR-2026W49"
RECORD_ID = "GSR-202611-W5-WED"
PAYOUT = 0.85
BREAKEVEN_WR = 1.0 / (1.0 + PAYOUT)  # 0.5405405405...
Z_975 = 1.959963984540054
JST = timezone(timedelta(hours=9))

BASE_DRIVE = Path(r"G:\マイドライブ")
PIPELINE_ROOT = BASE_DRIVE / r"AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告"
STAGE1_DIR = PIPELINE_ROOT / r"トレード手法の市場調査＆データ点検"
STAGE2_DIR = PIPELINE_ROOT / r"機会台帳突合＆IS統計・Plateau検証"
M1_DIR = BASE_DRIVE / r"通貨ペア\Dukascopy 1分足"

M1_SPECS = {
    "USDJPY": (M1_DIR / "USDJPY" / "2026.10.16USDJPY(3)-M1-No Session.csv", 0.01, "aa778785e1a0210a17b5a9c8198664cf34f698c139b02b92322118366e929c29"),
    "EURUSD": (M1_DIR / "EURUSD" / "2026.10.16EURUSD(5)-M1-No Session.csv", 0.0001, "029bc12ccd4b244173cd9ed294c7dc8ec9f9b61cfd4499544722179158433a4d"),
    "GBPUSD": (M1_DIR / "GBPUSD" / "2026.10.16GBPUSD(3)-M1-No Session.csv", 0.0001, "05468aa45b7e08a47fa7aff608af1d08d190fd6b5298534585f9c9554e7ab803"),
}

EXPECTED_SHA256 = {
    "governance_v12": "0caca9b9759cc28dfad5a50ef3952f2fac9b868d933b68b11d5592b36345dae9",
    "stage1_py": "f4609b51f933c21bbf8db3e2f54095ee728cd6571d805b3df04531c386fb364b",
    "track_a_oos_csv": "3e5c583f8b8bb5bef00846c2048c90716cb01f071d2591b65998549359758d68",
    "track_b_is_csv": "0272871721a3e96b6ace75afaa72e13708c8d398355a2cc971459d8cdec1a1c1",
    "exclusions_csv": "951cd609d678ff05dc4a1b62daf398f0bd89966e80e8bcd29a130d835a149757",
    "raw_m1_usdjpy": M1_SPECS["USDJPY"][2],
    "raw_m1_eurusd": M1_SPECS["EURUSD"][2],
    "raw_m1_gbpusd": M1_SPECS["GBPUSD"][2],
}


def calc_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def t_crit_975(df_val: int) -> float:
    if df_val <= 1:
        return 12.706204736432095
    if student_t is not None:
        return float(student_t.ppf(0.975, df=df_val))
    # Cornish-Fisher approximation for t_{0.975, df} if scipy is unavailable
    z = Z_975
    g1 = (z**3 + z) / (4.0 * df_val)
    g2 = (5.0 * z**5 + 16.0 * z**3 + 3.0 * z) / (96.0 * (df_val**2))
    return float(z + g1 + g2)


def load_open_prices(csv_path: Path, target_utc_strs: set, allow_oos: bool) -> dict:
    """Scan M1 Open prices for target timestamps only; physically block 2022+ when allow_oos=False."""
    lookup = {}
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
            if yr < "2015":
                continue
            if not allow_oos and yr >= "2022":
                continue
            d_iso = dt_part.replace(".", "-").replace("/", "-")
            hm = ("0" + tm_part if tm_part[1] == ":" else tm_part)[:5]
            ts_key = f"{d_iso} {hm}:00"
            if ts_key in target_utc_strs:
                lookup[ts_key] = float(p[o_idx])
    return lookup


def hac_metrics(wins: np.ndarray, max_lag: int = 5) -> dict:
    n = int(len(wins))
    if n == 0:
        return {
            "n": 0, "wins": 0, "losses": 0, "wr_pct": 0.0, "ev": -1.0,
            "se_hac": 0.0, "clb975_norm": -1.0, "clb975_t": -1.0, "t_stat": 0.0,
            "exceeds_be": False, "clb_norm_pos": False, "clb_t_pos": False,
        }
    w_cnt = int(np.sum(wins))
    l_cnt = n - w_cnt
    wr = float(w_cnt / n)
    payoffs = np.where(wins == 1, PAYOUT, -1.0)
    ev = float(np.mean(payoffs))
    if n < 5:
        return {
            "n": n, "wins": w_cnt, "losses": l_cnt, "wr_pct": round(wr * 100.0, 4),
            "ev": round(ev, 6), "se_hac": 0.0, "clb975_norm": -1.0, "clb975_t": -1.0,
            "t_stat": 0.0, "exceeds_be": bool(wr > BREAKEVEN_WR),
            "clb_norm_pos": False, "clb_t_pos": False,
        }
    u = payoffs - ev
    gamma0 = float(np.dot(u, u) / n)
    var_hac = gamma0
    L = min(max_lag, n - 1)
    for lag in range(1, L + 1):
        wt = 1.0 - lag / (L + 1.0)
        cov = float(np.dot(u[lag:], u[:-lag]) / n)
        var_hac += 2.0 * wt * cov
    var_hac = max(var_hac * (n / max(n - 1, 1)), 1e-12)
    se_ev = float(np.sqrt(var_hac / n))
    clb_norm = float(ev - Z_975 * se_ev)
    tc = t_crit_975(n - 1)
    clb_t = float(ev - tc * se_ev)
    t_stat = float(ev / se_ev) if se_ev > 0 else 0.0
    return {
        "n": n, "wins": w_cnt, "losses": l_cnt,
        "wr_pct": round(wr * 100.0, 4),
        "ev": round(ev, 6),
        "se_hac": round(se_ev, 6),
        "clb975_norm": round(clb_norm, 6),
        "clb975_t": round(clb_t, 6),
        "t_stat": round(t_stat, 4),
        "exceeds_be": bool(wr > BREAKEVEN_WR),
        "clb_norm_pos": bool(clb_norm > 0.0),
        "clb_t_pos": bool(clb_t > 0.0),
    }


def simulate_capital(wins: np.ndarray, init_cap: float = 50000.0, stake: float = 1000.0) -> dict:
    bal = init_cap
    peak = init_cap
    max_dd_pct = 0.0
    max_dd_jpy = 0.0
    cur_loss_streak = 0
    max_loss_streak = 0
    for w in wins:
        if w == 1:
            bal += stake * PAYOUT
            cur_loss_streak = 0
        else:
            bal -= stake
            cur_loss_streak += 1
            if cur_loss_streak > max_loss_streak:
                max_loss_streak = cur_loss_streak
        if bal > peak:
            peak = bal
        dd_jpy = peak - bal
        dd_pct = (dd_jpy / peak) * 100.0 if peak > 0 else 0.0
        if dd_pct > max_dd_pct:
            max_dd_pct = dd_pct
        if dd_jpy > max_dd_jpy:
            max_dd_jpy = dd_jpy
    return {
        "init_capital_jpy": round(init_cap, 2),
        "stake_jpy": round(stake, 2),
        "final_balance_jpy": round(bal, 2),
        "net_profit_jpy": round(bal - init_cap, 2),
        "max_dd_jpy": round(max_dd_jpy, 2),
        "max_dd_pct": round(max_dd_pct, 4),
        "dd_within_25pct": bool(max_dd_pct <= 25.0),
        "max_consecutive_losses": int(max_loss_streak),
    }


def eval_subset(df_sub: pd.DataFrame, track: str, cid: str, sym: str, section: str, dim: str, slc: str, ctrl_wr01: float, ctrl_ev01: float) -> dict:
    m0 = hac_metrics(df_sub["win_00pip"].to_numpy())
    m1 = hac_metrics(df_sub["win_01pip"].to_numpy())
    m2 = hac_metrics(df_sub["win_02pip"].to_numpy())
    m3 = hac_metrics(df_sub["win_03pip"].to_numpy())
    med_pips = round(float(df_sub["signed_move_pips"].median()), 4) if len(df_sub) > 0 else 0.0
    return {
        "track": track, "case_id": cid, "symbol": sym, "section": section,
        "dimension": dim, "slice_value": slc, "n_valid": m1["n"],
        "wr_00pip_pct": m0["wr_pct"], "ev_00pip": m0["ev"],
        "wins_01pip": m1["wins"], "losses_01pip": m1["losses"],
        "wr_01pip_pct": m1["wr_pct"], "ev_01pip": m1["ev"],
        "se_hac_01pip": m1["se_hac"],
        "clb975_norm_01pip": m1["clb975_norm"], "clb975_t_01pip": m1["clb975_t"],
        "t_stat_01pip": m1["t_stat"],
        "wr_02pip_pct": m2["wr_pct"], "ev_02pip": m2["ev"],
        "clb975_norm_02pip": m2["clb975_norm"], "clb975_t_02pip": m2["clb975_t"],
        "wr_03pip_pct": m3["wr_pct"], "ev_03pip": m3["ev"],
        "clb975_norm_03pip": m3["clb975_norm"], "clb975_t_03pip": m3["clb975_t"],
        "median_signed_move_pips": med_pips,
        "ablation_wr01_vs_none_pctpt": round(m1["wr_pct"] - ctrl_wr01, 4),
        "ablation_ev01_vs_none": round(m1["ev"] - ctrl_ev01, 6),
        "exceeds_be_01pip": m1["exceeds_be"],
        "clb_norm_pos_01pip": m1["clb_norm_pos"],
        "clb_t_pos_01pip": m1["clb_t_pos"],
    }


def score_df(df: pd.DataFrame, open_lookup: dict, pip_size: float) -> pd.DataFrame:
    sub = df.copy()
    sub["entry_open"] = sub["expected_entry_utc"].map(open_lookup)
    sub["expiry_open"] = sub["expected_expiry_utc"].map(open_lookup)
    valid = sub[(sub["m1_continuity_pass"] == True) & (sub["continuity_6bar_status"] == "PASS_6BAR_COMPLETE") & sub["entry_open"].notna() & sub["expiry_open"].notna()].copy()
    valid = valid.sort_values("expected_entry_utc").reset_index(drop=True)
    dir_sign = np.where(valid["direction"] == "SELL", -1.0, 1.0)
    valid["signed_move_pips"] = np.round((valid["expiry_open"] - valid["entry_open"]) * dir_sign / pip_size, 4)
    for fp, col in [(0.0, "win_00pip"), (0.1, "win_01pip"), (0.2, "win_02pip"), (0.3, "win_03pip")]:
        valid[col] = (valid["signed_move_pips"] > fp + 1e-9).astype(int)
    valid["year"] = valid["trade_date"].str[:4]
    return valid


def assign_disjoint_quartiles(series: pd.Series) -> pd.Series:
    """Assign non-cumulative Q1..Q4 quartiles robustly even when ties (e.g. theta_peak==0) occur."""
    try:
        bins = pd.qcut(series, q=4, duplicates="drop")
        labels = [f"Q{i+1}_{str(c)}" for i, c in enumerate(bins.cat.categories)]
        return bins.cat.rename_categories(labels).astype(str)
    except Exception:
        ranks = series.rank(method="first")
        return pd.qcut(ranks, q=4, labels=["Q1", "Q2", "Q3", "Q4"]).astype(str)


def main() -> None:
    gov_p = STAGE1_DIR / "MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md"
    if not gov_p.exists():
        gov_p = PIPELINE_ROOT / "MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md"

    paths = {
        "governance_v12": gov_p,
        "stage1_py": STAGE1_DIR / "profile_market_structure_gsr_2026w49_v1_0.py",
        "track_a_oos_csv": STAGE1_DIR / "oos_2022_2026_opportunity_ledger_gsr_tkyfix002_gsr_2026w49.csv",
        "track_b_is_csv": STAGE1_DIR / "is_2015_2021_opportunity_ledger_multifix_gsr_2026w49.csv",
        "exclusions_csv": STAGE1_DIR / "exclusions_log_gsr_2026w49.csv",
        "raw_m1_usdjpy": M1_SPECS["USDJPY"][0],
        "raw_m1_eurusd": M1_SPECS["EURUSD"][0],
        "raw_m1_gbpusd": M1_SPECS["GBPUSD"][0],
    }

    print("[1/5] Gate 1: Verifying SHA256 hashes of all 8 canonical input files...")
    actual_sha = {}
    for k, p in paths.items():
        if not p.exists():
            raise FileNotFoundError(f"Gate 1 FAIL: Missing file {k} at {p}")
        h = calc_sha256(p)
        actual_sha[k] = h
        if h != EXPECTED_SHA256[k]:
            raise RuntimeError(f"Gate 1 SHA256 MISMATCH on {k}: actual={h} != expected={EXPECTED_SHA256[k]}")
        print(f"  EXACT MATCH | {k:16s} | {h}")

    df_oos_raw = pd.read_csv(paths["track_a_oos_csv"])
    df_is_raw = pd.read_csv(paths["track_b_is_csv"])
    df_ex_raw = pd.read_csv(paths["exclusions_csv"])

    if len(df_oos_raw) != 774 or len(df_is_raw) != 5533 or len(df_ex_raw) != 66:
        raise RuntimeError(f"Gate 1 Row Count Mismatch: OOS={len(df_oos_raw)}, IS={len(df_is_raw)}, EX={len(df_ex_raw)}")
    if df_is_raw["expected_entry_utc"].max() >= "2022-01-01 00:00:00":
        raise RuntimeError("CRITICAL Gate 1 FAIL: OOS timestamp found in Track B IS ledger!")

    print("[2/5] Scanning Raw M1 Open[t+1] & Open[t+6] prices (Track B strictly IS-only; Track A USDJPY One-Shot OOS)...")
    is_opens = {}
    for sym, (m1_p, _, _) in M1_SPECS.items():
        t_set = set(df_is_raw[df_is_raw["symbol"] == sym]["expected_entry_utc"]).union(
            set(df_is_raw[df_is_raw["symbol"] == sym]["expected_expiry_utc"])
        )
        is_opens[sym] = load_open_prices(m1_p, t_set, allow_oos=False)

    oos_t_set = set(df_oos_raw["expected_entry_utc"]).union(set(df_oos_raw["expected_expiry_utc"]))
    oos_opens_usdjpy = load_open_prices(M1_SPECS["USDJPY"][0], oos_t_set, allow_oos=True)

    # ==========================================================================
    # [3/5] TRACK A: GSR-TKYFIX-002 ONE-SHOT OOS (2022-2026)
    # ==========================================================================
    print("[3/5] Executing Track A: GSR-TKYFIX-002 One-Shot OOS (2022-2026)...")
    oos_v = score_df(df_oos_raw, oos_opens_usdjpy, 0.01)
    assert len(oos_v) == 774, f"Expected 774 OOS PASS rows, got {len(oos_v)}"

    oos_none = oos_v[oos_v["wick_rejection_grade"] == "NONE"]
    oos_weak = oos_v[oos_v["wick_rejection_grade"] == "WEAK_SUB"]
    oos_pure = oos_v[oos_v["wick_rejection_grade"] == "PURE_STRONG"].copy()
    assert len(oos_pure) == 256 and len(oos_none) == 428 and len(oos_weak) == 90

    ctrl_m1 = hac_metrics(oos_none["win_01pip"].to_numpy())
    c_wr, c_ev = ctrl_m1["wr_pct"], ctrl_m1["ev"]

    track_a_rows = [
        eval_subset(oos_v, "TRACK_A_OOS", "GSR-TKYFIX-002", "USDJPY", "PRIMARY_AND_ABLATION", "cohort", "ALL_POOLED (n=774)", c_wr, c_ev),
        eval_subset(oos_none, "TRACK_A_OOS", "GSR-TKYFIX-002", "USDJPY", "PRIMARY_AND_ABLATION", "cohort", "NONE (CONTROL_ONLY, n=428)", c_wr, c_ev),
        eval_subset(oos_weak, "TRACK_A_OOS", "GSR-TKYFIX-002", "USDJPY", "PRIMARY_AND_ABLATION", "cohort", "WEAK_SUB (EXCLUDED_TRAP06, n=90)", c_wr, c_ev),
        eval_subset(oos_pure, "TRACK_A_OOS", "GSR-TKYFIX-002", "USDJPY", "PRIMARY_CONTRACT", "cohort", "PURE_STRONG (PRIMARY_CONTRACT, n=256)", c_wr, c_ev),
    ]

    # Pre-Registered Diagnostics on PURE_STRONG (n=256)
    for d_val in ["SELL", "BUY"]:
        track_a_rows.append(eval_subset(oos_pure[oos_pure["direction"] == d_val], "TRACK_A_OOS", "GSR-TKYFIX-002", "USDJPY", "DIAG_DIRECTION", "direction", d_val, c_wr, c_ev))
    for g_val in [True, False]:
        track_a_rows.append(eval_subset(oos_pure[oos_pure["gotobi_flag"] == g_val], "TRACK_A_OOS", "GSR-TKYFIX-002", "USDJPY", "DIAG_GOTOBI", "gotobi_flag", str(g_val), c_wr, c_ev))
    for dow in ["Mon", "Tue", "Wed", "Thu", "Fri"]:
        track_a_rows.append(eval_subset(oos_pure[oos_pure["day_of_week"] == dow], "TRACK_A_OOS", "GSR-TKYFIX-002", "USDJPY", "DIAG_DOW", "day_of_week", dow, c_wr, c_ev))
    oos_pure["atr_regime"] = np.where(oos_pure["atr14_pips"] < 2.0, "atr14_lt_2.0p", "atr14_ge_2.0p")
    for ar in ["atr14_lt_2.0p", "atr14_ge_2.0p"]:
        track_a_rows.append(eval_subset(oos_pure[oos_pure["atr_regime"] == ar], "TRACK_A_OOS", "GSR-TKYFIX-002", "USDJPY", "DIAG_ATR_REGIME", "atr14_2.0p_split", ar, c_wr, c_ev))
    for yr in ["2022", "2023", "2024", "2025", "2026"]:
        track_a_rows.append(eval_subset(oos_pure[oos_pure["year"] == yr], "TRACK_A_OOS", "GSR-TKYFIX-002", "USDJPY", "DIAG_YEARLY", "year", yr, c_wr, c_ev))
    oos_pure["wick_3bin"] = pd.cut(oos_pure["wick_rejection_ratio"], bins=[0.25, 0.40, 0.55, 1.01], right=False, labels=["[0.25, 0.40)", "[0.40, 0.55)", "[0.55, 1.00]"])
    for wb in ["[0.25, 0.40)", "[0.40, 0.55)", "[0.55, 1.00]"]:
        track_a_rows.append(eval_subset(oos_pure[oos_pure["wick_3bin"] == wb], "TRACK_A_OOS", "GSR-TKYFIX-002", "USDJPY", "DIAG_WICK_DISJOINT", "wick_3bin", wb, c_wr, c_ev))

    # Covariate Shift (IS GSR-TKYFIX-003 PURE_STRONG vs OOS GSR-TKYFIX-002 PURE_STRONG)
    is_tky_pure = df_is_raw[(df_is_raw["case_id"] == "GSR-TKYFIX-003") & (df_is_raw["wick_rejection_grade"] == "PURE_STRONG")]
    cov_shift = {}
    for col in ["atr14_pips", "pre_15m_range_pips", "pre_15m_body_pips", "wick_rejection_ratio"]:
        is_med = float(is_tky_pure[col].median())
        is_iqr = float(is_tky_pure[col].quantile(0.75) - is_tky_pure[col].quantile(0.25))
        oos_med = float(oos_pure[col].median())
        oos_iqr = float(oos_pure[col].quantile(0.75) - oos_pure[col].quantile(0.25))
        cov_shift[col] = {
            "is_median": round(is_med, 4), "is_iqr": round(is_iqr, 4),
            "oos_median": round(oos_med, 4), "oos_iqr": round(oos_iqr, 4),
            "oos_to_is_median_ratio": round(oos_med / is_med, 4) if is_med > 0 else None,
        }

    # Capital Simulation on Track A PURE_STRONG (n=256)
    cap_sim = {
        "friction_01pip": simulate_capital(oos_pure["win_01pip"].to_numpy(), 50000.0, 1000.0),
        "friction_02pip": simulate_capital(oos_pure["win_02pip"].to_numpy(), 50000.0, 1000.0),
    }

    # ==========================================================================
    # [4/5] TRACK B: MULTI-FIX & NEXT-GEN MODELS (IS 2015-2021 ONLY)
    # ==========================================================================
    print("[4/5] Executing Track B: Multi-Fix & Next-Gen Models (IS 2015-2021 ONLY, 5,532 PASS rows)...")
    track_b_sa = []
    track_b_slices = []
    total_b_pass = 0

    for (cid, sym), grp_raw in df_is_raw.groupby(["case_id", "symbol"]):
        pip_sz = M1_SPECS[sym][1]
        scored = score_df(grp_raw, is_opens[sym], pip_sz)
        total_b_pass += len(scored)

        none_g = scored[scored["wick_rejection_grade"] == "NONE"]
        weak_g = scored[scored["wick_rejection_grade"] == "WEAK_SUB"]
        pure_g = scored[scored["wick_rejection_grade"] == "PURE_STRONG"].copy()
        cm1 = hac_metrics(none_g["win_01pip"].to_numpy())
        b_cwr, b_cev = cm1["wr_pct"], cm1["ev"]

        track_b_sa.extend([
            eval_subset(scored, "TRACK_B_IS", cid, sym, "STANDALONE", "cohort", "ALL_POOLED", b_cwr, b_cev),
            eval_subset(none_g, "TRACK_B_IS", cid, sym, "STANDALONE", "cohort", "NONE (CONTROL_ONLY)", b_cwr, b_cev),
            eval_subset(weak_g, "TRACK_B_IS", cid, sym, "STANDALONE", "cohort", "WEAK_SUB", b_cwr, b_cev),
            eval_subset(pure_g, "TRACK_B_IS", cid, sym, "STANDALONE", "cohort", "PURE_STRONG", b_cwr, b_cev),
        ])

        if cid == "GSR-TKYFIX-003":
            for feat in ["eta_range", "theta_peak", "psi_reject", "phi_urp"]:
                scored[f"{feat}_q"] = assign_disjoint_quartiles(scored[feat])
                for q_val, sub_q in scored.groupby(f"{feat}_q"):
                    track_b_slices.append(eval_subset(sub_q, "TRACK_B_IS", cid, sym, f"TKYFIX003_ALL_{feat.upper()}_Q", feat, str(q_val), b_cwr, b_cev))
            pure_g["phi_urp_q"] = assign_disjoint_quartiles(pure_g["phi_urp"])
            for q_val, sub_q in pure_g.groupby("phi_urp_q"):
                track_b_slices.append(eval_subset(sub_q, "TRACK_B_IS", cid, sym, "TKYFIX003_PURE_PHI_URP_Q", "phi_urp_in_pure", str(q_val), b_cwr, b_cev))
        else:
            pure_g["phi_urp_q"] = assign_disjoint_quartiles(pure_g["phi_urp"])
            for q_val, sub_q in pure_g.groupby("phi_urp_q"):
                track_b_slices.append(eval_subset(sub_q, "TRACK_B_IS", cid, sym, "PURE_PHI_URP_Q", "phi_urp_in_pure", str(q_val), b_cwr, b_cev))

        # DST regime, Direction, Yearly on PURE_STRONG for all Track B pairs
        for dz, sub_d in pure_g.groupby("dst_zone"):
            track_b_slices.append(eval_subset(sub_d, "TRACK_B_IS", cid, sym, "DST_REGIME", "dst_zone", str(dz), b_cwr, b_cev))
        for dv in ["SELL", "BUY"]:
            track_b_slices.append(eval_subset(pure_g[pure_g["direction"] == dv], "TRACK_B_IS", cid, sym, "DIRECTION", "direction", dv, b_cwr, b_cev))
        for yr, sub_y in pure_g.groupby("year"):
            track_b_slices.append(eval_subset(sub_y, "TRACK_B_IS", cid, sym, "YEARLY", "year", str(yr), b_cwr, b_cev))

    assert total_b_pass == 5532, f"Expected 5,532 Track B PASS rows (1 FAIL_GAP_T+6 excluded), got {total_b_pass}"

    # ==========================================================================
    # [5/5] Save Lightweight CSVs (3), Manifest JSON, and Output Summary
    # ==========================================================================
    ts_str = datetime.now(JST).strftime("%Y%m%d_%H%M%S")
    out_dir = STAGE2_DIR / f"output_gsr_2026w49_stage2_{ts_str}"
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_a = out_dir / "oos_tkyfix002_standalone_and_diagnostics_gsr_2026w49.csv"
    csv_b1 = out_dir / "is_multifix_standalone_and_ablation_gsr_2026w49.csv"
    csv_b2 = out_dir / "is_multifix_disjoint_slices_and_yearly_gsr_2026w49.csv"

    pd.DataFrame(track_a_rows).to_csv(csv_a, index=False, encoding="utf-8")
    pd.DataFrame(track_b_sa).to_csv(csv_b1, index=False, encoding="utf-8")
    pd.DataFrame(track_b_slices).to_csv(csv_b2, index=False, encoding="utf-8")

    for f_p in (csv_a, csv_b1, csv_b2):
        (STAGE2_DIR / f_p.name).write_bytes(f_p.read_bytes())

    primary_oos = [r for r in track_a_rows if r["section"] == "PRIMARY_CONTRACT"][0]
    primary_verdict = "OOS_PASS" if (primary_oos["clb_norm_pos_01pip"] and primary_oos["clb_t_pos_01pip"] and primary_oos["wr_02pip_pct"] > BREAKEVEN_WR * 100.0) else "OOS_FAIL_OR_HOLD"

    manifest = {
        "schema_version": "2.2",
        "governance_version": "MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md",
        "pipeline_case_id": PIPELINE_CASE_ID,
        "record_id": RECORD_ID,
        "script_version": SCRIPT_VERSION,
        "generated_at_jst": datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S"),
        "verification_status": "LOCAL_775MB_FULL_VERIFIED",
        "oos_locked_for_track_b": True,
        "oos_authorized_for_track_a_only": True,
        "gate1_audit": {
            "confirmed_8files_sha256": actual_sha,
            "sha256_all_match": True,
            "track_a_oos_rows_pass": int(len(oos_v)),
            "track_b_is_rows_total": int(len(df_is_raw)),
            "track_b_is_rows_pass": int(total_b_pass),
            "track_b_excluded_gap_t6": 1,
        },
        "track_a_oos_primary_contract": {
            "verdict": primary_verdict,
            "metrics": primary_oos,
            "covariate_shift_is_vs_oos_pure_strong": cov_shift,
            "capital_simulation_50k_1k_fixed": cap_sim,
        },
        "track_b_is_standalone_summary": track_b_sa,
        "output_files": {
            "output_dir": out_dir.name,
            "verifier_script": Path(__file__).name,
            "verifier_script_sha256": calc_sha256(Path(__file__)),
            "oos_standalone_diagnostics_csv": csv_a.name,
            "oos_standalone_diagnostics_sha256": calc_sha256(csv_a),
            "is_multifix_standalone_csv": csv_b1.name,
            "is_multifix_standalone_sha256": calc_sha256(csv_b1),
            "is_multifix_disjoint_slices_csv": csv_b2.name,
            "is_multifix_disjoint_slices_sha256": calc_sha256(csv_b2),
        },
    }

    man_path = out_dir / "spark_audit_handover_manifest_gsr_2026w49.json"
    man_text = json.dumps(manifest, ensure_ascii=False, indent=2)
    man_path.write_text(man_text, encoding="utf-8")
    (STAGE2_DIR / "spark_audit_handover_manifest_gsr_2026w49.json").write_text(man_text, encoding="utf-8")

    print("\n[5/5] COMPLETED! Track A OOS Primary Contract Verdict:", primary_verdict)
    print(json.dumps(manifest["track_a_oos_primary_contract"], ensure_ascii=False, indent=2))
    print("Output SHA256s:", json.dumps(manifest["output_files"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
