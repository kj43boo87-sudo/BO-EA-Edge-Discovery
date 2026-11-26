#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GSR-2026W49 Stage 1 (v1.0.2 - W48-Exact Cohort Contract, Calendar Gotobi Fix & tzdata Guard):
  - Track A: GSR-TKYFIX-002 One-Shot OOS (2022-01-01+) Pure Label-Free Opportunity Ledger
  - Track B: Multi-Fixing IS (2015-01-01 .. 2021-12-31) Pure Label-Free Opportunity Ledger
      * GSR-TKYFIX-003 (USDJPY M1, 09:55 JST)
      * GSR-LDNFIX-001 (EURUSD / GBPUSD M1, 16:00 Europe/London with strict BST/GMT DST)
      * GSR-NYCUT-001  (USDJPY / EURUSD M1, 10:00 America/New_York with strict EDT/EST DST)

Strict Compliance (v1.2):
  - Zero Proxy Constants / Zero Bin-Reverse Synthesis
  - Pure Label-Free Enforcement (ZERO Win/Loss or future return columns in output CSVs)
  - Track A & Track B Cohort Classification matches W47/W48 IS PASS Contract 100%:
      * is_cand = (wick_r >= 0.35 - 1e-9) or (bar_t_dir != move_dir)
      * not is_cand -> NONE / CONTROL_ONLY
      * is_cand and wick_r >= 0.25 - 1e-9 -> PURE_STRONG / CANDIDATE
      * is_cand and wick_r <  0.25 - 1e-9 -> WEAK_SUB / EXCLUDED_TRAP06
  - Real calendar arithmetic for Tokyo Gotobi (fixes non-leap Feb 28 Friday bug)
  - Track B strictly blocks 2022-01-01+ OOS (oos_locked: true)
  - Row-level exclusion audit log exported to exclusions_log_gsr_2026w49.csv
