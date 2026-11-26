#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GSR-2026W49 Stage 1:
  - Track A: GSR-TKYFIX-002 One-Shot OOS (2022-01-01+) Label-Free Opportunity Ledger
  - Track B: Multi-Fixing IS (2015-01-01 .. 2021-12-31) Label-Free Opportunity Ledger
      * GSR-TKYFIX-003 (USDJPY M1, 09:55 JST)
      * GSR-LDNFIX-001 (EURUSD / GBPUSD M1, 16:00 Europe/London with strict BST/GMT DST)
      * GSR-NYCUT-001  (USDJPY / EURUSD M1, 10:00 America/New_York with strict EDT/EST DST)

Strict Compliance (v1.2):
  - Zero Proxy Constants / Zero Bin-Reverse Synthesis
  - Label-Free Enforcement (HOLD_LABEL_FREE; zero Win/Loss or future return calculation)
  - Track B strictly blocks 2022-01-01+ OOS (oos_locked: true)
  - Track A strictly isolates 2022-01-01+ OOS for Stage 2 One-Shot evaluation
"""

import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
import numpy as np
import pandas as pd

SCRIPT_VERSION = "1.0.0"
CASE_ID = "GSR-2026W49"

TZ_UTC = ZoneInfo("UTC")
TZ_TOKYO = ZoneInfo("Asia/Tokyo")
TZ_LONDON = ZoneInfo("Europe/London")
TZ_NY = ZoneInfo("America/New_York")

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


def is_gotobi_tokyo(dt_jst_date: datetime) -> bool:
    day_num = dt_jst_date.day
    dow = dt_jst_date.weekday()  # 0=Mon..4=Fri
    if day_num % 5 == 0:
        return True
    if dow == 4 and ((day_num + 1) % 5 == 0 or (day_num + 2) % 5 == 0):
        return True
    return False


def load_raw_m1_filtered(raw_csv_path: str, symbol: str, needed_utc_minutes: set) -> tuple:
    """
    Memory-efficient streaming loader that filters only bars whose UTC HH:MM falls in
    needed_utc_minutes (plus computes rolling ATR14 across contiguous bars prior to signal).
    Splits rows strictly into IS (2015-01-01 .. 2021-12-31) and OOS (2022-01-01+).
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

            is_oos = (d_iso >= OOS_START_DATE)
            if is_oos:
                oos_total_rows += 1
            else:
                is_total_rows += 1

            if t_raw in needed_utc_minutes:
                rec = (f"{d_iso} {t_raw}:00", d_iso, f"{t_raw}:00", o, h, l, c, (h - l) / pip_size)
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
        "oos_2022_plus_total_rows": oos_total_rows,
        "ohlc_anomalies_dropped": ohlc_anomalies,
    }
    return df_is, df_oos, audit


def build_utc_minute_set() -> set:
    """
    Collect all UTC HH:MM strings needed for:
      - Tokyo 09:54 JST (00:54 UTC): need 00:20 .. 01:00 UTC
      - London 15:59 Europe/London (BST=14:59 UTC, GMT=15:59 UTC): need 14:25 .. 16:05 UTC
      - NY 09:59 America/New_York (EDT=13:59 UTC, EST=14:59 UTC): need 13:25 .. 15:05 UTC
    """
    needed = set()
    # Tokyo window: 00:20 .. 01:01 UTC
    t0 = datetime(2020, 1, 1, 0, 20)
    for m in range(45):
        needed.add((t0 + timedelta(minutes=m)).strftime("%H:%M"))
    # NY + London combined window: 13:25 .. 16:10 UTC
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
    # ATR14: 14 bars ending at sig_dt_utc inclusive (t-13 .. t)
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

    # 15-minute window: t-14 .. t (15 confirmed bars)
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

    if signed_move_price > 0:
        direction = "SELL"
        s_t = 1.0
        counter_wick = bar_t_high - max(bar_t_open, bar_t_close)
        # Last bar index reaching max_high
        k_star = max(i for i, h in enumerate(highs) if h == max_high)
        e_star = max_high
        gamma = 0.5
    elif signed_move_price < 0:
        direction = "BUY"
        s_t = -1.0
        counter_wick = min(bar_t_open, bar_t_close) - bar_t_low
        # Last bar index reaching min_low
        k_star = max(i for i, l in enumerate(lows) if l == min_low)
        e_star = min_low
        gamma = 2.0
    else:
        direction = "FLAT"
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
        "atr14_pips": round(atr14_pips, 4),
        "pre_15m_range_pips": round(pre_15m_range_pips, 4),
        "pre_15m_body_pips": round(pre_15m_body_pips, 4),
        "move15m_atr": round(move15m_atr, 4),
        "wick_rejection_ratio": round(wick_rejection_ratio, 4),
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


