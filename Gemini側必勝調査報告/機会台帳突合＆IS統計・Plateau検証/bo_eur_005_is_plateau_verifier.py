#!/usr/bin/env python3
"""BO-EUR-005 IS Statistical Verification & Plateau Analyzer (v2.4 - Auto-Runtime & Auto-Path Edition).

How to run (Zero arguments required on local PC):
  PS C:\\Users\\kj43b> & "C:\\Users\\kj43b\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe" "$HOME\\bo_eur_005_is_plateau_verifier.py"
  (Or simply: python bo_eur_005_is_plateau_verifier.py — v2.4 auto-switches to Python 3.12 if needed)

Default output location:
  G:\\マイドライブ\\AIトレーサビリティ\\BO・EA Edge Discovery\\Gemini側必勝調査報告\\機会台帳突合＆IS統計・Plateau検証\\output_is_plateau_YYYYMMDD_HHMMSS
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import os
import platform
import subprocess
import sys
from collections import Counter
from datetime import datetime, timedelta
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
    and os.environ.get("BO_EUR_005_REEXEC") != "1"
):
    env = dict(os.environ, BO_EUR_005_REEXEC="1", PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    raise SystemExit(
        subprocess.call([str(CODEX_PY312_EXE), str(Path(__file__).resolve()), *sys.argv[1:]], env=env)
    )

if sys.version_info[:2] == (3, 12) and LOCAL_DEPS_DIR.exists() and str(LOCAL_DEPS_DIR) not in sys.path:
    sys.path.insert(0, str(LOCAL_DEPS_DIR))

import numpy as np
import pandas as pd
import scipy
from scipy.stats import t as student_t

try:
    import statsmodels
    import statsmodels.api as sm
    from statsmodels.stats.sandwich_covariance import cov_hac, weights_bartlett
    HAS_STATSMODELS = True
except ImportError:
    statsmodels = None  # type: ignore[assignment]
    HAS_STATSMODELS = False

IMPLEMENTATION_VERSION = "0.5-is-plateau-v2.4"
CASE_ID = "BO-EUR-005"

# Frozen SHA256 hashes from Contract v0.5
EXPECTED_CONTRACT_SHA256 = "b55657bccd92617fc241bcbc1962167c897aa7e761dd584601e42ee2dfc45fa5"
EXPECTED_LEDGER_SHA256 = "029f97ab3ac5c3d8084f30414422ce73d27f0fafc5e5ac2395bcd1fe4173e954"
EXPECTED_SOURCE_SHA256 = "16d036b4f72d388fb50de17588a81a78b5275b55a3e616d3ed9f7cda7f9ea9b0"
EXPECTED_OUTCOMES_SHA256 = "080dc7a36d0e32d7f00b0288eb06bf0f44db4d2710417edd56520e3d466b8687"
EXPECTED_SOURCE_ROWS = 4_343_300

# Dedicated Gemini IS/Plateau storage directory on Google Drive
DEFAULT_ARCHIVE_ROOT = Path(
    r"G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証"
)

# Candidate local paths for zero-argument auto-discovery on user PC
CANDIDATE_LEDGER_PATHS = [
    DEFAULT_ARCHIVE_ROOT / "opportunity_ledger.csv",
    Path(r"G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\AI4者会談\進行中\Scout\BO_EURUSD\EURUSD_Opportunity_Ledger_Package_20261004\output\opportunity_ledger.csv"),
    Path(r"G:\マイドライブ\AIトレーサビリティ\AI4者会談\進行中\Scout\BO_EURUSD\EURUSD_Opportunity_Ledger_Package_20261004\output\opportunity_ledger.csv"),
    Path(r"G:\マイドライブ\AIトレーサビリティ\Codex\BO-EA-Edge-Discovery\04_Python_Research\BO-EUR-005\upstream_impl1\output\opportunity_ledger.csv"),
    Path("opportunity_ledger.csv"),
]

CANDIDATE_OUTCOMES_PATHS = [
    DEFAULT_ARCHIVE_ROOT / "outcomes.csv",
    Path(r"C:\Users\kj43b\.codex\visualizations\2026\10\06\01a10ffb-5a5e-7fd0-8847-d6af3988f73a\bo_eur_005_impl1\regression_results\impl1_cli\outcomes.csv"),
    Path(r"G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\AI4者会談\進行中\Codex\BO-EUR-005\BO-EUR-005_v05_impl1_Regression\BO-EUR-005_v05_impl1\regression_results\impl1_cli\outcomes.csv"),
    Path(r"G:\マイドライブ\AIトレーサビリティ\Codex\BO-EA-Edge-Discovery\07_Tests_and_Backtests\BO-EUR-005\v05_impl1\regression_results\impl1_cli\outcomes.csv"),
    Path("outcomes.csv"),
]

CANDIDATE_SOURCE_PATHS = [
    Path(r"G:\マイドライブ\BO （順張・逆張）検証（パラメーター調整）\Spark用資料\EURUSD\EURUSD1.csv"),
    Path(r"G:\マイドライブ\通貨ペア\Dukascopy 1分足\EURUSD\EURUSD1.csv"),
    Path("EURUSD1.csv"),
]

CANDIDATE_CONTRACT_PATHS = [
    DEFAULT_ARCHIVE_ROOT / "contract_v05.json",
    Path(r"G:\マイドライブ\AIトレーサビリティ\Codex\BO-EA-Edge-Discovery\04_Python_Research\BO-EUR-005\v05_impl1\contract_v05.json"),
    Path(r"G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Codex\BO-EA-Edge-Discovery\04_Python_Research\BO-EUR-005\v05_impl1\contract_v05.json"),
    Path(r"C:\Users\kj43b\.codex\visualizations\2026\10\06\01a10ffb-5a5e-7fd0-8847-d6af3988f73a\bo_eur_005_impl1\contract_v05.json"),
    Path("contract_v05.json"),
]

# Frozen Opportunity Ledger reference counts (4,264 calendar days: 2015-01-07 to 2026-09-09)
EXPECTED_LEDGER_DAYS = 4_264
EXPECTED_STAGE_COUNTS = {
    "break_found": 2_138,
    "reentry_found": 1_042,
    "retest_found": 780,
}
EXPECTED_STATE_COUNTS = {
    "INVALID_RANGE_GAP": 1_336,
    "NO_REENTRY": 1_095,
    "NO_BREAK": 785,
    "REBREAK": 390,
    "RETEST_REJECT": 366,
    "NO_RETEST": 261,
    "BOUNDARY_DRAW": 24,
    "INVALID_MONITOR_GAP_OR_PRICE": 4,
    "OPPOSITE_BREAK": 1,
    "INVALID_REENTRY_GAP_OR_PRICE": 1,
    "OUTSIDE_COMPLETE_FILE_COVERAGE": 1,
}

# Contract v0.5 parameters
IS_START_DATE = "2015-01-07"
IS_END_DATE = "2021-12-31"
PAYOUT_NET = Decimal("0.85")
LOSS_NET = Decimal("-1.00")
BREAKEVEN_WIN_RATE = float(Decimal("1") / (Decimal("1") + PAYOUT_NET))  # 20/37 = 0.5405405405405406


# =====================================================================
# Step 1: SHA256 Hash & Opportunity Ledger Integrity Check
# =====================================================================

def compute_sha256(path: Path) -> str:
    """Compute SHA256 hex digest of a file in 1MB chunks."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_first_existing(candidates: list[Path], expected_sha: str | None = None) -> Path | None:
    """Return the first existing file path (preferring exact SHA256 match when specified)."""
    existing = [p for p in candidates if p.exists() and p.is_file()]
    if not existing:
        return None
    if expected_sha is not None:
        for p in existing:
            if compute_sha256(p) == expected_sha:
                return p
    return existing[0]