"""

import csv
import hashlib
import json
import os
import sys
from collections import Counter
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import numpy as np
import pandas as pd

SCRIPT_VERSION = "1.0.2"
CASE_ID = "GSR-2026W49"

try:
    TZ_UTC = ZoneInfo("UTC")
    TZ_TOKYO = ZoneInfo("Asia/Tokyo")
    TZ_LONDON = ZoneInfo("Europe/London")
    TZ_NY = ZoneInfo("America/New_York")
except ZoneInfoNotFoundError as exc:
    sys.stderr.write(
        "[ERROR] IANA タイムゾーンデータベース (tzdata) が見つかりません。\n"
        "Windows 環境では PowerShell で以下を実行してから再実行してください:\n"
        "    pip install tzdata\n"
        f"詳細: {exc}\n"
    )
    sys.exit(1)

DEFAULT_RAW_PATHS = {
    "USDJPY": r"G:\マイドライブ\通貨ペア\Dukascopy 1分足\USDJPY\2026.10.16USDJPY(3)-M1-No Session.csv",
    "EURUSD": r"G:\マイドライブ\通貨ペア\Dukascopy 1分足\EURUSD\2026.10.16EURUSD(5)-M1-No Session.csv",
    "GBPUSD": r"G:\マイドライブ\通貨ペア\Dukascopy 1分足\GBPUSD\2026.10.16GBPUSD(3)-M1-No Session.csv",
}
EXPECTED_RAW_SHA256 = {
    "USDJPY": "aa778785e1a0210a17b5a9c8198664cf34f698c139b02b92322118366e929c29",
    "EURUSD": "029bc12ccd4b244173cd9ed294c7dc8ec9f9b61cfd4499544722179158433a4d",
    "GBPUSD": "unknown",
}
PIP_SIZE_MAP = {
    "USDJPY": 0.01,
    "EURUSD": 0.0001,
    "GBPUSD": 0.0001,
}

DEFAULT_STAGE1_DIR = r"G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\トレード手法の市場調査＆データ点検"

IS_START_DATE = "2015-01-01"
IS_END_DATE = "2021-12-31"
OOS_START_DATE = "2022-01-01"


def compute_sha256(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def is_gotobi_tokyo(dt_jst_date) -> bool:
    """
    Real calendar-based Tokyo Gotobi check:
      - Any day with day % 5 == 0
      - Or Friday when Saturday (d + 1 day) or Sunday (d + 2 days) has day % 5 == 0
    Correctly handles non-leap Feb 28 (Fri) -> Sat Mar 1, Sun Mar 2 (False).
    """
    d = dt_jst_date.date() if isinstance(dt_jst_date, datetime) else dt_jst_date
    if d.day % 5 == 0:
        return True
    if d.weekday() == 4:  # Friday
        d_sat = d + timedelta(days=1)
        d_sun = d + timedelta(days=2)
        if (d_sat.day % 5 == 0) or (d_sun.day % 5 == 0):
            return True
    return False


def classify_wick_cohort(wick_r: float, bar_t_dir: int, move_dir: int) -> tuple:
    """
    W47/W48-exact cohort classification:
      - is_cand = (wick_r >= 0.35 - 1e-9) or (bar_t_dir != move_dir)
      - not is_cand -> ("NONE", "CONTROL_ONLY")
      - is_cand and wick_r >= 0.25 - 1e-9 -> ("PURE_STRONG", "CANDIDATE")
      - is_cand and wick_r <  0.25 - 1e-9 -> ("WEAK_SUB", "EXCLUDED_TRAP06")
    """
    is_cand = (wick_r >= 0.35 - 1e-9) or (bar_t_dir != move_dir)
    if not is_cand:
        return "NONE", "CONTROL_ONLY"
    if wick_r >= 0.25 - 1e-9:
        return "PURE_STRONG", "CANDIDATE"
    return "WEAK_SUB", "EXCLUDED_TRAP06"


def load_raw_m1_filtered(raw_csv_path: str, symbol: str, needed_utc_minutes: set) -> tuple:
    """
    Memory-efficient streaming loader that filters only bars whose UTC HH:MM falls in
    needed_utc_minutes. Splits rows strictly into IS (2015-01-01 .. 2021-12-31) and
    OOS (2022-01-01+).
    """
    if not os.path.exists(raw_csv_path):
        raise FileNotFoundError(f"Raw M1 CSV not found for {symbol}: {raw_csv_path}")

    raw_sha256 = compute_sha256(raw_csv_path)
    raw_bytes = os.path.getsize(raw_csv_path)
    pip_size = PIP_SIZE_MAP[symbol]

    total_raw_rows = 0
    dropped_pre_2015 = 0
    is_total_rows = 0
    oos_total_rows = 0
    ohlc_anomalies = 0
    is_min_dt = None
    is_max_dt = None
    oos_min_dt = None
    oos_max_dt = None

    is_kept = []
    oos_kept = []

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
            if d_iso < IS_START_DATE:
                dropped_pre_2015 += 1
                continue

            o = float(row[2])
            h = float(row[3])
            l = float(row[4])
            c = float(row[5])
            if h < l or o > h or o < l or c > h or c < l:
                ohlc_anomalies += 1
                continue

            dt_str = f"{d_iso} {t_raw}:00"
            is_oos = (d_iso >= OOS_START_DATE)
            if is_oos:
                oos_total_rows += 1
                if oos_min_dt is None:
                    oos_min_dt = dt_str
                oos_max_dt = dt_str
            else:
                is_total_rows += 1
                if is_min_dt is None:
                    is_min_dt = dt_str
                is_max_dt = dt_str

            if t_raw in needed_utc_minutes:
                rec = (dt_str, d_iso, f"{t_raw}:00", o, h, l, c, (h - l) / pip_size)
                if is_oos:
                    oos_kept.append(rec)
                else:
                    is_kept.append(rec)

    cols = ["dt_utc_str", "date_utc", "time_utc", "open", "high", "low", "close", "range_pips"]
    df_is = pd.DataFrame(is_kept, columns=cols)
    df_oos = pd.DataFrame(oos_kept, columns=cols)

    expected_sha = EXPECTED_RAW_SHA256.get(symbol, "unknown")
    audit = {
        "symbol": symbol,
        "file_path": raw_csv_path,
        "sha256": raw_sha256,
        "expected_sha256": expected_sha,
        "sha256_matches_expected": (raw_sha256 == expected_sha) if expected_sha != "unknown" else "NEWLY_RECORDED",
        "bytes": raw_bytes,
        "total_raw_rows": total_raw_rows,
        "dropped_pre_2015_rows": dropped_pre_2015,
        "is_2015_2021_total_rows": is_total_rows,
        "is_range_utc": [is_min_dt, is_max_dt],
        "oos_2022_plus_total_rows": oos_total_rows,
        "oos_range_utc": [oos_min_dt, oos_max_dt],
        "ohlc_anomalies_dropped": ohlc_anomalies,
    }
    return df_is, df_oos, audit


def build_utc_minute_set() -> set:
    """
    Collect all UTC HH:MM strings needed for:
      - Tokyo 09:54 JST (00:54 UTC): need 00:20 .. 01:04 UTC
      - London 15:59 Europe/London (BST=14:59 UTC, GMT=15:59 UTC): need 14:25 .. 16:05 UTC
      - NY 09:59 America/New_York (EDT=13:59 UTC, EST=14:59 UTC): need 13:25 .. 15:05 UTC
    """
    needed = set()
    t0 = datetime(2020, 1, 1, 0, 20)
    for m in range(45):
        needed.add((t0 + timedelta(minutes=m)).strftime("%H:%M"))
    t1 = datetime(2020, 1, 1, 13, 25)
    for m in range(166):
        needed.add((t1 + timedelta(minutes=m)).strftime("%H:%M"))
    return needed


def compute_window_features(bar_map: dict, sig_dt_utc: datetime, pip_size: float) -> dict:
    """
    Compute strictly Label-Free features using ONLY bars <= sig_dt_utc (available_at <= t).
    Also checks 6-minute continuity from t (sig_dt_utc) to t+6 (sig_dt_utc + 6m)
    WITHOUT reading or outputting any price/return from t+1..t+6.
    """
    atr_bars = []
    for k in range(-13, 1):
        dt_k = sig_dt_utc + timedelta(minutes=k)
        b = bar_map.get(dt_k)
        if b is None:
            return {"status": "MISSING_ATR_HISTORY", "m1_continuity_pass": False}
        atr_bars.append(b)

    atr14_pips = float(np.mean([b[4] for b in atr_bars]))
    if atr14_pips <= 0.0:
        return {"status": "ZERO_ATR14", "m1_continuity_pass": False}

    win_15 = []
    for k in range(-14, 1):
        dt_k = sig_dt_utc + timedelta(minutes=k)
        b = bar_map.get(dt_k)
        if b is None:
            return {"status": "MISSING_15M_WINDOW", "m1_continuity_pass": False}
        win_15.append(b)

    # Continuity check for t+1 .. t+6 (presence check only; ZERO price access)
    missing_fwd = []
    for k in range(1, 7):
        dt_k = sig_dt_utc + timedelta(minutes=k)
        if dt_k not in bar_map:
            missing_fwd.append(k)

    cont_pass = (len(missing_fwd) == 0)
    cont_status = "PASS_6BAR_COMPLETE" if cont_pass else f"FAIL_GAP_T+{','.join(map(str, missing_fwd))}"

    opens = [b[0] for b in win_15]
    highs = [b[1] for b in win_15]
    lows = [b[2] for b in win_15]
    closes = [b[3] for b in win_15]

    max_high = max(highs)
    min_low = min(lows)
    r15_price = max_high - min_low
    pre_15m_range_pips = r15_price / pip_size

    signed_move_price = closes[-1] - opens[0]
    pre_15m_body_pips = abs(signed_move_price) / pip_size
    move15m_atr = pre_15m_body_pips / atr14_pips

    bar_t_open, bar_t_high, bar_t_low, bar_t_close, _ = win_15[-1]
    bar_t_range = bar_t_high - bar_t_low
    bar_t_dir = 1 if bar_t_close > bar_t_open else (-1 if bar_t_close < bar_t_open else 0)

    if signed_move_price > 0:
        direction = "SELL"
        move_dir = 1
        s_t = 1.0
        counter_wick = bar_t_high - max(bar_t_open, bar_t_close)
        k_star = max(i for i, h in enumerate(highs) if h == max_high)
        e_star = max_high
        gamma = 0.5
    elif signed_move_price < 0:
        direction = "BUY"
        move_dir = -1
        s_t = -1.0
        counter_wick = min(bar_t_open, bar_t_close) - bar_t_low
        k_star = max(i for i, l in enumerate(lows) if l == min_low)
        e_star = min_low
        gamma = 2.0
    else:
        direction = "FLAT"
        move_dir = 0
        s_t = 0.0
        counter_wick = 0.0
        k_star = 14
        e_star = closes[-1]
        gamma = 1.0

    wick_rejection_ratio = (counter_wick / bar_t_range) if bar_t_range > 0 else 0.0

    if r15_price > 0 and s_t != 0.0:
        eta_range = abs(signed_move_price) / r15_price
        theta_peak = (14.0 - float(k_star)) / 14.0
        psi_reject = max(0.0, min(1.0, s_t * (e_star - closes[-1]) / r15_price))
        phi_urp = 4.0 * psi_reject * eta_range * ((1.0 - theta_peak) ** gamma)
    else:
        eta_range = 0.0
        theta_peak = 0.0
        psi_reject = 0.0
        phi_urp = 0.0

    return {
        "status": "OK",
        "direction": direction,
        "move_dir": move_dir,
        "bar_t_dir": bar_t_dir,
        "atr14_pips": round(atr14_pips, 4),
        "pre_15m_range_pips": round(pre_15m_range_pips, 4),
        "pre_15m_body_pips": round(pre_15m_body_pips, 4),
        "move15m_atr": round(move15m_atr, 4),
        "wick_rejection_ratio": round(wick_rejection_ratio, 4),
        "wick_rejection_ratio_raw": wick_rejection_ratio,
        "eta_range": round(eta_range, 6),
        "theta_peak": round(theta_peak, 6),
        "psi_reject": round(psi_reject, 6),
        "phi_urp": round(phi_urp, 6),
        "m1_continuity_pass": cont_pass,
        "continuity_6bar_status": cont_status,
    }


def build_bar_map(df: pd.DataFrame) -> dict:
    bar_map = {}
    for row in df.itertuples(index=False):
        dt_utc = datetime.strptime(row.dt_utc_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=TZ_UTC)
        bar_map[dt_utc] = (row.open, row.high, row.low, row.close, row.range_pips)
    return bar_map


def generate_track_a_oos(bar_map_usdjpy_oos: dict, out_csv_path: str) -> tuple:
    """
    Track A: GSR-TKYFIX-002 One-Shot OOS (2022-01-01+) Pure Label-Free Opportunity Ledger.
    Uses W47/W48-exact cohort classification (NONE / PURE_STRONG / WEAK_SUB).
    ZERO win/loss or future return columns.
    """
    all_dates = sorted({dt.date() for dt in bar_map_usdjpy_oos.keys() if dt.hour == 0 and dt.minute == 54})
    rows = []
    seq = 0
    exclusions = []

    for d in all_dates:
        sig_utc = datetime(d.year, d.month, d.day, 0, 54, 0, tzinfo=TZ_UTC)
        feat = compute_window_features(bar_map_usdjpy_oos, sig_utc, PIP_SIZE_MAP["USDJPY"])
        if feat["status"] != "OK":
            exclusions.append({
                "track": "TRACK_A_OOS",
                "case_id": "GSR-TKYFIX-002",
                "symbol": "USDJPY",
                "trade_date": d.isoformat(),
                "signal_utc": sig_utc.strftime("%Y-%m-%d %H:%M:%S"),
                "reason": feat["status"],
            })
            continue
        if feat["move15m_atr"] < 1.5 or feat["direction"] == "FLAT":
            continue

        if not feat["m1_continuity_pass"]:
            exclusions.append({
                "track": "TRACK_A_OOS",
                "case_id": "GSR-TKYFIX-002",
                "symbol": "USDJPY",
                "trade_date": d.isoformat(),
                "signal_utc": sig_utc.strftime("%Y-%m-%d %H:%M:%S"),
                "reason": feat["continuity_6bar_status"],
            })

        wick_r_raw = feat["wick_rejection_ratio_raw"]
        wick_grade, cohort_role = classify_wick_cohort(wick_r_raw, feat["bar_t_dir"], feat["move_dir"])
        is_wick_ge_025_uncond = (wick_r_raw >= 0.25 - 1e-9)

        seq += 1
        sig_jst = sig_utc.astimezone(TZ_TOKYO)
        entry_utc = sig_utc + timedelta(minutes=1)
        expiry_utc = sig_utc + timedelta(minutes=6)
        entry_jst = entry_utc.astimezone(TZ_TOKYO)
        expiry_jst = expiry_utc.astimezone(TZ_TOKYO)

        rows.append({
            "opportunity_id": f"GSR-TKYFIX-002-OOS-{seq:04d}",
            "case_id": "GSR-TKYFIX-002",
            "parent_case_id": "GSR-TKYFIX-001",
            "track": "TRACK_A_OOS",
            "symbol": "USDJPY",
            "trade_date": d.isoformat(),
            "decision_open_utc": (sig_utc - timedelta(minutes=14)).strftime("%Y-%m-%d %H:%M:%S"),
            "signal_utc": sig_utc.strftime("%Y-%m-%d %H:%M:%S"),
            "expected_entry_utc": entry_utc.strftime("%Y-%m-%d %H:%M:%S"),
            "expected_expiry_utc": expiry_utc.strftime("%Y-%m-%d %H:%M:%S"),
            "entry_time": entry_jst.strftime("%H:%M:%S"),
            "eval_end_time": expiry_jst.strftime("%H:%M:%S"),
            "direction": feat["direction"],
            "cohort_role": cohort_role,
            "wick_rejection_grade": wick_grade,
            "is_wick_ge_025_unconditional": is_wick_ge_025_uncond,
            "wick_rejection_ratio": feat["wick_rejection_ratio"],
            "pre_15m_range_pips": feat["pre_15m_range_pips"],
            "pre_15m_body_pips": feat["pre_15m_body_pips"],
            "atr14_pips": feat["atr14_pips"],
            "move15m_atr": feat["move15m_atr"],
            "day_of_week": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][sig_jst.weekday()],
            "gotobi_flag": is_gotobi_tokyo(sig_jst),
            "m1_continuity_pass": feat["m1_continuity_pass"],
            "continuity_6bar_status": feat["continuity_6bar_status"],
        })

    df_out = pd.DataFrame(rows)
    df_out.to_csv(out_csv_path, index=False)

    summary = {
        "file": os.path.basename(out_csv_path),
        "sha256": compute_sha256(out_csv_path),
        "bytes": os.path.getsize(out_csv_path),
        "label_free_columns_only": True,
        "w48_exact_cohort_contract": True,
        "total_pool_rows": len(df_out),
        "primary_pure_strong_rows": int((df_out["wick_rejection_grade"] == "PURE_STRONG").sum()) if len(df_out) else 0,
        "control_none_rows": int((df_out["wick_rejection_grade"] == "NONE").sum()) if len(df_out) else 0,
        "excluded_trap06_weak_sub_rows": int((df_out["wick_rejection_grade"] == "WEAK_SUB").sum()) if len(df_out) else 0,
        "continuity_pass_rows": int(df_out["m1_continuity_pass"].sum()) if len(df_out) else 0,
        "exclusions_count": len(exclusions),
        "exclusions_by_reason": dict(Counter(e["reason"] for e in exclusions)),
    }
    return summary, exclusions


def generate_track_b_is(bar_maps_is: dict, out_csv_path: str) -> tuple:
    """
    Track B: IS-Only (2015-01-01 .. 2021-12-31) Multi-Fixing Pure Label-Free Ledger.
    Uses the same W48-exact cohort classification across all sessions/symbols so
    ablation vs NONE (CONTROL_ONLY) is directly comparable.
    ZERO win/loss or future return columns.
    """
    specs = [
        ("GSR-TKYFIX-003", "USDJPY", TZ_TOKYO, 9, 54),
        ("GSR-LDNFIX-001", "EURUSD", TZ_LONDON, 15, 59),
        ("GSR-LDNFIX-001", "GBPUSD", TZ_LONDON, 15, 59),
        ("GSR-NYCUT-001", "USDJPY", TZ_NY, 9, 59),
        ("GSR-NYCUT-001", "EURUSD", TZ_NY, 9, 59),
    ]

    all_rows = []
    all_exclusions = []
    dst_audit = {}
    summary_by_candidate = {}

    for cand_id, symbol, local_tz, sig_h, sig_m in specs:
        bmap = bar_maps_is.get(symbol, {})
        if not bmap:
            continue

        d_cur = datetime(2015, 1, 1).date()
        d_end = datetime(2021, 12, 31).date()
        seq = 0
        offsets_seen = set()
        cand_exclusions = 0
        pass_cnt = 0
        grade_counts = Counter()

        while d_cur <= d_end:
            if d_cur.weekday() < 5:
                sig_local = datetime(d_cur.year, d_cur.month, d_cur.day, sig_h, sig_m, 0, tzinfo=local_tz)
                sig_utc = sig_local.astimezone(TZ_UTC)
                utc_offset_hrs = sig_local.utcoffset().total_seconds() / 3600.0
                offsets_seen.add(f"{sig_local.tzname()}(UTC{utc_offset_hrs:+.0f})")

                if sig_utc not in bmap:
                    cand_exclusions += 1
                    all_exclusions.append({
                        "track": "TRACK_B_IS",
                        "case_id": cand_id,
                        "symbol": symbol,
                        "trade_date": d_cur.isoformat(),
                        "signal_utc": sig_utc.strftime("%Y-%m-%d %H:%M:%S"),
                        "reason": "MISSING_SIGNAL_BAR_HOLIDAY_OR_GAP",
                    })
                else:
                    feat = compute_window_features(bmap, sig_utc, PIP_SIZE_MAP[symbol])
                    if feat["status"] != "OK":
                        cand_exclusions += 1
                        all_exclusions.append({
                            "track": "TRACK_B_IS",
                            "case_id": cand_id,
                            "symbol": symbol,
                            "trade_date": d_cur.isoformat(),
                            "signal_utc": sig_utc.strftime("%Y-%m-%d %H:%M:%S"),
                            "reason": feat["status"],
                        })
                    elif feat["move15m_atr"] >= 1.5 and feat["direction"] != "FLAT":
                        if feat["m1_continuity_pass"]:
                            pass_cnt += 1
                        else:
                            cand_exclusions += 1
                            all_exclusions.append({
                                "track": "TRACK_B_IS",
                                "case_id": cand_id,
                                "symbol": symbol,
                                "trade_date": d_cur.isoformat(),
                                "signal_utc": sig_utc.strftime("%Y-%m-%d %H:%M:%S"),
                                "reason": feat["continuity_6bar_status"],
                            })

                        seq += 1
                        entry_utc = sig_utc + timedelta(minutes=1)
                        expiry_utc = sig_utc + timedelta(minutes=6)
                        entry_local = entry_utc.astimezone(local_tz)
                        expiry_local = expiry_utc.astimezone(local_tz)

                        wick_r_raw = feat["wick_rejection_ratio_raw"]
                        wick_grade, cohort_role = classify_wick_cohort(wick_r_raw, feat["bar_t_dir"], feat["move_dir"])
                        is_wick_ge_025_uncond = (wick_r_raw >= 0.25 - 1e-9)
                        grade_counts[wick_grade] += 1

                        all_rows.append({
                            "opportunity_id": f"{cand_id}-{symbol}-{seq:04d}",
                            "case_id": cand_id,
                            "track": "TRACK_B_IS",
                            "symbol": symbol,
                            "local_tz": local_tz.key,
                            "dst_zone": sig_local.tzname(),
                            "utc_offset_hours": utc_offset_hrs,
                            "trade_date": d_cur.isoformat(),
                            "decision_open_utc": (sig_utc - timedelta(minutes=14)).strftime("%Y-%m-%d %H:%M:%S"),
                            "signal_utc": sig_utc.strftime("%Y-%m-%d %H:%M:%S"),
                            "expected_entry_utc": entry_utc.strftime("%Y-%m-%d %H:%M:%S"),
                            "expected_expiry_utc": expiry_utc.strftime("%Y-%m-%d %H:%M:%S"),
                            "entry_time_local": entry_local.strftime("%H:%M:%S"),
                            "eval_end_time_local": expiry_local.strftime("%H:%M:%S"),
                            "direction": feat["direction"],
                            "cohort_role": cohort_role,
                            "wick_rejection_grade": wick_grade,
                            "is_wick_ge_025_unconditional": is_wick_ge_025_uncond,
                            "wick_rejection_ratio": feat["wick_rejection_ratio"],
                            "pre_15m_range_pips": feat["pre_15m_range_pips"],
                            "pre_15m_body_pips": feat["pre_15m_body_pips"],
                            "atr14_pips": feat["atr14_pips"],
                            "move15m_atr": feat["move15m_atr"],
                            "eta_range": feat["eta_range"],
                            "theta_peak": feat["theta_peak"],
                            "psi_reject": feat["psi_reject"],
                            "phi_urp": feat["phi_urp"],
                            "day_of_week": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][d_cur.weekday()],
                            "gotobi_flag": is_gotobi_tokyo(d_cur) if cand_id == "GSR-TKYFIX-003" else False,
                            "m1_continuity_pass": feat["m1_continuity_pass"],
                            "continuity_6bar_status": feat["continuity_6bar_status"],
                        })
            d_cur += timedelta(days=1)

        key = f"{cand_id}|{symbol}"
        dst_audit[key] = sorted(offsets_seen)
        summary_by_candidate[key] = {
            "total_rows": seq,
            "continuity_pass_rows": pass_cnt,
            "grade_counts": dict(grade_counts),
            "exclusions": cand_exclusions,
        }

    df_out = pd.DataFrame(all_rows)
    df_out.to_csv(out_csv_path, index=False)

    summary = {
        "file": os.path.basename(out_csv_path),
        "sha256": compute_sha256(out_csv_path),
        "bytes": os.path.getsize(out_csv_path),
        "label_free_columns_only": True,
        "w48_exact_cohort_contract": True,
        "total_rows": len(df_out),
        "dst_offsets_verified": dst_audit,
        "summary_by_candidate": summary_by_candidate,
        "exclusions_count": len(all_exclusions),
        "exclusions_by_reason": dict(Counter(e["reason"] for e in all_exclusions)),
    }
    return summary, all_exclusions


def write_handover_markdown(manifest: dict, out_md_path: str):
    ra = manifest["track_a_oos_ledger"]
    rb = manifest["track_b_is_ledger"]
    aud = manifest["raw_m1_audits"]
    lines = [
        "# HANDOVER_GSR_2026W49_STAGE1 — 第1工程→第2工程 引き継ぎ書（ローカル全量実測確定版）",
        "",
        f"- **案件ID**: `{manifest['case_id']}`",
        f"- **実行日時 (JST)**: `{manifest['executed_at_jst']}`",
        f"- **スクリプト**: `profile_market_structure_gsr_2026w49_v1_0.py` (v{manifest['script_version']}, SHA256: `{manifest['script_sha256']}`)",
        "- **Label-Free純度**: 勝敗列・リターン列を物理的に一切含まない純粋Label-Free出力",
        "- **W48完全一致契約**: `is_cand = (wick_r >= 0.35 - 1e-9) or (bar_t_dir != move_dir)` により `NONE` / `PURE_STRONG` / `WEAK_SUB` を厳密分離",
        "",
        "## 1. 生M1データ全量監査ログ",
        "| 通貨ペア | Bytes | 総行数 | IS (2015–2021) 行数 | OOS (2022+) 行数 | SHA256 |",
        "| :--- | ---: | ---: | ---: | ---: | :--- |",
    ]
    for sym in ["USDJPY", "EURUSD", "GBPUSD"]:
        if sym in aud:
            a = aud[sym]
            lines.append(
                f"| {sym} | {a['bytes']:,} | {a['total_raw_rows']:,} | {a['is_2015_2021_total_rows']:,} | {a['oos_2022_plus_total_rows']:,} | `{a['sha256']}` |"
            )
    lines += [
        "",
        "## 2. Track A (`GSR-TKYFIX-002` One-Shot OOS) 出力確定",
        f"- **ファイル**: `{ra['file']}` (SHA256: `{ra['sha256']}`, {ra['bytes']:,} bytes)",
        f"- **プール総数**: {ra['total_pool_rows']} 件 / **主契約 `PURE_STRONG`**: {ra['primary_pure_strong_rows']} 件 / `NONE`: {ra['control_none_rows']} 件 / `EXCLUDED_TRAP06`: {ra['excluded_trap06_weak_sub_rows']} 件",
        f"- **6本連続性合格**: {ra['continuity_pass_rows']} 件 / **除外ログ件数**: {ra['exclusions_count']} 件 ({ra['exclusions_by_reason']})",
        "",
        "## 3. Track B (マルチ・フィキシング IS専用 / `oos_locked: true`) 出力確定",
        f"- **ファイル**: `{rb['file']}` (SHA256: `{rb['sha256']}`, {rb['bytes']:,} bytes)",
        f"- **総抽出行数**: {rb['total_rows']} 件 / **除外ログ件数**: {rb['exclusions_count']} 件 ({rb['exclusions_by_reason']})",
        f"- **候補別内訳**: `{json.dumps(rb['summary_by_candidate'], ensure_ascii=False)}`",
        f"- **DST変換確認**: `{json.dumps(rb['dst_offsets_verified'], ensure_ascii=False)}`",
        "",
        "## 4. 行単位除外監査ログ",
        f"- **ファイル**: `{manifest['exclusions_log']['file']}` (SHA256: `{manifest['exclusions_log']['sha256']}`, {manifest['exclusions_log']['total_rows']} 行)",
    ]
    with open(out_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    stage1_dir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_STAGE1_DIR
    os.makedirs(stage1_dir, exist_ok=True)
    needed_utc_mins = build_utc_minute_set()

    raw_audits = {}
    bar_maps_is = {}
    bar_map_usdjpy_oos = {}

    for symbol, path in DEFAULT_RAW_PATHS.items():
        df_is, df_oos, audit = load_raw_m1_filtered(path, symbol, needed_utc_mins)
        raw_audits[symbol] = audit
        bar_maps_is[symbol] = build_bar_map(df_is)
        if symbol == "USDJPY":
            bar_map_usdjpy_oos = build_bar_map(df_oos)

    out_a = os.path.join(stage1_dir, "oos_2022_2026_opportunity_ledger_gsr_tkyfix002_gsr_2026w49.csv")
    out_b = os.path.join(stage1_dir, "is_2015_2021_opportunity_ledger_multifix_gsr_2026w49.csv")
    out_excl = os.path.join(stage1_dir, "exclusions_log_gsr_2026w49.csv")
    out_manifest = os.path.join(stage1_dir, "stage1_to_stage2_handover_manifest_gsr_2026w49.json")
    out_handover = os.path.join(stage1_dir, "HANDOVER_GSR_2026W49_STAGE1.md")

    res_a, excl_a = generate_track_a_oos(bar_map_usdjpy_oos, out_a)
    res_b, excl_b = generate_track_b_is(bar_maps_is, out_b)

    all_excl = excl_a + excl_b
    pd.DataFrame(
        all_excl,
        columns=["track", "case_id", "symbol", "trade_date", "signal_utc", "reason"],
    ).to_csv(out_excl, index=False)

    manifest = {
        "manifest_version": "1.2.2",
        "script_version": SCRIPT_VERSION,
        "case_id": CASE_ID,
        "executed_at_jst": datetime.now(TZ_TOKYO).isoformat(timespec="seconds"),
        "oos_locked_for_track_b": True,
        "oos_authorized_for_track_a_only": True,
        "label_free_enforced": True,
        "zero_win_loss_columns": True,
        "w48_exact_cohort_contract": True,
        "raw_m1_audits": raw_audits,
        "track_a_oos_ledger": res_a,
        "track_b_is_ledger": res_b,
        "exclusions_log": {
            "file": os.path.basename(out_excl),
            "sha256": compute_sha256(out_excl),
            "bytes": os.path.getsize(out_excl),
            "total_rows": len(all_excl),
        },
        "script_sha256": compute_sha256(os.path.abspath(__file__)),
    }

    with open(out_manifest, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    write_handover_markdown(manifest, out_handover)
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