def generate_track_a_oos(bar_map_usdjpy_oos: dict, out_csv_path: str) -> dict:
    """
    Track A: GSR-TKYFIX-002 One-Shot OOS (2022-01-01+) Label-Free Opportunity Ledger.
    Contract (Locked):
      - Signal bar t: 00:54:00 UTC (09:54:00 JST)
      - Entry: 00:55:00 UTC (09:55:00 JST) -> Expiry: 01:00:00 UTC (10:00:00 JST)
      - Pool condition: pre_15m_body_pips / atr14_pips >= 1.5
      - Primary Contract: wick_rejection_ratio >= 0.25 (PURE_STRONG)
    """
    all_dates = sorted({dt.date() for dt in bar_map_usdjpy_oos.keys() if dt.hour == 0 and dt.minute == 54})
    rows = []
    seq = 0
    exclusions = []

    for d in all_dates:
        sig_utc = datetime(d.year, d.month, d.day, 0, 54, 0, tzinfo=TZ_UTC)
        feat = compute_window_features(bar_map_usdjpy_oos, sig_utc, PIP_SIZE_MAP["USDJPY"])
        if feat["status"] != "OK":
            exclusions.append({"trade_date": d.isoformat(), "reason": feat["status"]})
            continue
        if feat["move15m_atr"] < 1.5 or feat["direction"] == "FLAT":
            continue

        if not feat["m1_continuity_pass"]:
            exclusions.append({"trade_date": d.isoformat(), "reason": feat["continuity_6bar_status"]})

        wick_r = feat["wick_rejection_ratio"]
        if wick_r >= 0.25:
            wick_grade = "PURE_STRONG"
            cohort_role = "CANDIDATE"
        elif wick_r > 0.0:
            wick_grade = "WEAK_SUB"
            cohort_role = "EXCLUDED_TRAP06"
        else:
            wick_grade = "NONE"
            cohort_role = "CONTROL_ONLY"

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
            "wick_rejection_ratio": feat["wick_rejection_ratio"],
            "pre_15m_range_pips": feat["pre_15m_range_pips"],
            "pre_15m_body_pips": feat["pre_15m_body_pips"],
            "atr14_pips": feat["atr14_pips"],
            "move15m_atr": feat["move15m_atr"],
            "day_of_week": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][sig_jst.weekday()],
            "gotobi_flag": is_gotobi_tokyo(sig_jst),
            "m1_continuity_pass": feat["m1_continuity_pass"],
            "continuity_6bar_status": feat["continuity_6bar_status"],
            "win_loss_label": "HOLD_LABEL_FREE",
            "net_pips_result": "HOLD_LABEL_FREE",
        })

    df_out = pd.DataFrame(rows)
    df_out.to_csv(out_csv_path, index=False)

    return {
        "file": os.path.basename(out_csv_path),
        "sha256": compute_sha256(out_csv_path),
        "bytes": os.path.getsize(out_csv_path),
        "total_pool_rows": len(df_out),
        "primary_pure_strong_rows": int((df_out["wick_rejection_grade"] == "PURE_STRONG").sum()) if len(df_out) else 0,
        "control_none_rows": int((df_out["wick_rejection_grade"] == "NONE").sum()) if len(df_out) else 0,
        "excluded_trap06_weak_sub_rows": int((df_out["wick_rejection_grade"] == "WEAK_SUB").sum()) if len(df_out) else 0,
        "continuity_pass_rows": int(df_out["m1_continuity_pass"].sum()) if len(df_out) else 0,
        "exclusions_sample": exclusions[:20],
        "exclusions_count": len(exclusions),
    }


