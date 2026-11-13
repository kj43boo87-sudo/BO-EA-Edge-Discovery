#!/usr/bin/env python3
"""GSR-2026W46 Stage 2: EURUSD-Only IS Statistical Verification & Plateau Analyzer (v1.0).

Purpose:
  Executes Stage 2 ("機会台帳突合＆IS統計・Plateau検証") exclusively for EURUSD
  to minimize token consumption and verify whether any of the 3 Stage-1 candidates
  (GSR-CLIMAX-001, GSR-PULLBACK-001, GSR-FAKEOUT-001) achieves a statistically
  significant edge on In-Sample (2015-2021) before expanding to other pairs.

How to run (Zero arguments required on local PC):
  PS C:\\Users\\kj43b> python "G:\\マイドライブ\\AIトレーサビリティ\\BO・EA Edge Discovery\\Gemini側必勝調査報告\\機会台帳突合＆IS統計・Plateau検証\\gsr_eurusd_is_plateau_verifier_v1_0.py"

Default output location:
  G:\\マイドライブ\\AIトレーサビリティ\\BO・EA Edge Discovery\\Gemini側必勝調査報告\\機会台帳突合＆IS統計・Plateau検証\\output_eurusd_is_plateau_YYYYMMDD_HHMMSS
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import os
import platform
import subprocess
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

# Automatically switch to Python 3.12 codex-primary-runtime if launched from Python 3.14+
CODEX_PY312_EXE = Path(
    r"C:\Users\kj43b\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
)
LOCAL_DEPS_DIR = Path(
    r"C:\Users\kj43b\.codex\visualizations\2026\10\06"
    r"\01a10ffb-5a5e-7fd0-8847-d6af3988f73a\bo_eur_005_audit\deps"
)

if (
    sys.version_info[:2] != (3, 12)
    and CODEX_PY312_EXE.exists()
    and os.environ.get("GSR_EURUSD_REEXEC") != "1"
):
    env = dict(os.environ, GSR_EURUSD_REEXEC="1", PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    raise SystemExit(
        subprocess.call([str(CODEX_PY312_EXE), str(Path(__file__).resolve()), *sys.argv[1:]], env=env)
    )

if sys.version_info[:2] == (3, 12) and LOCAL_DEPS_DIR.exists() and str(LOCAL_DEPS_DIR) not in sys.path:
    sys.path.insert(0, str(LOCAL_DEPS_DIR))

import numpy as np
import pandas as pd

try:
    import scipy
    from scipy.stats import t as student_t
    HAS_SCIPY = True
except ImportError:
    scipy = None  # type: ignore[assignment]
    student_t = None  # type: ignore[assignment]
    HAS_SCIPY = False

try:
    import statsmodels
    import statsmodels.api as sm
    from statsmodels.stats.sandwich_covariance import cov_hac, weights_bartlett
    HAS_STATSMODELS = True
except ImportError:
    statsmodels = None  # type: ignore[assignment]
    HAS_STATSMODELS = False

SCRIPT_VERSION = "1.0.0"
PIPELINE_CASE_ID = "GSR-2026W46"
CANDIDATE_CASE_IDS = (
    "GSR-CLIMAX-001",
    "GSR-PULLBACK-001",
    "GSR-FAKEOUT-001",
)
SURVEY_CASE_ID = "GSR-SURVEY-001"

# Frozen Stage-1 EURUSD hashes from output_is_profile_20261107_065432
EXPECTED_EURUSD_LEDGER_SHA256 = "a45156cfc29cec249a538d3b81b85b74e02817c0cf0ae67ac783b6d57c72c327"
EXPECTED_EURUSD_LEDGER_ROWS = 6_733
EXPECTED_EURUSD_M1_SHA256 = "029bc12ccd4b244173cd9ed294c7dc8ec9f9b61cfd4499544722179158433a4d"
EXPECTED_EURUSD_M1_IS_ROWS = 2_610_900

# Strict In-Sample boundary (2022+ OOS strictly blocked for candidate evaluation)
IS_START_DT = datetime(2015, 1, 1, 0, 0, 0)
IS_END_DT = datetime(2021, 12, 31, 23, 59, 59)

PAYOUT_NET = Decimal("0.85")
LOSS_NET = Decimal("-1.00")
BREAKEVEN_WIN_RATE = float(Decimal("1") / (Decimal("1") + PAYOUT_NET))  # 20/37 = 0.5405405405405406

STAGE1_DIR = Path(
    r"G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\トレード手法の市場調査＆データ点検"
)
STAGE2_DIR = Path(
    r"G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証"
)
STAGE3_DIR = Path(
    r"G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\執行監査・週次総括・Git資産整理"
)
EXISTING_EURUSD_REPORT_DIR = Path(
    r"G:\マイドライブ\BO （順張・逆張）検証（パラメーター調整）\逆張りEA\EURUSD"
)

CANDIDATE_EURUSD_M1_PATHS = [
    Path(r"G:\マイドライブ\通貨ペア\Dukascopy 1分足\EURUSD\2026.10.16EURUSD(5)-M1-No Session.csv"),
    Path(r"G:\マイドライブ\通貨ペア\Dukascopy 1分足\EURUSD\EURUSD1.csv"),
    Path(r"G:\マイドライブ\BO （順張・逆張）検証（パラメーター調整）\Spark用資料\EURUSD\EURUSD1.csv"),
]


# =====================================================================
# Step 1: File Discovery & SHA256 Verification
# =====================================================================

def compute_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def discover_eurusd_ledger(explicit_path: Path | None = None) -> Path:
    if explicit_path is not None and explicit_path.exists():
        return explicit_path.resolve()

    candidates: list[Path] = [
        STAGE1_DIR / "output_is_profile_20261107_065432" / "is_2015_2021_opportunity_ledger_eurusd.csv",
        STAGE2_DIR / "is_2015_2021_opportunity_ledger_eurusd.csv",
        STAGE1_DIR / "is_2015_2021_opportunity_ledger_eurusd.csv",
    ]
    if STAGE1_DIR.exists():
        profile_dirs = sorted(
            STAGE1_DIR.glob("output_is_profile_*"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        for d in profile_dirs:
            p = d / "is_2015_2021_opportunity_ledger_eurusd.csv"
            if p not in candidates:
                candidates.append(p)

    existing = [p for p in candidates if p.exists() and p.is_file()]
    if not existing:
        raise FileNotFoundError(
            "EURUSD Stage-1 opportunity ledger (is_2015_2021_opportunity_ledger_eurusd.csv) not found."
        )
    for p in existing:
        if compute_sha256(p) == EXPECTED_EURUSD_LEDGER_SHA256:
            return p.resolve()
    return existing[0].resolve()


def discover_eurusd_m1_csv(explicit_path: Path | None = None) -> Path:
    if explicit_path is not None and explicit_path.exists():
        return explicit_path.resolve()

    existing = [p for p in CANDIDATE_EURUSD_M1_PATHS if p.exists() and p.is_file()]
    pair_dir = Path(r"G:\マイドライブ\通貨ペア\Dukascopy 1分足\EURUSD")
    if pair_dir.exists():
        for p in sorted(pair_dir.glob("*.csv"), key=lambda x: x.stat().st_size, reverse=True):
            if p not in existing:
                existing.append(p)
    if not existing:
        raise FileNotFoundError("EURUSD M1 CSV not found in G:\\マイドライブ\\通貨ペア\\Dukascopy 1分足\\EURUSD.")
    for p in existing:
        if compute_sha256(p) == EXPECTED_EURUSD_M1_SHA256:
            return p.resolve()
    return existing[0].resolve()


# =====================================================================
# Step 2: Exact 1e-5 Integer Price Grid & Timestamp Parser
# =====================================================================

def decimal_points_exact(d: Decimal) -> int:
    """Convert EURUSD Decimal price to exact 1e-5 integer points (1 pip = 10 pts, 0.1 pip = 1 pt)."""
    sign, digits, exponent = d.as_tuple()
    if not any(digits):
        return 0
    power = exponent + 5
    if power < 0:
        keep = len(digits) + power
        if keep <= 0 or any(digits[keep:]):
            raise ValueError("PRICE_GRID")
        digits = digits[:keep]
        power = 0
    coefficient = 0
    for digit in digits:
        coefficient = coefficient * 10 + digit
    value = coefficient * (10 ** power)
    return -value if sign else value


def parse_m1_row_timestamp(row: list[str]) -> tuple[datetime | None, int]:
    """Parse Dukascopy or MT4 M1 timestamp and return (datetime, ohlc_start_idx)."""
    if len(row) < 5:
        return None, 1
    c0 = row[0].strip()
    c1 = row[1].strip()
    if ":" in c1 and len(c0) in (8, 10) and c0[0].isdigit():
        dt_str = f"{c0.replace('.', '-').replace('/', '-')} {c1}"
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
            try:
                return datetime.strptime(dt_str, fmt), 2
            except ValueError:
                pass
    if c0 and c0[0].isdigit():
        norm = c0.replace(".", "-").replace("/", "-")
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S"):
            try:
                return datetime.strptime(norm[:19], fmt), 1
            except ValueError:
                pass
    return None, 1


def check_ohlc_bar(raw_ohlc: list[str]) -> tuple[list[int], set[str]]:
    reasons: set[str] = set()
    points: list[int] = []
    for s in raw_ohlc[:4]:
        try:
            d = Decimal(s.strip())
            if not d.is_finite():
                reasons.add("NONFINITE")
                continue
            pt = decimal_points_exact(d)
            if pt <= 0:
                reasons.add("NONPOSITIVE_PRICE")
                continue
            points.append(pt)
        except InvalidOperation:
            reasons.add("PRICE_PARSE")
        except ValueError as exc:
            reasons.add(str(exc))
    if len(points) == 4:
        o, h, l, c = points
        if not (l <= min(o, c) <= max(o, c) <= h):
            reasons.add("OHLC_ORDER")
    else:
        reasons.add("INCOMPLETE_OHLC")
    return points, reasons


# =====================================================================
# Step 3: Newey-West HAC (lag=1, Bartlett, finite-sample correction)
# =====================================================================

def critical_t_975(df: int) -> float:
    if HAS_SCIPY and student_t is not None:
        return float(student_t.ppf(0.975, df))
    # High-precision Peizer-Pratt / Hill approximation fallback when scipy is absent
    if df <= 1:
        return 12.7062047364
    z = 1.959963984540054
    z3 = z ** 3
    z5 = z ** 5
    return z + (z3 + z) / (4.0 * df) + (5.0 * z5 + 16.0 * z3 + 3.0 * z) / (96.0 * (df ** 2))


def compute_newey_west_stats(ev_series: list[float] | np.ndarray) -> dict[str, Any]:
    ans: dict[str, Any] = {
        "n": 0,
        "ev": None,
        "se_hac": None,
        "lower_97_5": None,
        "t_stat_ev_gt_0": None,
        "status": "HOLD",
        "hold_reason": None,
    }
    try:
        x = np.asarray(ev_series, dtype=float)
        n = int(len(x))
        ans["n"] = n
        if n == 0:
            ans["hold_reason"] = "EMPTY_SAMPLE"
            return ans
        ans["ev"] = float(x.mean())
        if n < 2:
            ans["hold_reason"] = "INSUFFICIENT_N"
            return ans
        if np.ptp(x) == 0:
            ans["hold_reason"] = "ZERO_VARIANCE"
            return ans

        u = x - x.mean()
        v = float((np.dot(u, u) + np.dot(u[1:], u[:-1])) / (n ** 2) * (n / (n - 1)))
        if not np.isfinite(v) or v <= 0:
            ans["hold_reason"] = "NONPOSITIVE_HAC_VAR"
            return ans
        se = float(np.sqrt(v))

        if HAS_STATSMODELS and sm is not None:
            fit = sm.OLS(x, np.ones((n, 1))).fit()
            se_sm = float(
                np.sqrt(
                    cov_hac(fit, nlags=1, weights_func=weights_bartlett, use_correction=True)[0, 0]
                )
            )
            if np.isfinite(se_sm) and se_sm > 0:
                se = se_sm

        crit = critical_t_975(n - 1)
        low = float(x.mean() - crit * se)
        t_stat = float(x.mean() / se)
        ans.update(
            se_hac=se,
            lower_97_5=low,
            t_stat_ev_gt_0=t_stat,
            status="PASS_CLB_GT_0" if low > 0 else "FAIL_NOT_ABOVE_ZERO",
        )
        return ans
    except Exception as exc:
        ans["hold_reason"] = f"EXCEPTION:{type(exc).__name__}"
        return ans


# =====================================================================
# Step 4: Load EURUSD M1 Bars for IS Candidates & Existing Report Audit
# =====================================================================

def collect_existing_eurusd_report_timestamps(report_dir: Path) -> set[datetime]:
    req_ts: set[datetime] = set()
    if not report_dir.exists():
        return req_ts
    for csv_file in sorted(report_dir.glob("*.csv")):
        try:
            with csv_file.open("r", encoding="utf-8-sig", errors="replace", newline="") as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames or "EntryTime" not in reader.fieldnames:
                    continue
                for row in reader:
                    e_str = (row.get("EntryTime") or "").strip()
                    dt, _ = parse_m1_row_timestamp([e_str, "0", "0", "0", "0"])
                    if dt is not None:
                        for m in range(0, 10):
                            req_ts.add(dt + timedelta(minutes=m))
        except Exception:
            continue
    return req_ts


def load_eurusd_m1_bars(
    m1_path: Path,
    is_required_ts: set[datetime],
    audit_report_ts: set[datetime],
) -> tuple[dict[datetime, tuple[list[int], set[str]]], Counter, dict[datetime, tuple[list[int], set[str]]], dict[str, Any]]:
    """Scan EURUSD M1 CSV once, enforcing strict IS gate (2015-2021) for candidate evaluation."""
    m1_sha = compute_sha256(m1_path)
    is_bars: dict[datetime, tuple[list[int], set[str]]] = {}
    is_counts: Counter = Counter()
    audit_bars: dict[datetime, tuple[list[int], set[str]]] = {}

    total_rows = 0
    is_rows = 0
    pre_2015_rows = 0
    post_2021_oos_rows = 0

    with m1_path.open("r", encoding="utf-8-sig", errors="replace", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            total_rows += 1
            dt, ohlc_idx = parse_m1_row_timestamp(row)
            if dt is None or len(row) < ohlc_idx + 4:
                continue

            if dt in audit_report_ts:
                audit_bars[dt] = check_ohlc_bar(row[ohlc_idx : ohlc_idx + 4])

            if dt < IS_START_DT:
                pre_2015_rows += 1
                continue
            if dt > IS_END_DT:
                post_2021_oos_rows += 1
                continue

            is_rows += 1
            if dt in is_required_ts:
                is_counts[dt] += 1
                is_bars[dt] = check_ohlc_bar(row[ohlc_idx : ohlc_idx + 4])

    meta = {
        "m1_path": str(m1_path),
        "m1_sha256": m1_sha,
        "expected_m1_sha256": EXPECTED_EURUSD_M1_SHA256,
        "sha256_matched": m1_sha == EXPECTED_EURUSD_M1_SHA256,
        "total_raw_rows": total_rows,
        "pre_2015_rows_dropped": pre_2015_rows,
        "post_2021_oos_rows_blocked": post_2021_oos_rows,
        "is_2015_2021_rows_kept": is_rows,
        "expected_is_rows_matched": is_rows == EXPECTED_EURUSD_M1_IS_ROWS,
        "is_required_timestamps_count": len(is_required_ts),
        "is_found_timestamps_count": len(is_bars),
    }
    return is_bars, is_counts, audit_bars, meta


# =====================================================================
# Step 5: Evaluate IS Candidates & Multi-Dimensional Plateau Grids
# =====================================================================

def evaluate_is_ledger_outcomes(
    ledger_df: pd.DataFrame,
    is_bars: dict[datetime, tuple[list[int], set[str]]],
    is_counts: Counter,
) -> pd.DataFrame:
    records: list[dict[str, Any]] = []
    for r in ledger_df.to_dict("records"):
        entry_dt = datetime.strptime(str(r["expected_entry_utc"]).strip(), "%Y-%m-%d %H:%M:%S")
        expiry_dt = datetime.strptime(str(r["expected_expiry_utc"]).strip(), "%Y-%m-%d %H:%M:%S")
        assert expiry_dt - entry_dt == timedelta(minutes=5), f"Invalid 5m window on {entry_dt}"
        assert IS_START_DT <= entry_dt <= IS_END_DT, f"OOS timestamp leak detected: {entry_dt}"

        reasons: set[str] = set()
        if str(r.get("continuity_status", "")) != "VALID_6BAR_CONTINUOUS":
            reasons.add(str(r.get("invalid_reasons", "LEDGER_INVALID_GAP")))

        for m in range(6):
            dt = entry_dt + timedelta(minutes=m)
            if is_counts[dt] == 0:
                reasons.add(f"MISSING_M1_BAR_T{m + 1}")
            elif is_counts[dt] > 1:
                reasons.add(f"DUPLICATE_M1_BAR_T{m + 1}")
            if dt in is_bars:
                reasons.update(is_bars[dt][1])

        valid = len(reasons) == 0
        ep: int | None = None
        xp: int | None = None
        favorable_pts: int | None = None
        win_01pip: bool | None = None
        win_02pip: bool | None = None
        win_03pip: bool | None = None
        raw_tie: bool | None = None
        ev_01pip: float | None = None
        ev_02pip: float | None = None
        ev_03pip: float | None = None

        direction = str(r["direction"]).strip().upper()
        if valid:
            ep = is_bars[entry_dt][0][0]   # Open of t+1
            xp = is_bars[expiry_dt][0][0]  # Open of t+6
            favorable_pts = (xp - ep) if direction == "HIGH" else (ep - xp)
            raw_tie = favorable_pts == 0
            win_01pip = favorable_pts > 1  # > +0.1 pip (1 pt)
            win_02pip = favorable_pts > 2  # > +0.2 pip (2 pts)
            win_03pip = favorable_pts > 3  # > +0.3 pip (3 pts)
            ev_01pip = float(PAYOUT_NET) if win_01pip else float(LOSS_NET)
            ev_02pip = float(PAYOUT_NET) if win_02pip else float(LOSS_NET)
            ev_03pip = float(PAYOUT_NET) if win_03pip else float(LOSS_NET)

        atr_pips = float(r["atr14_pips"])
        bbw_pips = float(r["m5_bbw_pips"])
        slope_pips = float(r["m5_slope3_pips"])

        records.append(
            {
                "case_id": r["case_id"],
                "parent_case_id": r["parent_case_id"],
                "strategy": r["strategy"],
                "direction": direction,
                "decision_open_utc": r["decision_open_utc"],
                "signal_utc": r["signal_utc"],
                "expected_entry_utc": r["expected_entry_utc"],
                "expected_expiry_utc": r["expected_expiry_utc"],
                "year": int(r["year"]),
                "utc_hour": int(r["utc_hour"]),
                "session": r["session"],
                "atr14_pips": atr_pips,
                "atr_bucket": r["atr_bucket"],
                "m5_bbw_pips": bbw_pips,
                "m5_slope3_pips": slope_pips,
                "abs_m5_slope3_pips": abs(slope_pips),
                "m5_ref_close_utc": r["m5_ref_close_utc"],
                "valid": valid,
                "invalid_reasons": "|".join(sorted(reasons)) if reasons else "PASS",
                "entry_price_pts": ep,
                "expiry_price_pts": xp,
                "favorable_diff_pts": favorable_pts,
                "raw_tie_0pt": raw_tie,
                "win_01pip": win_01pip,
                "win_02pip": win_02pip,
                "win_03pip": win_03pip,
                "ev_01pip": ev_01pip,
                "ev_02pip": ev_02pip,
                "ev_03pip": ev_03pip,
            }
        )
    return pd.DataFrame(records)


def evaluate_subset_metrics(sub_df: pd.DataFrame, stress_pts: int = 1) -> dict[str, Any]:
    valid = sub_df[sub_df["valid"]].sort_values("expected_entry_utc")
    n_valid = int(len(valid))
    if n_valid == 0:
        return {
            "n_valid": 0,
            "wins": 0,
            "losses": 0,
            "raw_ties_0pt": 0,
            "stress_1pt_losses": 0,
            "win_rate": None,
            "win_rate_pct": None,
            "breakeven_margin_pct": None,
            "ev": None,
            "se_hac": None,
            "lower_97_5": None,
            "t_stat_ev_gt_0": None,
            "exceeds_breakeven": False,
            "clb_positive": False,
            "status": "EMPTY",
        }

    diff = valid["favorable_diff_pts"].to_numpy(dtype=int)
    wins_mask = diff > stress_pts
    ev_arr = np.where(wins_mask, float(PAYOUT_NET), float(LOSS_NET))
    wins = int(wins_mask.sum())
    losses = n_valid - wins
    raw_ties = int((diff == 0).sum())
    stress_1pt = int((diff == 1).sum())
    win_rate = float(wins / n_valid)
    exact_ev = float((Decimal(wins) * PAYOUT_NET + Decimal(losses) * LOSS_NET) / Decimal(n_valid))
    exceeds_be = (wins * 185) > (n_valid * 100)
    hac = compute_newey_west_stats(ev_arr)
    clb_pos = bool(hac["lower_97_5"] is not None and hac["lower_97_5"] > 0)

    return {
        "n_valid": n_valid,
        "wins": wins,
        "losses": losses,
        "raw_ties_0pt": raw_ties,
        "stress_1pt_losses": stress_1pt,
        "win_rate": round(win_rate, 6),
        "win_rate_pct": round(win_rate * 100.0, 2),
        "breakeven_margin_pct": round((win_rate - BREAKEVEN_WIN_RATE) * 100.0, 2),
        "ev": round(exact_ev, 6),
        "se_hac": round(hac["se_hac"], 6) if hac["se_hac"] is not None else None,
        "lower_97_5": round(hac["lower_97_5"], 6) if hac["lower_97_5"] is not None else None,
        "t_stat_ev_gt_0": round(hac["t_stat_ev_gt_0"], 4) if hac["t_stat_ev_gt_0"] is not None else None,
        "exceeds_breakeven": bool(exceeds_be),
        "clb_positive": clb_pos,
        "status": hac["status"],
    }


def build_standalone_and_marginal_summaries(
    outcomes_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    standalone_rows: list[dict[str, Any]] = []
    yearly_rows: list[dict[str, Any]] = []
    session_rows: list[dict[str, Any]] = []
    atr_rows: list[dict[str, Any]] = []

    for cid in CANDIDATE_CASE_IDS:
        g = outcomes_df[outcomes_df["case_id"] == cid]
        strat = str(g["strategy"].iloc[0]) if len(g) > 0 else cid
        m1 = evaluate_subset_metrics(g, stress_pts=1)
        m2 = evaluate_subset_metrics(g, stress_pts=2)
        m3 = evaluate_subset_metrics(g, stress_pts=3)
        standalone_rows.append(
            {
                "case_id": cid,
                "parent_case_id": PIPELINE_CASE_ID,
                "strategy": strat,
                "total_candidates": int(len(g)),
                "n_valid": m1["n_valid"],
                "n_invalid": int(len(g) - m1["n_valid"]),
                "wins_01pip": m1["wins"],
                "losses_01pip": m1["losses"],
                "raw_ties_0pt": m1["raw_ties_0pt"],
                "stress_1pt_losses": m1["stress_1pt_losses"],
                "win_rate_01pip_pct": m1["win_rate_pct"],
                "breakeven_margin_01pip_pct": m1["breakeven_margin_pct"],
                "ev_01pip": m1["ev"],
                "se_hac_01pip": m1["se_hac"],
                "clb975_01pip": m1["lower_97_5"],
                "t_stat_01pip": m1["t_stat_ev_gt_0"],
                "win_rate_02pip_pct": m2["win_rate_pct"],
                "ev_02pip": m2["ev"],
                "clb975_02pip": m2["lower_97_5"],
                "win_rate_03pip_pct": m3["win_rate_pct"],
                "ev_03pip": m3["ev"],
                "clb975_03pip": m3["lower_97_5"],
                "gate2_clb_gt_0": m1["clb_positive"],
                "status": m1["status"],
            }
        )

        for yr, yg in g.groupby("year"):
            ym = evaluate_subset_metrics(yg, stress_pts=1)
            yearly_rows.append(
                {
                    "case_id": cid,
                    "strategy": strat,
                    "year": int(yr),
                    "n_valid": ym["n_valid"],
                    "wins": ym["wins"],
                    "losses": ym["losses"],
                    "win_rate_01pip_pct": ym["win_rate_pct"],
                    "ev_01pip": ym["ev"],
                    "clb975_01pip": ym["lower_97_5"],
                    "exceeds_breakeven": ym["exceeds_breakeven"],
                }
            )

        for sess, sg in g.groupby("session"):
            sm_res = evaluate_subset_metrics(sg, stress_pts=1)
            session_rows.append(
                {
                    "case_id": cid,
                    "strategy": strat,
                    "session": sess,
                    "n_valid": sm_res["n_valid"],
                    "wins": sm_res["wins"],
                    "losses": sm_res["losses"],
                    "win_rate_01pip_pct": sm_res["win_rate_pct"],
                    "ev_01pip": sm_res["ev"],
                    "clb975_01pip": sm_res["lower_97_5"],
                    "exceeds_breakeven": sm_res["exceeds_breakeven"],
                }
            )

        for ab, ag in g.groupby("atr_bucket"):
            am = evaluate_subset_metrics(ag, stress_pts=1)
            atr_rows.append(
                {
                    "case_id": cid,
                    "strategy": strat,
                    "atr_bucket": ab,
                    "n_valid": am["n_valid"],
                    "wins": am["wins"],
                    "losses": am["losses"],
                    "win_rate_01pip_pct": am["win_rate_pct"],
                    "ev_01pip": am["ev"],
                    "clb975_01pip": am["lower_97_5"],
                    "exceeds_breakeven": am["exceeds_breakeven"],
                }
            )

    return (
        pd.DataFrame(standalone_rows),
        pd.DataFrame(yearly_rows),
        pd.DataFrame(session_rows),
        pd.DataFrame(atr_rows),
    )


# Strategy-specific 3D parameter grids grounded in Stage-1 EURUSD quantiles (4 x 4 x 4 = 64 cells each)
STRATEGY_GRIDS: dict[str, dict[str, Any]] = {
    "GSR-CLIMAX-001": {
        "atr_min_grid": (1.2, 1.5, 1.8, 2.2),
        "bbw_max_grid": (10.0, 12.5, 15.0, 18.0),
        "slope_mode": "max",  # non-trending M5 filter: |slope| <= threshold
        "slope_grid": (0.6, 1.0, 1.5, 2.0),
    },
    "GSR-FAKEOUT-001": {
        "atr_min_grid": (1.2, 1.6, 2.0, 2.5),
        "bbw_max_grid": (15.0, 20.0, 28.0, 999.0),
        "slope_mode": "max",  # non-runaway M5 filter: |slope| <= threshold
        "slope_grid": (1.0, 1.8, 2.8, 4.0),
    },
    "GSR-PULLBACK-001": {
        "atr_min_grid": (1.2, 1.8, 2.4, 3.0),
        "bbw_max_grid": (25.0, 35.0, 50.0, 999.0),
        "slope_mode": "min",  # trending M5 filter: |slope| >= threshold
        "slope_grid": (1.5, 2.0, 2.8, 3.8),
    },
}


def run_eurusd_plateau_grid(
    outcomes_df: pd.DataFrame,
    min_cell_n: int = 50,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    records: list[dict[str, Any]] = []
    stress_levels = (1, 2, 3)

    for cid in CANDIDATE_CASE_IDS:
        g_df = outcomes_df[outcomes_df["case_id"] == cid]
        strat = str(g_df["strategy"].iloc[0]) if len(g_df) > 0 else cid
        cfg = STRATEGY_GRIDS[cid]
        atr_grid = cfg["atr_min_grid"]
        bbw_grid = cfg["bbw_max_grid"]
        slope_mode = cfg["slope_mode"]
        slope_grid = cfg["slope_grid"]

        coords = list(itertools.product(range(len(atr_grid)), range(len(bbw_grid)), range(len(slope_grid))))
        cell_lookup: dict[tuple[int, int, int], dict[int, dict[str, Any]]] = {}

        for coord in coords:
            ia, ib, islp = coord
            a_min = atr_grid[ia]
            b_max = bbw_grid[ib]
            s_thr = slope_grid[islp]

            mask = (g_df["atr14_pips"] >= a_min) & (g_df["m5_bbw_pips"] <= b_max)
            if slope_mode == "max":
                mask = mask & (g_df["abs_m5_slope3_pips"] <= s_thr)
            else:
                mask = mask & (g_df["abs_m5_slope3_pips"] >= s_thr)

            sub_df = g_df[mask]
            cell_lookup[coord] = {
                sp: evaluate_subset_metrics(sub_df, stress_pts=sp) for sp in stress_levels
            }

        for coord, stress_map in cell_lookup.items():
            ia, ib, islp = coord
            neighbors = [
                other
                for other in cell_lookup
                if abs(other[0] - ia) + abs(other[1] - ib) + abs(other[2] - islp) == 1
            ]
            nb_be_flags = [
                cell_lookup[nb][1]["exceeds_breakeven"]
                for nb in neighbors
                if cell_lookup[nb][1]["n_valid"] >= min_cell_n
            ]
            nb_be_ratio = float(sum(nb_be_flags) / len(nb_be_flags)) if nb_be_flags else 0.0

            m1 = stress_map[1]
            m2 = stress_map[2]
            m3 = stress_map[3]

            if m1["n_valid"] < min_cell_n:
                p_class = "LOW_SAMPLE_UNDER_50"
            elif not m1["exceeds_breakeven"]:
                p_class = "BELOW_BREAKEVEN"
            elif m1["clb_positive"] and m2["exceeds_breakeven"] and nb_be_ratio >= 0.75:
                p_class = "STABLE_PLATEAU_CLB_PASS"
            elif m2["exceeds_breakeven"] and nb_be_ratio >= 0.75:
                p_class = "CANDIDATE_PLATEAU_CLB_UNPROVEN"
            elif nb_be_ratio >= 0.50:
                p_class = "MODERATE_REGION"
            else:
                p_class = "ISOLATED_SPIKE_WARNING"

            records.append(
                {
                    "case_id": cid,
                    "strategy": strat,
                    "atr_min_pips": atr_grid[ia],
                    "m5_bbw_max_pips": bbw_grid[ib],
                    "m5_slope_rule": f"|slope3| <= {slope_grid[islp]}" if slope_mode == "max" else f"|slope3| >= {slope_grid[islp]}",
                    "n_valid": m1["n_valid"],
                    "win_rate_01pip_pct": m1["win_rate_pct"],
                    "ev_01pip": m1["ev"],
                    "se_hac_01pip": m1["se_hac"],
                    "clb975_01pip": m1["lower_97_5"],
                    "win_rate_02pip_pct": m2["win_rate_pct"],
                    "ev_02pip": m2["ev"],
                    "clb975_02pip": m2["lower_97_5"],
                    "win_rate_03pip_pct": m3["win_rate_pct"],
                    "ev_03pip": m3["ev"],
                    "clb975_03pip": m3["lower_97_5"],
                    "l1_neighbors_ge_min_n": len(nb_be_flags),
                    "neighbor_be_ratio_01pip": round(nb_be_ratio, 4),
                    "survives_02pip_be": m2["exceeds_breakeven"],
                    "survives_03pip_be": m3["exceeds_breakeven"],
                    "clb975_gt_0_at_01pip": m1["clb_positive"],
                    "plateau_class": p_class,
                }
            )

    plateau_df = pd.DataFrame(records)
    summary_by_case: dict[str, Any] = {}
    for cid, g in plateau_df.groupby("case_id"):
        valid_g = g[g["n_valid"] >= min_cell_n].sort_values("ev_01pip", ascending=False)
        top_row = valid_g.iloc[0].to_dict() if len(valid_g) > 0 else None
        summary_by_case[str(cid)] = {
            "total_cells": int(len(g)),
            "cells_n_ge_50": int((g["n_valid"] >= min_cell_n).sum()),
            "cells_exceeding_be_01pip": int(((g["n_valid"] >= min_cell_n) & (g["ev_01pip"] > 0)).sum()),
            "cells_surviving_02pip_be": int(((g["n_valid"] >= min_cell_n) & g["survives_02pip_be"]).sum()),
            "cells_clb975_gt_0": int(((g["n_valid"] >= min_cell_n) & g["clb975_gt_0_at_01pip"]).sum()),
            "class_counts": dict(Counter(g["plateau_class"])),
            "best_cell_n_ge_50": top_row,
        }

    meta = {
        "total_grid_cells": int(len(plateau_df)),
        "total_stress_evaluations": int(len(plateau_df) * len(stress_levels)),
        "min_cell_n": min_cell_n,
        "breakeven_win_rate_pct": round(BREAKEVEN_WIN_RATE * 100.0, 3),
        "by_case_id": summary_by_case,
    }
    return plateau_df, meta


# =====================================================================
# Step 6: Existing EURUSD Reports M1 Continuity & 6m-vs-5m Bug Audit
# =====================================================================

def audit_existing_eurusd_reports(
    report_dir: Path,
    audit_bars: dict[datetime, tuple[list[int], set[str]]],
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    if not report_dir.exists():
        return results

    for csv_file in sorted(report_dir.glob("*.csv")):
        try:
            with csv_file.open("r", encoding="utf-8-sig", errors="replace", newline="") as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames or "EntryTime" not in reader.fieldnames:
                    continue
                rows = list(reader)
        except Exception:
            continue

        if not rows:
            continue

        total = len(rows)
        delta_5m = 0
        delta_6m_mt4_gt_bug = 0
        delta_gt_6m_gap = 0
        m1_6bar_continuous = 0
        m1_6bar_gap_broken = 0
        m1_outside_coverage = 0
        true_5m_wins_01pip = 0
        true_5m_evaluated = 0

        for r in rows:
            e_str = (r.get("EntryTime") or "").strip()
            s_str = (r.get("SettleTime") or "").strip()
            direction = (r.get("Type") or "").strip().upper()
            e_dt, _ = parse_m1_row_timestamp([e_str, "0", "0", "0", "0"])
            s_dt, _ = parse_m1_row_timestamp([s_str, "0", "0", "0", "0"])
            if e_dt is None:
                continue

            if s_dt is not None:
                diff_min = (s_dt - e_dt).total_seconds() / 60.0
                if abs(diff_min - 5.0) < 1e-6:
                    delta_5m += 1
                elif abs(diff_min - 6.0) < 1e-6:
                    delta_6m_mt4_gt_bug += 1
                elif diff_min > 6.0:
                    delta_gt_6m_gap += 1

            # Check M1 6-bar continuity (t+1..t+6) in Dukascopy M1
            window_dts = [e_dt + timedelta(minutes=m) for m in range(6)]
            if all(dt in audit_bars for dt in window_dts):
                m1_6bar_continuous += 1
                ep = audit_bars[e_dt][0][0]
                xp_5m = audit_bars[e_dt + timedelta(minutes=5)][0][0]
                fav = (xp_5m - ep) if direction == "HIGH" else (ep - xp_5m)
                true_5m_evaluated += 1
                if fav > 1:
                    true_5m_wins_01pip += 1
            else:
                if e_dt in audit_bars:
                    m1_6bar_gap_broken += 1
                else:
                    m1_outside_coverage += 1

        true_5m_wr = round(true_5m_wins_01pip / true_5m_evaluated * 100.0, 2) if true_5m_evaluated > 0 else None
        results.append(
            {
                "case_id": SURVEY_CASE_ID,
                "parent_case_id": PIPELINE_CASE_ID,
                "file": csv_file.name,
                "total_trades": total,
                "settle_delta_5m_count": delta_5m,
                "settle_delta_6m_barsPassed_gt_5_count": delta_6m_mt4_gt_bug,
                "settle_delta_gt_6m_gap_count": delta_gt_6m_gap,
                "m1_t1_t6_continuous_count": m1_6bar_continuous,
                "m1_t1_t6_gap_broken_count": m1_6bar_gap_broken,
                "m1_entry_missing_or_tz_offset_count": m1_outside_coverage,
                "recomputed_true_5m_01pip_win_rate_pct": true_5m_wr,
            }
        )
    return results


# =====================================================================
# CLI & Main Execution
# =====================================================================

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="GSR-2026W46 Stage 2: EURUSD-Only IS Statistical Verification & Plateau Analyzer (v1.0)"
    )
    parser.add_argument("--ledger", type=Path, default=None, help="Path to EURUSD Stage-1 opportunity ledger CSV")
    parser.add_argument("--m1-csv", type=Path, default=None, help="Path to EURUSD Dukascopy M1 CSV")
    parser.add_argument("--out-dir", type=Path, default=None, help="Custom output directory")
    parser.add_argument("--min-cell-n", type=int, default=50, help="Minimum valid trades per Plateau grid cell")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    ledger_path = discover_eurusd_ledger(args.ledger)
    m1_path = discover_eurusd_m1_csv(args.m1_csv)

    now_jst = datetime.now(timezone(timedelta(hours=9)))
    stamp = now_jst.strftime("%Y%m%d_%H%M%S")
    if args.out_dir is not None:
        out_dir = args.out_dir.resolve()
    else:
        base_root = STAGE2_DIR if STAGE2_DIR.exists() else Path.cwd()
        out_dir = (base_root / f"output_eurusd_is_plateau_{stamp}").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Read & verify Stage-1 EURUSD Opportunity Ledger
    ledger_sha = compute_sha256(ledger_path)
    ledger_df = pd.read_csv(ledger_path, keep_default_na=False)
    is_required_ts: set[datetime] = set()
    for r in ledger_df.to_dict("records"):
        e_dt = datetime.strptime(str(r["expected_entry_utc"]).strip(), "%Y-%m-%d %H:%M:%S")
        for m in range(6):
            is_required_ts.add(e_dt + timedelta(minutes=m))

    # 2. Collect existing EURUSD report timestamps & scan EURUSD M1 CSV once
    audit_report_ts = collect_existing_eurusd_report_timestamps(EXISTING_EURUSD_REPORT_DIR)
    is_bars, is_counts, audit_bars, m1_meta = load_eurusd_m1_bars(
        m1_path, is_required_ts, audit_report_ts
    )

    # 3. Evaluate EURUSD IS Outcomes (2015-2021)
    outcomes_df = evaluate_is_ledger_outcomes(ledger_df, is_bars, is_counts)
    standalone_df, yearly_df, session_df, atr_df = build_standalone_and_marginal_summaries(outcomes_df)

    # 4. Run 3D Parameter Plateau Grid (192 cells x 3 stress levels = 576 evaluations)
    plateau_df, plateau_meta = run_eurusd_plateau_grid(outcomes_df, min_cell_n=args.min_cell_n)

    # 5. Audit Existing EURUSD Report CSVs against M1 timestamps
    existing_audit_rows = audit_existing_eurusd_reports(EXISTING_EURUSD_REPORT_DIR, audit_bars)
    existing_audit_df = pd.DataFrame(existing_audit_rows)

    # 6. Save all Stage-2 deliverables to out_dir
    outcomes_csv = out_dir / "is_outcomes_eurusd.csv"
    standalone_csv = out_dir / "is_standalone_summary_eurusd.csv"
    yearly_csv = out_dir / "is_yearly_breakdown_eurusd.csv"
    session_csv = out_dir / "is_session_breakdown_eurusd.csv"
    atr_csv = out_dir / "is_atr_breakdown_eurusd.csv"
    plateau_csv = out_dir / "is_plateau_grid_eurusd.csv"
    existing_audit_csv = out_dir / "existing_eurusd_reports_m1_audit.csv"
    manifest_json = out_dir / "spark_audit_handover_manifest_eurusd.json"

    outcomes_df.to_csv(outcomes_csv, index=False, encoding="utf-8-sig")
    standalone_df.to_csv(standalone_csv, index=False, encoding="utf-8-sig")
    yearly_df.to_csv(yearly_csv, index=False, encoding="utf-8-sig")
    session_df.to_csv(session_csv, index=False, encoding="utf-8-sig")
    atr_df.to_csv(atr_csv, index=False, encoding="utf-8-sig")
    plateau_df.to_csv(plateau_csv, index=False, encoding="utf-8-sig")
    if not existing_audit_df.empty:
        existing_audit_df.to_csv(existing_audit_csv, index=False, encoding="utf-8-sig")

    manifest = {
        "script_version": SCRIPT_VERSION,
        "pipeline_case_id": PIPELINE_CASE_ID,
        "target_pair": "EURUSD",
        "executed_at_jst": now_jst.isoformat(),
        "out_dir": str(out_dir),
        "ledger_verification": {
            "ledger_path": str(ledger_path),
            "ledger_sha256": ledger_sha,
            "expected_ledger_sha256": EXPECTED_EURUSD_LEDGER_SHA256,
            "sha256_matched": ledger_sha == EXPECTED_EURUSD_LEDGER_SHA256,
            "ledger_rows": int(len(ledger_df)),
            "expected_rows_matched": int(len(ledger_df)) == EXPECTED_EURUSD_LEDGER_ROWS,
        },
        "m1_source_verification": m1_meta,
        "is_standalone_summary": standalone_df.to_dict("records"),
        "is_yearly_breakdown": yearly_df.to_dict("records"),
        "is_session_breakdown": session_df.to_dict("records"),
        "is_atr_breakdown": atr_df.to_dict("records"),
        "plateau_summary": plateau_meta,
        "existing_eurusd_reports_m1_audit": existing_audit_rows,
        "output_files_sha256": {
            "is_outcomes_eurusd.csv": compute_sha256(outcomes_csv),
            "is_standalone_summary_eurusd.csv": compute_sha256(standalone_csv),
            "is_yearly_breakdown_eurusd.csv": compute_sha256(yearly_csv),
            "is_session_breakdown_eurusd.csv": compute_sha256(session_csv),
            "is_atr_breakdown_eurusd.csv": compute_sha256(atr_csv),
            "is_plateau_grid_eurusd.csv": compute_sha256(plateau_csv),
        },
    }
    manifest_json.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Print COMPACT console summary (keeps console output < 2.5 KB to save chat tokens!)
    compact_console = {
        "pipeline_case_id": PIPELINE_CASE_ID,
        "target_pair": "EURUSD_ONLY",
        "out_dir": str(out_dir),
        "ledger_sha256_matched": manifest["ledger_verification"]["sha256_matched"],
        "m1_sha256_matched": m1_meta["sha256_matched"],
        "is_2015_2021_m1_rows": m1_meta["is_2015_2021_rows_kept"],
        "oos_2022_plus_rows_blocked": m1_meta["post_2021_oos_rows_blocked"],
        "standalone_is_results_01pip": [
            {
                "case_id": r["case_id"],
                "n_valid": r["n_valid"],
                "win_rate_01pip_pct": r["win_rate_01pip_pct"],
                "ev_01pip": r["ev_01pip"],
                "clb975_01pip": r["clb975_01pip"],
                "win_rate_02pip_pct": r["win_rate_02pip_pct"],
                "ev_02pip": r["ev_02pip"],
                "status": r["status"],
            }
            for r in standalone_df.to_dict("records")
        ],
        "plateau_grid_overview": {
            cid: {
                "cells_n_ge_50": info["cells_n_ge_50"],
                "cells_exceeding_be_01pip": info["cells_exceeding_be_01pip"],
                "cells_surviving_02pip_be": info["cells_surviving_02pip_be"],
                "cells_clb975_gt_0": info["cells_clb975_gt_0"],
                "class_counts": info["class_counts"],
                "best_cell": (
                    {
                        "atr_min": info["best_cell_n_ge_50"]["atr_min_pips"],
                        "bbw_max": info["best_cell_n_ge_50"]["m5_bbw_max_pips"],
                        "slope_rule": info["best_cell_n_ge_50"]["m5_slope_rule"],
                        "n": info["best_cell_n_ge_50"]["n_valid"],
                        "wr_01p": info["best_cell_n_ge_50"]["win_rate_01pip_pct"],
                        "ev_01p": info["best_cell_n_ge_50"]["ev_01pip"],
                        "clb975_01p": info["best_cell_n_ge_50"]["clb975_01pip"],
                        "wr_02p": info["best_cell_n_ge_50"]["win_rate_02pip_pct"],
                        "class": info["best_cell_n_ge_50"]["plateau_class"],
                    }
                    if info["best_cell_n_ge_50"]
                    else None
                ),
            }
            for cid, info in plateau_meta["by_case_id"].items()
        },
    }
    print(json.dumps(compact_console, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