def verify_ledger_integrity(
    ledger_path: Path,
    strict_hash: bool = True,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Verify opportunity_ledger.csv hash, row counts, and state isolation counts."""
    ledger_sha = compute_sha256(ledger_path)
    hash_matched = ledger_sha == EXPECTED_LEDGER_SHA256
    if strict_hash and not hash_matched:
        raise ValueError(
            f"Ledger SHA256 mismatch: got {ledger_sha}, expected {EXPECTED_LEDGER_SHA256}"
        )

    df = pd.read_csv(ledger_path, keep_default_na=False)
    total_days = len(df)
    duplicate_dates = int(df["jst_date"].duplicated().sum())

    # Guard against outcome leakage inside Label-free ledger
    forbidden_cols = {"entry_points", "expiry_points", "forward_points", "win", "ev"}
    leaked_cols = sorted(forbidden_cols.intersection(df.columns))
    if leaked_cols:
        raise ValueError(f"Label-free ledger contains outcome columns: {leaked_cols}")

    stage_counts = {
        "break_found": int((df["break_found"].astype(str).str.lower() == "true").sum()),
        "reentry_found": int((df["reentry_found"].astype(str).str.lower() == "true").sum()),
        "retest_found": int((df["retest_found"].astype(str).str.lower() == "true").sum()),
    }
    state_counts = dict(Counter(df["state"]))

    # Verify Control I timestamp preservation across all reentry_found == True rows
    reentry_rows = df[df["reentry_found"].astype(str).str.lower() == "true"]
    control_i_preserved = int((reentry_rows["control_I_signal_at_csv"] != "").sum())

    # Split counts by IS (2015-01-07..2021-12-31) vs VIEWED_EVAL (2022-01-01..2026-09-09)
    df["period"] = np.where(df["jst_date"] <= IS_END_DATE, "IS", "VIEWED_EVAL")
    is_df = df[df["period"] == "IS"]
    is_state_counts = dict(Counter(is_df["state"]))
    is_stage_counts = {
        "calendar_days": int(len(is_df)),
        "break_found": int((is_df["break_found"].astype(str).str.lower() == "true").sum()),
        "reentry_found_control_I": int(
            (is_df["reentry_found"].astype(str).str.lower() == "true").sum()
        ),
        "retest_found": int((is_df["retest_found"].astype(str).str.lower() == "true").sum()),
        "candidate_R": int((is_df["candidate"] == "R").sum()),
        "candidate_B": int((is_df["candidate"] == "B").sum()),
        "boundary_draw_isolated": int((is_df["state"] == "BOUNDARY_DRAW").sum()),
        "invalid_range_gap_isolated": int((is_df["state"] == "INVALID_RANGE_GAP").sum()),
        "invalid_monitor_gap_isolated": int(
            (is_df["state"] == "INVALID_MONITOR_GAP_OR_PRICE").sum()
        ),
        "invalid_reentry_gap_isolated": int(
            (is_df["state"] == "INVALID_REENTRY_GAP_OR_PRICE").sum()
        ),
        "opposite_break_isolated": int((is_df["state"] == "OPPOSITE_BREAK").sum()),
        "outside_coverage_isolated": int(
            (is_df["state"] == "OUTSIDE_COMPLETE_FILE_COVERAGE").sum()
        ),
    }

    report = {
        "ledger_path": str(ledger_path.resolve()),
        "ledger_sha256": ledger_sha,
        "expected_ledger_sha256": EXPECTED_LEDGER_SHA256,
        "sha256_matched": hash_matched,
        "total_calendar_days": total_days,
        "expected_calendar_days": EXPECTED_LEDGER_DAYS,
        "duplicate_jst_dates": duplicate_dates,
        "label_free_verified": len(leaked_cols) == 0,
        "all_period_stage_counts": stage_counts,
        "expected_stage_counts_matched": stage_counts == EXPECTED_STAGE_COUNTS,
        "control_I_non_destructive_count": control_i_preserved,
        "control_I_preservation_matched": control_i_preserved == stage_counts["reentry_found"],
        "all_period_state_counts": state_counts,
        "expected_state_counts_matched": state_counts == EXPECTED_STATE_COUNTS,
        "in_sample_summary": is_stage_counts,
        "in_sample_state_counts": is_state_counts,
    }
    return df, report


# =====================================================================
# Step 2: Contract v0.5 Exact Price Check, Outcome & Newey-West HAC
# =====================================================================

def decimal_points_exact(d: Decimal) -> int:
    """Convert finite Decimal price to exact 1e-5 integer points (int64) without rounding."""
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
    if len(digits) + power > 19:
        raise ValueError("INT64_RANGE")
    coefficient = 0
    for digit in digits:
        coefficient = coefficient * 10 + digit
    value = coefficient * (10 ** power)
    if sign:
        value = -value
    if not (-(2 ** 63) <= value < (2 ** 63)):
        raise ValueError("INT64_RANGE")
    return value


def check_ohlc_bar(raw_ohlc: list[str]) -> tuple[list[int], set[str]]:
    """Validate OHLC strings against exact 1e-5 grid, positivity, and OHLC ordering."""
    reasons: set[str] = set()
    points: list[int] = []
    for s in raw_ohlc:
        try:
            d = Decimal(s)
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
            reasons.add("OHLC")
    return points, reasons


def compute_newey_west_stats(ev_series: list[float] | np.ndarray) -> dict[str, Any]:
    """Compute Newey-West HAC (lag=1, Bartlett, small-sample correction) and 97.5% CLB."""
    ans: dict[str, Any] = {
        "n": 0,
        "ev": None,
        "se_hac": None,
        "lower_97_5": None,
        "t_stat_ev_gt_0": None,
        "status": "HOLD",
        "hold_reason": None,
    }
    stage = "INPUT"
    try:
        x = np.asarray(ev_series, dtype=float)
        n = int(len(x))
        ans["n"] = n
        if x.ndim != 1:
            ans["hold_reason"] = "INVALID_SAMPLE_SHAPE"
            return ans
        if not np.all(np.isfinite(x)):
            ans["hold_reason"] = "NONFINITE_SAMPLE"
            return ans
        ans["ev"] = float(x.mean()) if n > 0 else None
        if n < 2:
            ans["hold_reason"] = "INSUFFICIENT_N"
            return ans
        if not np.isfinite(ans["ev"]):
            ans["ev"] = None
            ans["hold_reason"] = "NONFINITE_MEAN"
            return ans
        if np.ptp(x) == 0:
            ans["hold_reason"] = "ZERO_VARIANCE"
            return ans

        # Exact lag=1 Bartlett HAC variance with n/(n-1) finite-sample correction
        stage = "HAC"
        u = x - x.mean()
        v = float((np.dot(u, u) + np.dot(u[1:], u[:-1])) / (n ** 2) * (n / (n - 1)))
        if not np.isfinite(v) or v <= 0:
            ans["hold_reason"] = "NONFINITE_OR_NONPOSITIVE_SE"
            return ans
        se = float(np.sqrt(v))

        # When statsmodels is installed, cross-check against cov_hac(nlags=1, Bartlett)
        if HAS_STATSMODELS:
            stage = "OLS_HAC_CROSSCHECK"
            fit = sm.OLS(x, np.ones((n, 1))).fit()
            se_sm = float(
                np.sqrt(
                    cov_hac(
                        fit,
                        nlags=1,
                        weights_func=weights_bartlett,
                        use_correction=True,
                    )[0, 0]
                )
            )
            if not np.isfinite(se_sm) or se_sm <= 0:
                ans["hold_reason"] = "NONFINITE_OR_NONPOSITIVE_SE"
                return ans
            if not np.isclose(se_sm ** 2, v, rtol=1e-10, atol=1e-12):
                ans["hold_reason"] = "HAC_CROSSCHECK_FAILED"
                return ans
            se = se_sm

        stage = "CRITICAL_VALUE"
        critical = float(student_t.ppf(0.975, n - 1))
        if not np.isfinite(critical):
            ans["hold_reason"] = "NONFINITE_CRITICAL"
            return ans

        stage = "LOWER_BOUND"
        low = float(x.mean() - critical * se)
        t_stat = float(x.mean() / se)
        if not np.isfinite(low):
            ans["hold_reason"] = "NONFINITE_LOWER"
            return ans

        ans.update(
            se_hac=se,
            lower_97_5=low,
            t_stat_ev_gt_0=t_stat,
            status="REFERENCE_POSITIVE" if low > 0 else "NOT_ABOVE_ZERO",
        )
        return ans
    except Exception as exc:
        ans["hold_reason"] = f"{stage}_EXCEPTION:{type(exc).__name__}"
        return ans


def build_is_opportunities(ledger_df: pd.DataFrame) -> list[dict[str, Any]]:
    """Extract In-Sample (2015-01-07..2021-12-31) opportunities with feature metadata."""
    is_df = ledger_df[
        (ledger_df["jst_date"] >= IS_START_DATE) & (ledger_df["jst_date"] <= IS_END_DATE)
    ]
    opportunities: list[dict[str, Any]] = []
    for r in is_df.to_dict("records"):
        range_pts = int(r["range_points"]) if str(r.get("range_points", "")) != "" else None
        reentry_bars = (
            int(r["bars_to_reentry"]) if str(r.get("bars_to_reentry", "")) != "" else None
        )
        retest_bars = (
            int(r["bars_to_retest"]) if str(r.get("bars_to_retest", "")) != "" else None
        )
        reentry_depth = (
            int(r["reentry_depth_points"])
            if str(r.get("reentry_depth_points", "")) != ""
            else None
        )

        # Control I (independent reentry signal timestamp)
        if str(r["reentry_found"]).lower() == "true":
            entry_dt = datetime.fromisoformat(r["reentry_csv_open_time"]) + timedelta(minutes=1)
            assert entry_dt.isoformat() == r["control_I_signal_at_csv"], (
                f"Control I timestamp mismatch on {r['jst_date']}"
            )
            opportunities.append(
                {
                    "date": r["jst_date"],
                    "year": r["jst_date"][:4],
                    "period": "IS",
                    "group": "I",
                    "direction": r["control_I_direction"],
                    "entry_dt": entry_dt,
                    "range_points": range_pts,
                    "bars_to_reentry": reentry_bars,
                    "bars_to_retest": None,
                    "reentry_depth_points": reentry_depth,
                }
            )

        # Candidate R or B (retest signal timestamp)
        if r["candidate"] in ("R", "B"):
            entry_dt = datetime.fromisoformat(r["retest_csv_open_time"]) + timedelta(minutes=1)
            assert (
                entry_dt.isoformat()
                == r["scheduled_entry_time_csv"]
                == r["signal_available_at_csv"]
            ), f"Candidate entry timestamp mismatch on {r['jst_date']}"
            assert (entry_dt + timedelta(minutes=5)).isoformat() == r[
                "scheduled_expiry_time_csv"
            ], f"Candidate expiry timestamp mismatch on {r['jst_date']}"
            opportunities.append(
                {
                    "date": r["jst_date"],
                    "year": r["jst_date"][:4],
                    "period": "IS",
                    "group": r["candidate"],
                    "direction": r["signal_direction"],
                    "entry_dt": entry_dt,
                    "range_points": range_pts,
                    "bars_to_reentry": reentry_bars,
                    "bars_to_retest": retest_bars,
                    "reentry_depth_points": reentry_depth,
                }
            )
    return opportunities


def load_required_source_bars(
    source_path: Path,
    required_timestamps: set[datetime],
    strict_hash: bool = True,
) -> tuple[dict[datetime, tuple[list[int], set[str]]], Counter, dict[str, Any]]:
    """Scan EURUSD1.csv, verify SHA256 & row count, and inspect required 6-bar windows."""
    source_sha = compute_sha256(source_path)
    hash_matched = source_sha == EXPECTED_SOURCE_SHA256
    if strict_hash and not hash_matched:
        raise ValueError(
            f"Source SHA256 mismatch: got {source_sha}, expected {EXPECTED_SOURCE_SHA256}"
        )

    bars: dict[datetime, tuple[list[int], set[str]]] = {}
    counts: Counter = Counter()
    rows = 0
    with source_path.open(encoding="utf-8-sig", newline="") as f:
        for r in csv.reader(f):
            rows += 1
            if len(r) != 7:
                raise ValueError(f"Malformed source row at line {rows}: expected 7 columns")
            dt = datetime.fromisoformat(r[0].replace(".", "-") + "T" + r[1] + ":00")
            if dt in required_timestamps:
                counts[dt] += 1
                bars[dt] = check_ohlc_bar(r[2:6])

    if strict_hash and rows != EXPECTED_SOURCE_ROWS:
        raise ValueError(f"Source row count mismatch: got {rows}, expected {EXPECTED_SOURCE_ROWS}")

    meta = {
        "mode": "raw_source_m1",
        "source_path": str(source_path.resolve()),
        "source_sha256": source_sha,
        "expected_source_sha256": EXPECTED_SOURCE_SHA256,
        "sha256_matched": hash_matched,
        "source_rows": rows,
        "required_timestamps_count": len(required_timestamps),
    }
    return bars, counts, meta


def load_is_trades_from_outcomes(
    outcomes_path: Path,
    is_opps: list[dict[str, Any]],
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Join verified outcomes.csv with IS opportunity feature metadata from ledger."""
    outcomes_sha = compute_sha256(outcomes_path)
    raw_df = pd.read_csv(outcomes_path, keep_default_na=False)
    is_raw = raw_df[raw_df["period"] == "IS"].copy()

    opp_df = pd.DataFrame(is_opps)
    opp_df["entry_csv"] = opp_df["entry_dt"].apply(lambda d: d.isoformat())

    merged = opp_df.merge(
        is_raw,
        on=["date", "period", "group", "direction", "entry_csv"],
        how="inner",
        validate="one_to_one",
    )
    assert len(merged) == len(opp_df) == len(is_raw), (
        f"IS opportunity merge mismatch: {len(merged)} vs {len(opp_df)} vs {len(is_raw)}"
    )

    merged["valid"] = merged["valid"].astype(str).str.lower() == "true"
    for col in ("entry_points", "expiry_points", "forward_points"):
        merged[col] = merged[col].apply(lambda v: int(float(v)) if str(v) != "" else None)
    merged["win"] = merged["win"].apply(
        lambda v: (str(v).lower() == "true") if str(v) != "" else None
    )
    merged["raw_draw"] = merged["raw_draw"].apply(
        lambda v: (str(v).lower() == "true") if str(v) != "" else None
    )
    merged["ev"] = merged["ev"].apply(lambda v: float(v) if str(v) != "" else None)

    # Independent verification of integer point differences and EV
    valid_rows = merged[merged["valid"]]
    for r in valid_rows.to_dict("records"):
        diff = (int(r["expiry_points"]) - int(r["entry_points"])) * (
            1 if r["direction"] == "HIGH" else -1
        )
        assert diff == int(r["forward_points"]), f"Forward points mismatch on {r['date']}"
        assert (diff > 1) == bool(r["win"]), f"Win flag mismatch on {r['date']}"
        assert (diff == 0) == bool(r["raw_draw"]), f"Draw flag mismatch on {r['date']}"
        expected_ev = float(PAYOUT_NET) if diff > 1 else float(LOSS_NET)
        assert np.isclose(float(r["ev"]), expected_ev), f"EV mismatch on {r['date']}"

    merged = merged.sort_values(["entry_csv", "group"]).reset_index(drop=True)
    meta = {
        "mode": "verified_outcomes_csv",
        "outcomes_path": str(outcomes_path.resolve()),
        "outcomes_sha256": outcomes_sha,
        "expected_outcomes_sha256": EXPECTED_OUTCOMES_SHA256,
        "total_outcomes_rows": int(len(raw_df)),
        "is_outcomes_rows": int(len(merged)),
        "viewed_eval_rows_masked": int(len(raw_df) - len(merged)),
    }
    return merged, meta


def evaluate_is_trades(
    opportunities: list[dict[str, Any]],
    bars: dict[datetime, tuple[list[int], set[str]]],
    counts: Counter,
    stress_points: int = 1,
) -> pd.DataFrame:
    """Evaluate 6-minute continuity and outcomes under specified stress_points."""
    out: list[dict[str, Any]] = []
    for a in opportunities:
        reasons: set[str] = set()
        for i in range(6):
            dt = a["entry_dt"] + timedelta(minutes=i)
            if not counts[dt]:
                reasons.add("MISSING_BAR")
            elif counts[dt] > 1:
                reasons.add("DUPLICATE_TIME")
            if dt in bars:
                reasons.update(bars[dt][1])

        valid = len(reasons) == 0
        row: dict[str, Any] = {
            "date": a["date"],
            "year": a["year"],
            "period": a["period"],
            "group": a["group"],
            "direction": a["direction"],
            "entry_csv": a["entry_dt"].isoformat(),
            "expiry_csv": (a["entry_dt"] + timedelta(minutes=5)).isoformat(),
            "range_points": a["range_points"],
            "bars_to_reentry": a["bars_to_reentry"],
            "bars_to_retest": a["bars_to_retest"],
            "reentry_depth_points": a["reentry_depth_points"],
            "valid": valid,
            "invalid_reasons": "|".join(sorted(reasons)),
            "entry_points": None,
            "expiry_points": None,
            "forward_points": None,
            "win": None,
            "raw_draw": None,
            "ev": None,
        }
        if valid:
            ep = bars[a["entry_dt"]][0][0]
            xp = bars[a["entry_dt"] + timedelta(minutes=5)][0][0]
            assert a["direction"] in ("HIGH", "LOW")
            diff = (xp - ep) * (1 if a["direction"] == "HIGH" else -1)
            win = diff > stress_points
            ev = float(PAYOUT_NET) if win else float(LOSS_NET)
            row.update(
                entry_points=ep,
                expiry_points=xp,
                forward_points=diff,
                win=win,
                raw_draw=(diff == 0),
                ev=ev,
            )
        out.append(row)

    trades_df = pd.DataFrame(out).sort_values(["entry_csv", "group"]).reset_index(drop=True)
    return trades_df


def summarize_is_performance(trades_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compute standalone group stats (I, R, B) and same-day paired comparisons (R-I, B-I)."""
    standalone_rows: list[dict[str, Any]] = []
    for group in ("I", "R", "B"):
        g = trades_df[trades_df["group"] == group].sort_values("entry_csv")
        valid = g[g["valid"]]
        s = compute_newey_west_stats(valid["ev"].to_numpy(dtype=float))
        win_rate = float(valid["win"].mean()) if len(valid) > 0 else None
        one_pt_draws = int((valid["forward_points"] == 1).sum()) if len(valid) > 0 else 0
        standalone_rows.append(
            {
                "period": "IS",
                "group": group,
                "candidates": int(len(g)),
                "valid": int(len(valid)),
                "invalid": int(len(g) - len(valid)),
                "wins": int(valid["win"].sum()) if len(valid) > 0 else 0,
                "losses": int(len(valid) - valid["win"].sum()) if len(valid) > 0 else 0,
                "raw_draws_0pt": int(valid["raw_draw"].sum()) if len(valid) > 0 else 0,
                "stress_losses_1pt": one_pt_draws,
                "win_rate": win_rate,
                "breakeven_margin_pct": (
                    (win_rate - BREAKEVEN_WIN_RATE) * 100.0 if win_rate is not None else None
                ),
                "ev": s["ev"],
                "se_hac": s["se_hac"],
                "lower_97_5": s["lower_97_5"],
                "t_stat_ev_gt_0": s["t_stat_ev_gt_0"],
                "status": s["status"],
                "hold_reason": s["hold_reason"],
                "invalid_reasons": json.dumps(
                    dict(
                        Counter(
                            z
                            for reason_str in g["invalid_reasons"]
                            for z in str(reason_str).split("|")
                            if z
                        )
                    ),
                    ensure_ascii=False,
                ),
            }
        )

    paired_rows: list[dict[str, Any]] = []
    co = trades_df[trades_df["group"] == "I"]
    for group in ("R", "B"):
        ca = trades_df[trades_df["group"] == group]
        paired = ca.merge(
            co,
            on=["date", "period"],
            suffixes=("_candidate", "_I"),
            validate="one_to_one",
        )
        assert len(paired) == len(ca)
        paired["pair_valid"] = paired["valid_candidate"] & paired["valid_I"]
        valid_pairs = paired[paired["pair_valid"]].sort_values("entry_csv_candidate")
        ev_diff = (
            valid_pairs["ev_candidate"].to_numpy(dtype=float)
            - valid_pairs["ev_I"].to_numpy(dtype=float)
        )
        s = compute_newey_west_stats(ev_diff)
        paired_rows.append(
            {
                "period": "IS",
                "comparison": f"{group}_minus_I_same_day",
                "group": group,
                "total_pairs": int(len(paired)),
                "valid_pairs": int(len(valid_pairs)),
                "candidate_only_invalid": int(
                    (~paired["valid_candidate"] & paired["valid_I"]).sum()
                ),
                "I_only_invalid": int(
                    (paired["valid_candidate"] & ~paired["valid_I"]).sum()
                ),
                "both_invalid": int(
                    (~paired["valid_candidate"] & ~paired["valid_I"]).sum()
                ),
                "mean_ev_candidate": (
                    float(valid_pairs["ev_candidate"].mean()) if len(valid_pairs) > 0 else None
                ),
                "mean_ev_control_I": (
                    float(valid_pairs["ev_I"].mean()) if len(valid_pairs) > 0 else None
                ),
                "ev_diff_mean": s["ev"],
                "se_hac_diff": s["se_hac"],
                "lower_97_5_diff": s["lower_97_5"],
                "t_stat_diff_gt_0": s["t_stat_ev_gt_0"],
                "status": s["status"],
                "hold_reason": s["hold_reason"],
            }
        )

    return pd.DataFrame(standalone_rows), pd.DataFrame(paired_rows)


# =====================================================================
# Step 3: Neighborhood Parameter Grid & Spread Stress Plateau Analysis
# =====================================================================

DEFAULT_RANGE_MIN_GRID = (0, 100, 150, 200)          # in points (0, 10, 15, 20 pips)
DEFAULT_RANGE_MAX_GRID = (350, 400, 450, 999_999)    # in points (35, 40, 45, inf pips)
DEFAULT_MAX_REENTRY_BARS_GRID = (1, 2, 3)            # minutes (3 = full unfiltered window)
DEFAULT_MAX_RETEST_BARS_GRID = (2, 3, 4, 5)          # minutes (5 = full unfiltered window)
DEFAULT_STRESS_POINTS_GRID = (1, 2, 3)               # +0.1 pip, +0.2 pip, +0.3 pip


def evaluate_cell_metrics(
    sub_df: pd.DataFrame,
    stress_points: int,
) -> dict[str, Any]:
    """Compute win rate, exact EV, and Newey-West HAC stats for a subset at given stress_points."""
    valid = sub_df[sub_df["valid"]].sort_values("entry_csv")
    n_valid = int(len(valid))
    if n_valid == 0:
        return {
            "n_valid": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": None,
            "ev": None,
            "se_hac": None,
            "lower_97_5": None,
            "exceeds_breakeven": False,
            "clb_positive": False,
        }
    diff = valid["forward_points"].to_numpy(dtype=int)
    wins_mask = diff > stress_points
    ev_arr = np.where(wins_mask, float(PAYOUT_NET), float(LOSS_NET))
    wins = int(wins_mask.sum())
    losses = n_valid - wins
    win_rate = float(wins / n_valid)
    # Exact integer break-even check: wins * 85 - losses * 100 > 0 (i.e. wins * 185 > n_valid * 100)
    exact_ev = float((Decimal(wins) * PAYOUT_NET + Decimal(losses) * LOSS_NET) / Decimal(n_valid))
    exceeds_be = (wins * 185) > (n_valid * 100)
    hac = compute_newey_west_stats(ev_arr)
    return {
        "n_valid": n_valid,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate,
        "ev": exact_ev,
        "se_hac": hac["se_hac"],
        "lower_97_5": hac["lower_97_5"],
        "exceeds_breakeven": bool(exceeds_be),
        "clb_positive": bool(hac["lower_97_5"] is not None and hac["lower_97_5"] > 0),
    }


def run_plateau_grid_analysis(
    trades_df: pd.DataFrame,
    range_min_grid: tuple[int, ...] = DEFAULT_RANGE_MIN_GRID,
    range_max_grid: tuple[int, ...] = DEFAULT_RANGE_MAX_GRID,
    max_reentry_grid: tuple[int, ...] = DEFAULT_MAX_REENTRY_BARS_GRID,
    max_retest_grid: tuple[int, ...] = DEFAULT_MAX_RETEST_BARS_GRID,
    stress_grid: tuple[int, ...] = DEFAULT_STRESS_POINTS_GRID,
    min_cell_n: int = 30,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Evaluate 4D parameter grid across +0.1..+0.3 pip stress and classify Plateau stability."""
    grid_coords = list(
        itertools.product(
            range(len(range_min_grid)),
            range(len(range_max_grid)),
            range(len(max_reentry_grid)),
            range(len(max_retest_grid)),
        )
    )

    records: list[dict[str, Any]] = []
    for group in ("I", "R", "B"):
        g_df = trades_df[trades_df["group"] == group]
        cell_lookup: dict[tuple[int, int, int, int], dict[int, dict[str, Any]]] = {}

        for coord in grid_coords:
            i_rmin, i_rmax, i_re, i_rt = coord
            r_min = range_min_grid[i_rmin]
            r_max = range_max_grid[i_rmax]
            max_re = max_reentry_grid[i_re]
            max_rt = max_retest_grid[i_rt]

            if group == "I" and max_rt != max(max_retest_grid):
                continue

            mask = (
                (g_df["range_points"] >= r_min)
                & (g_df["range_points"] <= r_max)
                & (g_df["bars_to_reentry"] <= max_re)
            )
            if group in ("R", "B"):
                mask = mask & (g_df["bars_to_retest"] <= max_rt)

            sub_df = g_df[mask]
            cell_lookup[coord] = {
                sp: evaluate_cell_metrics(sub_df, stress_points=sp) for sp in stress_grid
            }

        for coord, stress_map in cell_lookup.items():
            i_rmin, i_rmax, i_re, i_rt = coord
            neighbors: list[tuple[int, int, int, int]] = []
            for other in cell_lookup:
                l1_dist = (
                    abs(other[0] - i_rmin)
                    + abs(other[1] - i_rmax)
                    + abs(other[2] - i_re)
                    + abs(other[3] - i_rt)
                )
                if l1_dist == 1:
                    neighbors.append(other)

            neighbor_be_flags = [
                cell_lookup[nb][1]["exceeds_breakeven"]
                for nb in neighbors
                if cell_lookup[nb][1]["n_valid"] > 0
            ]
            neighbor_be_ratio = (
                float(sum(neighbor_be_flags) / len(neighbor_be_flags))
                if neighbor_be_flags
                else 0.0
            )

            m1 = stress_map[1]  # +0.1 pip
            m2 = stress_map.get(2, {})  # +0.2 pip
            m3 = stress_map.get(3, {})  # +0.3 pip

            if not m1["exceeds_breakeven"]:
                p_class = "BELOW_BREAKEVEN"
            elif (
                m1["n_valid"] >= min_cell_n
                and m2.get("exceeds_breakeven", False)
                and neighbor_be_ratio >= 0.75
            ):
                p_class = "STABLE_PLATEAU"
            elif m1["n_valid"] >= min_cell_n and neighbor_be_ratio >= 0.50:
                p_class = "MODERATE_REGION"
            else:
                p_class = "ISOLATED_PEAK_WARNING"

            records.append(
                {
                    "group": group,
                    "range_min_pts": range_min_grid[i_rmin],
                    "range_max_pts": range_max_grid[i_rmax],
                    "max_reentry_bars": max_reentry_grid[i_re],
                    "max_retest_bars": max_retest_grid[i_rt] if group != "I" else None,
                    "n_valid": m1["n_valid"],
                    "win_rate_01pip": m1["win_rate"],
                    "ev_01pip": m1["ev"],
                    "se_hac_01pip": m1["se_hac"],
                    "clb975_01pip": m1["lower_97_5"],
                    "win_rate_02pip": m2.get("win_rate"),
                    "ev_02pip": m2.get("ev"),
                    "clb975_02pip": m2.get("lower_97_5"),
                    "win_rate_03pip": m3.get("win_rate"),
                    "ev_03pip": m3.get("ev"),
                    "clb975_03pip": m3.get("lower_97_5"),
                    "l1_neighbors_count": len(neighbor_be_flags),
                    "neighbor_be_ratio_01pip": neighbor_be_ratio,
                    "survives_02pip_be": bool(m2.get("exceeds_breakeven", False)),
                    "survives_03pip_be": bool(m3.get("exceeds_breakeven", False)),
                    "plateau_class": p_class,
                }
            )

    plateau_df = pd.DataFrame(records)
    audit_meta: dict[str, Any] = {
        "total_grid_cells_evaluated": int(len(plateau_df)),
        "stress_levels_evaluated_points": list(stress_grid),
        "total_cell_stress_evaluations": int(len(plateau_df) * len(stress_grid)),
        "breakeven_win_rate_threshold": BREAKEVEN_WIN_RATE,
        "min_cell_n_threshold": min_cell_n,
        "class_counts_by_group": {
            grp: dict(Counter(g["plateau_class"]))
            for grp, g in plateau_df.groupby("group")
        },
        "top_cells_by_group": {},
    }
    for grp, g in plateau_df.groupby("group"):
        valid_g = g[g["n_valid"] >= min_cell_n].sort_values("ev_01pip", ascending=False)
        audit_meta["top_cells_by_group"][grp] = valid_g.head(3).to_dict("records")

    return plateau_df, audit_meta


def summarize_yearly_stability(trades_df: pd.DataFrame, stress_points: int = 1) -> pd.DataFrame:
    """Break down IS performance by calendar year (2015..2021) for regime concentration audit."""
    rows: list[dict[str, Any]] = []
    for (group, year), g in trades_df.groupby(["group", "year"]):
        m = evaluate_cell_metrics(g, stress_points=stress_points)
        rows.append(
            {
                "group": group,
                "year": year,
                "candidates": int(len(g)),
                "n_valid": m["n_valid"],
                "wins": m["wins"],
                "losses": m["losses"],
                "win_rate": m["win_rate"],
                "ev": m["ev"],
                "exceeds_breakeven": m["exceeds_breakeven"],
            }
        )
    return pd.DataFrame(rows).sort_values(["group", "year"]).reset_index(drop=True)


# =====================================================================
# CLI Entry Point (Supports Zero-Argument Auto-Discovery)
# =====================================================================

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="BO-EUR-005 IS Statistical Verification & Plateau Analyzer (v2.4)"
    )
    src_group = parser.add_mutually_exclusive_group(required=False)
    src_group.add_argument("--source", type=Path, default=None, help="Path to raw EURUSD1.csv")
    src_group.add_argument(
        "--outcomes", type=Path, default=None, help="Path to verified outcomes.csv (fast mode)"
    )
    parser.add_argument(
        "--ledger",
        type=Path,
        required=False,
        default=None,
        help="Path to opportunity_ledger.csv (auto-discovered if omitted)",
    )
    parser.add_argument(
        "--contract",
        type=Path,
        required=False,
        default=None,
        help="Optional path to contract_v05.json (auto-discovered if omitted)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=False,
        default=None,
        help="New output directory (defaults to Gemini側必勝調査報告/機会台帳突合＆IS統計・Plateau検証/output_is_plateau_YYYYMMDD_HHMMSS)",
    )
    parser.add_argument(
        "--allow-custom-hash",
        action="store_true",
        help="Allow running on test/synthetic files whose SHA256 differs from frozen contract",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    # Auto-discover paths if omitted on CLI
    ledger_path = args.ledger or resolve_first_existing(
        CANDIDATE_LEDGER_PATHS, EXPECTED_LEDGER_SHA256
    )
    if ledger_path is None:
        raise FileNotFoundError(
            "opportunity_ledger.csv was not found in default paths. Please pass --ledger <path>."
        )

    outcomes_path = args.outcomes
    source_path = args.source
    if outcomes_path is None and source_path is None:
        outcomes_path = resolve_first_existing(
            CANDIDATE_OUTCOMES_PATHS, EXPECTED_OUTCOMES_SHA256
        )
        if outcomes_path is None:
            source_path = resolve_first_existing(
                CANDIDATE_SOURCE_PATHS, EXPECTED_SOURCE_SHA256
            )
        if outcomes_path is None and source_path is None:
            raise FileNotFoundError(
                "Neither outcomes.csv nor EURUSD1.csv was found in default paths. "
                "Please pass --outcomes <path> or --source <path>."
            )

    contract_path = args.contract or resolve_first_existing(
        CANDIDATE_CONTRACT_PATHS, EXPECTED_CONTRACT_SHA256
    )

    if args.output is not None:
        out_dir = args.output.resolve()
    else:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_root = DEFAULT_ARCHIVE_ROOT if DEFAULT_ARCHIVE_ROOT.exists() else Path.cwd()
        out_dir = (base_root / f"output_is_plateau_{stamp}").resolve()

    if out_dir.exists():
        raise FileExistsError(
            f"Output directory already exists (refusing to overwrite prior evidence): {out_dir}"
        )

    strict_hash = not args.allow_custom_hash

    contract_sha = None
    if contract_path is not None and contract_path.exists():
        contract_sha = compute_sha256(contract_path)
        if strict_hash and contract_sha != EXPECTED_CONTRACT_SHA256:
            raise ValueError(
                f"Contract SHA256 mismatch: got {contract_sha}, expected {EXPECTED_CONTRACT_SHA256}"
            )

    # 1. Verify Opportunity Ledger
    ledger_df, ledger_report = verify_ledger_integrity(ledger_path, strict_hash=strict_hash)

    # 2. Extract IS Opportunities & Evaluate or Join Outcomes
    is_opps = build_is_opportunities(ledger_df)
    if source_path is not None:
        required_ts = {
            a["entry_dt"] + timedelta(minutes=i) for a in is_opps for i in range(6)
        }
        bars, counts, source_meta = load_required_source_bars(
            source_path, required_ts, strict_hash=strict_hash
        )
        is_trades_df = evaluate_is_trades(is_opps, bars, counts, stress_points=1)
    else:
        assert outcomes_path is not None
        is_trades_df, source_meta = load_is_trades_from_outcomes(outcomes_path, is_opps)

    # 3. Summarize IS Baseline (+0.1 pip stress)
    standalone_summary_df, paired_summary_df = summarize_is_performance(is_trades_df)
    yearly_df = summarize_yearly_stability(is_trades_df, stress_points=1)

    # 4. Run Neighborhood Plateau & Spread Load (+0.1..+0.3 pip) Analysis
    plateau_df, plateau_meta = run_plateau_grid_analysis(is_trades_df)

    # 5. Write Outputs & Spark Audit Handover Manifest
    out_dir.mkdir(parents=True, exist_ok=False)
    is_trades_df.to_csv(out_dir / "is_outcomes.csv", index=False, encoding="utf-8-sig")
    standalone_summary_df.to_csv(
        out_dir / "is_standalone_summary.csv", index=False, encoding="utf-8-sig"
    )
    paired_summary_df.to_csv(
        out_dir / "is_paired_summary.csv", index=False, encoding="utf-8-sig"
    )
    yearly_df.to_csv(out_dir / "is_yearly_breakdown.csv", index=False, encoding="utf-8-sig")
    plateau_df.to_csv(out_dir / "is_plateau_grid.csv", index=False, encoding="utf-8-sig")

    handover_manifest = {
        "case_id": CASE_ID,
        "implementation_version": IMPLEMENTATION_VERSION,
        "script_sha256": compute_sha256(Path(__file__).resolve()),
        "runtime": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scipy": scipy.__version__,
            "statsmodels": (
                statsmodels.__version__
                if HAS_STATSMODELS
                else "not_installed_used_exact_algebraic_hac"
            ),
        },
        "evaluation_scope": {
            "in_sample_window": [IS_START_DATE, IS_END_DATE],
            "viewed_eval_masked": True,
            "breakeven_win_rate": BREAKEVEN_WIN_RATE,
            "payout_net": str(PAYOUT_NET),
            "baseline_stress_points": 1,
        },
        "contract_sha256": contract_sha,
        "ledger_integrity": ledger_report,
        "source_integrity": source_meta,
        "is_standalone_summary": standalone_summary_df.to_dict("records"),
        "is_paired_summary": paired_summary_df.to_dict("records"),
        "is_yearly_breakdown": yearly_df.to_dict("records"),
        "plateau_audit_metadata": plateau_meta,
    }
    (out_dir / "spark_audit_handover_manifest.json").write_text(
        json.dumps(handover_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"=== Output saved to: {out_dir} ===")
    print("=== [1] Opportunity Ledger Integrity Summary ===")
    print(json.dumps(ledger_report["in_sample_summary"], ensure_ascii=False, indent=2))
    print("\n=== [2] IS Standalone Performance (0.1 pip stress, tie=LOSE) ===")
    print(standalone_summary_df.to_string(index=False))
    print("\n=== [3] IS Same-Day Paired Comparison (Candidate - Control I) ===")
    print(paired_summary_df.to_string(index=False))
    print("\n=== [4] IS Yearly Breakdown ===")
    print(yearly_df.to_string(index=False))
    print("\n=== [5] IS Plateau Grid Summary ===")
    print(json.dumps(plateau_meta, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