def generate_track_b_is(bar_maps_is: dict, out_csv_path: str) -> dict:
    """
    Track B: IS-Only (2015-01-01 .. 2021-12-31) Multi-Fixing Label-Free Ledger.
      - GSR-TKYFIX-003 (USDJPY, 09:54 JST signal -> 09:55 JST entry)
      - GSR-LDNFIX-001 (EURUSD / GBPUSD, 15:59 Europe/London signal -> 16:00 London entry, strict BST/GMT)
      - GSR-NYCUT-001  (USDJPY / EURUSD, 09:59 America/New_York signal -> 10:00 NY entry, strict EDT/EST)
    """
    specs = [
        ("GSR-TKYFIX-003", "USDJPY", TZ_TOKYO, 9, 54),
        ("GSR-LDNFIX-001", "EURUSD", TZ_LONDON, 15, 59),
        ("GSR-LDNFIX-001", "GBPUSD", TZ_LONDON, 15, 59),
        ("GSR-NYCUT-001", "USDJPY", TZ_NY, 9, 59),
        ("GSR-NYCUT-001", "EURUSD", TZ_NY, 9, 59),
    ]

    all_rows = []
    dst_audit = {}
    summary_by_candidate = {}

    for cand_id, symbol, local_tz, sig_h, sig_m in specs:
        bmap = bar_maps_is.get(symbol, {})
        if not bmap:
            continue

        # Enumerate IS calendar dates 2015-01-01 .. 2021-12-31
        d_cur = datetime(2015, 1, 1).date()
        d_end = datetime(2021, 12, 31).date()
        seq = 0
        offsets_seen = set()
        exclusions = 0
        pass_cnt = 0

        while d_cur <= d_end:
            if d_cur.weekday() < 5:  # Mon-Fri
                sig_local = datetime(d_cur.year, d_cur.month, d_cur.day, sig_h, sig_m, 0, tzinfo=local_tz)
                sig_utc = sig_local.astimezone(TZ_UTC)
                utc_offset_hrs = sig_local.utcoffset().total_seconds() / 3600.0
                offsets_seen.add(f"{sig_local.tzname()}(UTC{utc_offset_hrs:+.0f})")

                if sig_utc in bmap:
                    feat = compute_window_features(bmap, sig_utc, PIP_SIZE_MAP[symbol])
                    if feat["status"] != "OK":
                        exclusions += 1
                    elif feat["move15m_atr"] >= 1.5 and feat["direction"] != "FLAT":
                        if feat["m1_continuity_pass"]:
                            pass_cnt += 1
                        else:
                            exclusions += 1

                        seq += 1
                        entry_utc = sig_utc + timedelta(minutes=1)
                        expiry_utc = sig_utc + timedelta(minutes=6)
                        entry_local = entry_utc.astimezone(local_tz)
                        expiry_local = expiry_utc.astimezone(local_tz)

                        wick_r = feat["wick_rejection_ratio"]
                        if wick_r >= 0.25:
                            wick_grade = "PURE_STRONG"
                            cohort_role = "CANDIDATE"
                        elif wick_r > 0.0:
                            wick_grade = "WEAK_SUB"
                            cohort_role = "WEAK_SUB"
                        else:
                            wick_grade = "NONE"
                            cohort_role = "CONTROL_ONLY"

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
                            "win_loss_label": "HOLD_LABEL_FREE",
                            "net_pips_result": "HOLD_LABEL_FREE",
                        })
            d_cur += timedelta(days=1)

        key = f"{cand_id}|{symbol}"
        dst_audit[key] = sorted(offsets_seen)
        summary_by_candidate[key] = {
            "total_rows": seq,
            "continuity_pass_rows": pass_cnt,
            "exclusions": exclusions,
        }

    df_out = pd.DataFrame(all_rows)
    df_out.to_csv(out_csv_path, index=False)

    return {
        "file": os.path.basename(out_csv_path),
        "sha256": compute_sha256(out_csv_path),
        "bytes": os.path.getsize(out_csv_path),
        "total_rows": len(df_out),
        "dst_offsets_verified": dst_audit,
        "summary_by_candidate": summary_by_candidate,
    }


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
    out_manifest = os.path.join(stage1_dir, "stage1_to_stage2_handover_manifest_gsr_2026w49.json")

    res_a = generate_track_a_oos(bar_map_usdjpy_oos, out_a)
    res_b = generate_track_b_is(bar_maps_is, out_b)

    manifest = {
        "manifest_version": "1.2.0",
        "script_version": SCRIPT_VERSION,
        "case_id": CASE_ID,
        "executed_at_jst": datetime.now(TZ_TOKYO).isoformat(timespec="seconds"),
        "oos_locked_for_track_b": True,
        "oos_authorized_for_track_a_only": True,
        "label_free_enforced": True,
        "raw_m1_audits": raw_audits,
        "track_a_oos_ledger": res_a,
        "track_b_is_ledger": res_b,
        "script_sha256": compute_sha256(os.path.abspath(__file__)),
    }

    with open(out_manifest, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
