#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BO・EA Edge Discovery (Gemini側必勝調査報告):
Stage 1 — In-Sample (2015-2021) Market Structure & Opportunity Profiler
and Existing Model (Cross-Yen BB Reversal etc.) Continuity Auditor (v1.3.0 - GSR Trace Code Edition).

Trace Rule Compliance:
  Conforms to GEMINI_DISCOVERY_TRACE_RULE.md (2026-11-06 JST):
  - Parent Weekly Pipeline Code: GSR-2026W46 (configurable via --gsr-parent-id)
  - Individual Candidate Codes:
      * GSR-FAKEOUT-001  (Proposal_A_FakeoutReentry: Cross-Market / Session Fakeout Re-entry)
      * GSR-CLIMAX-001   (Proposal_B_BBClimaxReversal: M5 Non-Trend Gated M1 BB Climax Reversal)
      * GSR-PULLBACK-001 (Proposal_C_M5TrendPullback: M5 Trend Sync + M1 Volatility Contraction Pullback)
      * GSR-SURVEY-001   (Existing 60 Backtest Reports Continuity & 0.1pip Stress Audit)

How to run (Zero arguments required on local PC):
  PS C:\\Users\\kj43b> python "G:\\マイドライブ\\AIトレーサビリティ\\BO・EA Edge Discovery\\Gemini側必勝調査報告\\トレード手法の市場調査＆データ点検\\profile_is_market_structure_2015_2021_v1_3.py"
"""

from __future__ import annotations

import argparse
import csv
import glob
import hashlib
import json
import math
import os
import platform
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Dict, List, Optional, Tuple

sys.dont_write_bytecode = True

CODEX_PY312_EXE = Path(
    r"C:\Users\kj43b\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
)
if (
    sys.version_info[:2] != (3, 12)
    and CODEX_PY312_EXE.exists()
    and os.environ.get("BO_STAGE1_REEXEC") != "1"
):
    env = dict(
        os.environ,
        BO_STAGE1_REEXEC="1",
        PYTHONUTF8="1",
        PYTHONDONTWRITEBYTECODE="1",
    )
    raise SystemExit(
        subprocess.call(
            [str(CODEX_PY312_EXE), str(Path(__file__).resolve()), *sys.argv[1:]],
            env=env,
        )
    )

REPORT_ROOT = Path(
    r"G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告"
)
STAGE1_DIR = REPORT_ROOT / "トレード手法の市場調査＆データ点検"
STAGE2_DIR = REPORT_ROOT / "機会台帳突合＆IS統計・Plateau検証"
STAGE3_DIR = REPORT_ROOT / "執行監査・週次総括・Git資産整理"

GSR_STRATEGY_CASE_IDS: Dict[str, str] = {
    "Proposal_A_FakeoutReentry": "GSR-FAKEOUT-001",
    "Proposal_B_BBClimaxReversal": "GSR-CLIMAX-001",
    "Proposal_C_M5TrendPullback": "GSR-PULLBACK-001",
}
GSR_SURVEY_CASE_ID = "GSR-SURVEY-001"

CANDIDATE_M1_SOURCES: Dict[str, Tuple[str, List[Path]]] = {
    "EURUSD": (
        "0.00001",
        [
            Path(r"G:\マイドライブ\BO （順張・逆張）検証（パラメーター調整）\Spark用資料\EURUSD\EURUSD1.csv"),
            Path(r"G:\マイドライブ\通貨ペア\Dukascopy 1分足\EURUSD\EURUSD1.csv"),
            Path(r"C:\Users\kj43b\Desktop\BO （順張・逆張）検証（パラメーター調整）\EURUSD1.csv"),
        ],
    ),
    "USDJPY": (
        "0.001",
        [
            Path(r"G:\マイドライブ\通貨ペア\Dukascopy 1分足\USDJPY\USDJPY1.csv"),
            Path(r"G:\マイドライブ\BO （順張・逆張）検証（パラメーター調整）\USDJPY1.csv"),
            Path(r"C:\Users\kj43b\Desktop\BO （順張・逆張）検証（パラメーター調整）\USDJPY1.csv"),
        ],
    ),
}

CANDIDATE_REPORT_GLOBS = [
    r"G:\マイドライブ\BO （順張・逆張）検証（パラメーター調整）\逆張りEA\*\BO_BB3Sigma_Reversal_5M_*.csv",
    r"C:\Users\kj43b\Desktop\BO （順張・逆張）検証（パラメーター調整）\逆張りEA\*\BO_BB3Sigma_Reversal_5M_*.csv",
]

IS_START_DT = datetime(2015, 1, 1, 0, 0, 0)
IS_END_DT = datetime(2021, 12, 31, 23, 59, 59)
OOS_CUTOFF_DT = datetime(2022, 1, 1, 0, 0, 0)


@dataclass
class M1Bar:
    dt: datetime
    close_dt: datetime
    o_pts: int
    h_pts: int
    l_pts: int
    c_pts: int
    vol: float
    raw_line_no: int
    ohlc_valid: bool


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with filepath.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_price_to_points(val_str: str, point_unit: Decimal) -> Tuple[Optional[int], bool]:
    try:
        d = Decimal(val_str.strip())
        if not d.is_finite() or d <= 0:
            return None, False
        q = d / point_unit
        if q != q.to_integral_value():
            return None, False
        return int(q), True
    except (InvalidOperation, ValueError, AttributeError):
        return None, False


def parse_timestamp(row: List[str]) -> Tuple[Optional[datetime], int]:
    if len(row) >= 6:
        c0 = row[0].strip()
        c1 = row[1].strip()
        if ":" in c1 and ("-" in c0 or "." in c0 or "/" in c0) and " " not in c0:
            dt_str = f"{c0} {c1}"
            for fmt in (
                "%Y.%m.%d %H:%M:%S",
                "%Y.%m.%d %H:%M",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%Y/%m/%d %H:%M:%S",
                "%Y/%m/%d %H:%M",
            ):
                try:
                    return datetime.strptime(dt_str, fmt), 2
                except ValueError:
                    continue
        for fmt in (
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y.%m.%d %H:%M:%S",
            "%Y.%m.%d %H:%M",
            "%Y/%m/%d %H:%M:%S",
            "%Y/%m/%d %H:%M",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%SZ",
        ):
            try:
                return datetime.strptime(c0, fmt), 1
            except ValueError:
                continue
    return None, -1


def load_is_m1_bars(
    csv_path: Path, point_unit_str: str
) -> Tuple[List[M1Bar], Dict[str, object]]:
    point_unit = Decimal(point_unit_str)
    bars: List[M1Bar] = []
    stats = {
        "file_path": str(csv_path.resolve()),
        "sha256": compute_sha256(csv_path),
        "bytes": csv_path.stat().st_size,
        "total_raw_rows": 0,
        "header_or_unparseable_rows": 0,
        "dropped_pre_2015_rows": 0,
        "dropped_post_2021_oos_rows": 0,
        "is_kept_rows": 0,
        "ohlc_or_grid_invalid_rows": 0,
        "duplicate_timestamps": 0,
        "time_reversals": 0,
        "first_is_timestamp": None,
        "last_is_timestamp": None,
    }

    prev_dt: Optional[datetime] = None
    seen_dts = set()

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        for line_no, row in enumerate(reader, start=1):
            if not row or all(not c.strip() for c in row):
                continue
            stats["total_raw_rows"] += 1
            dt, p_idx = parse_timestamp(row)
            if dt is None or len(row) < p_idx + 4:
                stats["header_or_unparseable_rows"] += 1
                continue

            if dt < IS_START_DT:
                stats["dropped_pre_2015_rows"] += 1
                continue
            if dt >= OOS_CUTOFF_DT:
                stats["dropped_post_2021_oos_rows"] += 1
                continue

            if prev_dt is not None:
                if dt < prev_dt:
                    stats["time_reversals"] += 1
                elif dt == prev_dt or dt in seen_dts:
                    stats["duplicate_timestamps"] += 1
                    continue
            prev_dt = dt
            seen_dts.add(dt)

            o_pts, ok_o = parse_price_to_points(row[p_idx], point_unit)
            h_pts, ok_h = parse_price_to_points(row[p_idx + 1], point_unit)
            l_pts, ok_l = parse_price_to_points(row[p_idx + 2], point_unit)
            c_pts, ok_c = parse_price_to_points(row[p_idx + 3], point_unit)
            vol = 0.0
            if len(row) > p_idx + 4:
                try:
                    vol = float(row[p_idx + 4])
                except ValueError:
                    vol = 0.0

            ohlc_ok = (
                ok_o
                and ok_h
                and ok_l
                and ok_c
                and (l_pts <= o_pts <= h_pts)
                and (l_pts <= c_pts <= h_pts)
                and (h_pts >= l_pts)
            )
            if not ohlc_ok:
                stats["ohlc_or_grid_invalid_rows"] += 1
                o_pts = o_pts or 0
                h_pts = h_pts or 0
                l_pts = l_pts or 0
                c_pts = c_pts or 0

            bar = M1Bar(
                dt=dt,
                close_dt=dt + timedelta(minutes=1),
                o_pts=o_pts,
                h_pts=h_pts,
                l_pts=l_pts,
                c_pts=c_pts,
                vol=vol,
                raw_line_no=line_no,
                ohlc_valid=ohlc_ok,
            )
            bars.append(bar)

    bars.sort(key=lambda b: b.dt)
    stats["is_kept_rows"] = len(bars)
    if bars:
        stats["first_is_timestamp"] = bars[0].dt.strftime("%Y-%m-%d %H:%M:%S")
        stats["last_is_timestamp"] = bars[-1].dt.strftime("%Y-%m-%d %H:%M:%S")
    return bars, stats


def classify_session(utc_hour: int) -> str:
    if 0 <= utc_hour < 6:
        return "01_Tokyo_00_05UTC"
    elif 6 <= utc_hour < 7:
        return "02_PreLondon_06UTC"
    elif 7 <= utc_hour < 11:
        return "03_LondonEarly_07_10UTC"
    elif 11 <= utc_hour < 13:
        return "04_LondonMid_11_12UTC"
    elif 13 <= utc_hour < 17:
        return "05_NYOverlap_13_16UTC"
    elif 17 <= utc_hour < 21:
        return "06_NYLate_17_20UTC"
    else:
        return "07_Rollover_21_23UTC"


def classify_atr_bucket(atr_pips: float) -> str:
    if math.isnan(atr_pips):
        return "00_NA"
    if atr_pips < 1.2:
        return "01_Low_<1.2p"
    elif atr_pips < 2.0:
        return "02_Normal_1.2_2.0p"
    elif atr_pips < 3.5:
        return "03_Active_2.0_3.5p"
    else:
        return "04_High_>=3.5p"


def build_features_and_m5_context(
    bars: List[M1Bar], pip_points: int = 10
) -> List[Dict[str, object]]:
    n = len(bars)
    features: List[Dict[str, object]] = [{} for _ in range(n)]

    m5_groups: Dict[datetime, List[M1Bar]] = defaultdict(list)
    for b in bars:
        if not b.ohlc_valid:
            continue
        m5_open_dt = b.dt.replace(minute=(b.dt.minute // 5) * 5, second=0, microsecond=0)
        m5_groups[m5_open_dt].append(b)

    m5_sorted_keys = sorted(m5_groups.keys())
    m5_records: Dict[datetime, Dict[str, float]] = {}

    ema20_m5: Optional[float] = None
    ema75_m5: Optional[float] = None
    ema200_m5: Optional[float] = None
    k20 = 2.0 / 21.0
    k75 = 2.0 / 76.0
    k200 = 2.0 / 201.0

    m5_closes: List[float] = []
    m5_ema20_hist: List[float] = []

    for m5_dt in m5_sorted_keys:
        grp = m5_groups[m5_dt]
        c_val = float(grp[-1].c_pts)
        m5_closes.append(c_val)

        if ema20_m5 is None:
            ema20_m5 = c_val
            ema75_m5 = c_val
            ema200_m5 = c_val
        else:
            ema20_m5 = c_val * k20 + ema20_m5 * (1.0 - k20)
            ema75_m5 = c_val * k75 + ema75_m5 * (1.0 - k75)
            ema200_m5 = c_val * k200 + ema200_m5 * (1.0 - k200)

        m5_ema20_hist.append(ema20_m5)

        if len(m5_closes) >= 20:
            win20 = m5_closes[-20:]
            mu = sum(win20) / 20.0
            var = sum((x - mu) ** 2 for x in win20) / 20.0
            sd = math.sqrt(var)
            bbw_pips = (4.0 * sd) / float(pip_points)
        else:
            bbw_pips = float("nan")

        if len(m5_ema20_hist) >= 4:
            slope3_pips = (m5_ema20_hist[-1] - m5_ema20_hist[-4]) / float(pip_points)
        else:
            slope3_pips = float("nan")

        m5_records[m5_dt + timedelta(minutes=5)] = {
            "m5_open_dt": m5_dt,
            "m5_close_dt": m5_dt + timedelta(minutes=5),
            "m5_bbw_pips": bbw_pips,
            "m5_ema20": ema20_m5,
            "m5_ema75": ema75_m5,
            "m5_ema200": ema200_m5,
            "m5_slope3_pips": slope3_pips,
        }

    ema20_m1: Optional[float] = None
    ema75_m1: Optional[float] = None
    ema200_m1: Optional[float] = None
    avg_gain7: Optional[float] = None
    avg_loss7: Optional[float] = None
    tr_window: List[float] = []

    latest_m5: Optional[Dict[str, float]] = None

    for i, b in enumerate(bars):
        cand_m5_close = b.close_dt.replace(
            minute=(b.close_dt.minute // 5) * 5, second=0, microsecond=0
        )
        if cand_m5_close in m5_records:
            latest_m5 = m5_records[cand_m5_close]

        c_val = float(b.c_pts)
        if ema20_m1 is None:
            ema20_m1 = c_val
            ema75_m1 = c_val
            ema200_m1 = c_val
        else:
            ema20_m1 = c_val * k20 + ema20_m1 * (1.0 - k20)
            ema75_m1 = c_val * k75 + ema75_m1 * (1.0 - k75)
            ema200_m1 = c_val * k200 + ema200_m1 * (1.0 - k200)

        if i == 0 or (b.dt - bars[i - 1].dt) != timedelta(minutes=1):
            tr = float(b.h_pts - b.l_pts)
        else:
            prev_c = float(bars[i - 1].c_pts)
            tr = max(
                float(b.h_pts - b.l_pts),
                abs(float(b.h_pts) - prev_c),
                abs(float(b.l_pts) - prev_c),
            )
        tr_window.append(tr)
        if len(tr_window) > 14:
            tr_window.pop(0)
        atr14_pips = (
            (sum(tr_window) / 14.0) / float(pip_points)
            if len(tr_window) == 14
            else float("nan")
        )

        rsi7 = float("nan")
        if i > 0:
            chg = float(b.c_pts - bars[i - 1].c_pts)
            gain = max(chg, 0.0)
            loss = max(-chg, 0.0)
            if i < 7:
                pass
            elif i == 7:
                gains = [
                    max(float(bars[j].c_pts - bars[j - 1].c_pts), 0.0)
                    for j in range(1, 8)
                ]
                losses = [
                    max(float(bars[j - 1].c_pts - bars[j].c_pts), 0.0)
                    for j in range(1, 8)
                ]
                avg_gain7 = sum(gains) / 7.0
                avg_loss7 = sum(losses) / 7.0
            else:
                assert avg_gain7 is not None and avg_loss7 is not None
                avg_gain7 = (avg_gain7 * 6.0 + gain) / 7.0
                avg_loss7 = (avg_loss7 * 6.0 + loss) / 7.0

            if avg_gain7 is not None and avg_loss7 is not None:
                if avg_loss7 == 0.0:
                    rsi7 = 100.0 if avg_gain7 > 0.0 else 50.0
                else:
                    rs = avg_gain7 / avg_loss7
                    rsi7 = 100.0 - (100.0 / (1.0 + rs))

        bb_mu = float("nan")
        bb_sd = float("nan")
        if i >= 19:
            win_c = [float(bars[j].c_pts) for j in range(i - 19, i + 1)]
            bb_mu = sum(win_c) / 20.0
            bb_sd = math.sqrt(sum((x - bb_mu) ** 2 for x in win_c) / 20.0)

        rng_pts = b.h_pts - b.l_pts
        upper_wick_ratio = (
            float(b.h_pts - max(b.o_pts, b.c_pts)) / float(rng_pts)
            if rng_pts > 0
            else 0.0
        )
        lower_wick_ratio = (
            float(min(b.o_pts, b.c_pts) - b.l_pts) / float(rng_pts)
            if rng_pts > 0
            else 0.0
        )
        body_ratio = (
            float(abs(b.c_pts - b.o_pts)) / float(rng_pts) if rng_pts > 0 else 0.0
        )

        features[i] = {
            "atr14_pips": atr14_pips,
            "rsi7": rsi7,
            "bb_mu": bb_mu,
            "bb_sd": bb_sd,
            "ema20_m1": ema20_m1,
            "ema75_m1": ema75_m1,
            "ema200_m1": ema200_m1,
            "upper_wick_ratio": upper_wick_ratio,
            "lower_wick_ratio": lower_wick_ratio,
            "body_ratio": body_ratio,
            "range_pips": float(rng_pts) / float(pip_points),
            "m5_context": latest_m5,
        }

    return features


def check_t1_to_t6_continuity(
    bars: List[M1Bar], idx_t: int
) -> Tuple[bool, List[str], Optional[M1Bar], Optional[M1Bar]]:
    reasons: List[str] = []
    b_t = bars[idx_t]
    if not b_t.ohlc_valid:
        reasons.append("DECISION_BAR_OHLC_INVALID")

    dt_base = b_t.dt
    found: Dict[int, M1Bar] = {}
    for k in range(idx_t + 1, min(idx_t + 7, len(bars))):
        delta = bars[k].dt - dt_base
        if timedelta(minutes=1) <= delta <= timedelta(minutes=6):
            if delta.seconds % 60 == 0 and delta.days == 0:
                m_off = delta.seconds // 60
                found[m_off] = bars[k]

    if 1 not in found:
        reasons.append("MISSING_ENTRY_T1")
    if 6 not in found:
        reasons.append("MISSING_EXPIRY_T6")
    for m_off in (2, 3, 4, 5):
        if m_off not in found:
            reasons.append("INTERMEDIATE_BAR_GAP_T2_T5")
            break

    for m_off, bar_obj in found.items():
        if not bar_obj.ohlc_valid:
            reasons.append(f"BAR_T{m_off}_OHLC_INVALID")

    is_valid = len(reasons) == 0
    return is_valid, reasons, found.get(1), found.get(6)


def scan_three_proposals(
    bars: List[M1Bar],
    features: List[Dict[str, object]],
    pip_points: int = 10,
    eval_is_baseline: bool = False,
    gsr_parent_id: str = "GSR-2026W46",
) -> List[Dict[str, object]]:
    n = len(bars)
    tokyo_boxes: Dict[str, Dict[str, object]] = {}
    day_bars_map: Dict[str, List[int]] = defaultdict(list)
    for i, b in enumerate(bars):
        day_str = b.dt.strftime("%Y-%m-%d")
        day_bars_map[day_str].append(i)

    for day_str, idxs in day_bars_map.items():
        t_bars = [bars[i] for i in idxs if 0 <= bars[i].dt.hour < 6 and bars[i].ohlc_valid]
        if len(t_bars) >= 330:
            h_pts = max(x.h_pts for x in t_bars)
            l_pts = min(x.l_pts for x in t_bars)
            w_pips = float(h_pts - l_pts) / float(pip_points)
            tokyo_boxes[day_str] = {
                "valid_base": True,
                "base_count": len(t_bars),
                "h_pts": h_pts,
                "l_pts": l_pts,
                "w_pips": w_pips,
            }
        else:
            tokyo_boxes[day_str] = {
                "valid_base": False,
                "base_count": len(t_bars),
                "h_pts": 0,
                "l_pts": 0,
                "w_pips": 0.0,
            }

    opportunities: List[Dict[str, object]] = []
    seen_prop_a_day_dir = set()
    last_entry_until_prop_b: Optional[datetime] = None
    last_entry_until_prop_c: Optional[datetime] = None

    break_margin_pts = int(round(0.5 * pip_points))
    reentry_margin_pts = int(round(0.2 * pip_points))

    for i in range(25, n):
        b = bars[i]
        f = features[i]
        m5 = f.get("m5_context")
        day_str = b.dt.strftime("%Y-%m-%d")
        utc_hr = b.dt.hour
        atr14 = f["atr14_pips"]
        rsi7 = f["rsi7"]
        bb_mu = f["bb_mu"]
        bb_sd = f["bb_sd"]
        rng_pips = f["range_pips"]

        if math.isnan(atr14) or math.isnan(rsi7) or math.isnan(bb_mu) or m5 is None:
            continue

        m5_bbw = m5["m5_bbw_pips"]
        m5_slope = m5["m5_slope3_pips"]
        if math.isnan(m5_bbw) or math.isnan(m5_slope):
            continue

        # GSR-FAKEOUT-001 (Proposal_A_FakeoutReentry)
        if 7 <= utc_hr < 10:
            tbox = tokyo_boxes.get(day_str)
            if tbox and tbox["valid_base"]:
                w_pips = tbox["w_pips"]
                if 12.0 <= w_pips <= 40.0 and abs(m5_slope) <= 4.0:
                    h_box = tbox["h_pts"]
                    l_box = tbox["l_pts"]
                    body_pips = abs(b.c_pts - b.o_pts) / float(pip_points)
                    if body_pips <= 2.5 * atr14 and atr14 >= 1.2:
                        up_excursion = any(
                            bars[i - k].h_pts >= h_box + break_margin_pts
                            and (b.dt - bars[i - k].dt) == timedelta(minutes=k)
                            for k in (1, 2, 3)
                        )
                        down_excursion = any(
                            bars[i - k].l_pts <= l_box - break_margin_pts
                            and (b.dt - bars[i - k].dt) == timedelta(minutes=k)
                            for k in (1, 2, 3)
                        )
                        if (
                            up_excursion
                            and b.c_pts <= h_box - reentry_margin_pts
                            and b.c_pts < b.o_pts
                            and (day_str, "LOW") not in seen_prop_a_day_dir
                        ):
                            seen_prop_a_day_dir.add((day_str, "LOW"))
                            opportunities.append(
                                build_opp_record(
                                    "Proposal_A_FakeoutReentry",
                                    "LOW",
                                    bars,
                                    i,
                                    f,
                                    pip_points,
                                    eval_is_baseline,
                                    gsr_parent_id,
                                )
                            )
                        elif (
                            down_excursion
                            and b.c_pts >= l_box + reentry_margin_pts
                            and b.c_pts > b.o_pts
                            and (day_str, "HIGH") not in seen_prop_a_day_dir
                        ):
                            seen_prop_a_day_dir.add((day_str, "HIGH"))
                            opportunities.append(
                                build_opp_record(
                                    "Proposal_A_FakeoutReentry",
                                    "HIGH",
                                    bars,
                                    i,
                                    f,
                                    pip_points,
                                    eval_is_baseline,
                                    gsr_parent_id,
                                )
                            )

        # GSR-CLIMAX-001 (Proposal_B_BBClimaxReversal)
        if not (21 <= utc_hr <= 23) and b.dt.minute < 55:
            if last_entry_until_prop_b is None or b.dt >= last_entry_until_prop_b:
                if atr14 >= 1.2 and rng_pips >= 1.5 and m5_bbw <= 18.0 and abs(m5_slope) < 2.5:
                    bb_up28 = bb_mu + 2.8 * bb_sd
                    bb_dn28 = bb_mu - 2.8 * bb_sd
                    if (
                        float(b.h_pts) >= bb_up28
                        and rsi7 >= 85.0
                        and f["upper_wick_ratio"] >= 0.40
                    ):
                        last_entry_until_prop_b = b.dt + timedelta(minutes=6)
                        opportunities.append(
                            build_opp_record(
                                "Proposal_B_BBClimaxReversal",
                                "LOW",
                                bars,
                                i,
                                f,
                                pip_points,
                                eval_is_baseline,
                                gsr_parent_id,
                            )
                        )
                    elif (
                        float(b.l_pts) <= bb_dn28
                        and rsi7 <= 15.0
                        and f["lower_wick_ratio"] >= 0.40
                    ):
                        last_entry_until_prop_b = b.dt + timedelta(minutes=6)
                        opportunities.append(
                            build_opp_record(
                                "Proposal_B_BBClimaxReversal",
                                "HIGH",
                                bars,
                                i,
                                f,
                                pip_points,
                                eval_is_baseline,
                                gsr_parent_id,
                            )
                        )

        # GSR-PULLBACK-001 (Proposal_C_M5TrendPullback)
        if 7 <= utc_hr < 16:
            if last_entry_until_prop_c is None or b.dt >= last_entry_until_prop_c:
                vr = rng_pips / atr14 if atr14 > 0 else 0.0
                if atr14 >= 1.2 and 0.8 <= vr <= 2.0 and f["body_ratio"] >= 0.50:
                    prev_b = bars[i - 1]
                    prev_f = features[i - 1]
                    prev_rsi = prev_f.get("rsi7", float("nan"))
                    if (
                        not math.isnan(prev_rsi)
                        and (b.dt - prev_b.dt) == timedelta(minutes=1)
                    ):
                        m5_bull = (
                            m5["m5_ema20"] > m5["m5_ema75"] > m5["m5_ema200"]
                            and m5_slope >= 1.5
                        )
                        m5_bear = (
                            m5["m5_ema20"] < m5["m5_ema75"] < m5["m5_ema200"]
                            and m5_slope <= -1.5
                        )
                        m1_bull = f["ema20_m1"] > f["ema75_m1"]
                        m1_bear = f["ema20_m1"] < f["ema75_m1"]

                        if (
                            m5_bull
                            and m1_bull
                            and b.c_pts > b.o_pts
                            and prev_rsi <= 45.0
                            and (
                                float(b.l_pts) <= f["ema20_m1"]
                                or float(prev_b.l_pts) <= prev_f["ema20_m1"]
                            )
                            and float(min(b.c_pts, prev_b.c_pts)) > f["ema75_m1"]
                            and float(b.c_pts) > f["ema20_m1"]
                            and b.c_pts > prev_b.h_pts
                        ):
                            last_entry_until_prop_c = b.dt + timedelta(minutes=6)
                            opportunities.append(
                                build_opp_record(
                                    "Proposal_C_M5TrendPullback",
                                    "HIGH",
                                    bars,
                                    i,
                                    f,
                                    pip_points,
                                    eval_is_baseline,
                                    gsr_parent_id,
                                )
                            )
                        elif (
                            m5_bear
                            and m1_bear
                            and b.c_pts < b.o_pts
                            and prev_rsi >= 55.0
                            and (
                                float(b.h_pts) >= f["ema20_m1"]
                                or float(prev_b.h_pts) >= prev_f["ema20_m1"]
                            )
                            and float(max(b.c_pts, prev_b.c_pts)) < f["ema75_m1"]
                            and float(b.c_pts) < f["ema20_m1"]
                            and b.c_pts < prev_b.l_pts
                        ):
                            last_entry_until_prop_c = b.dt + timedelta(minutes=6)
                            opportunities.append(
                                build_opp_record(
                                    "Proposal_C_M5TrendPullback",
                                    "LOW",
                                    bars,
                                    i,
                                    f,
                                    pip_points,
                                    eval_is_baseline,
                                    gsr_parent_id,
                                )
                            )

    return opportunities


def build_opp_record(
    strategy: str,
    direction: str,
    bars: List[M1Bar],
    idx_t: int,
    f: Dict[str, object],
    pip_points: int,
    eval_is_baseline: bool,
    gsr_parent_id: str,
) -> Dict[str, object]:
    b_t = bars[idx_t]
    is_valid, reasons, b_t1, b_t6 = check_t1_to_t6_continuity(bars, idx_t)
    m5 = f["m5_context"]

    rec: Dict[str, object] = {
        "case_id": GSR_STRATEGY_CASE_IDS.get(strategy, "GSR-SURVEY-001"),
        "parent_case_id": gsr_parent_id,
        "strategy": strategy,
        "direction": direction,
        "decision_open_utc": b_t.dt.strftime("%Y-%m-%d %H:%M:%S"),
        "signal_utc": b_t.close_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "expected_entry_utc": (b_t.dt + timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S"),
        "expected_expiry_utc": (b_t.dt + timedelta(minutes=6)).strftime("%Y-%m-%d %H:%M:%S"),
        "year": b_t.dt.year,
        "utc_hour": b_t.dt.hour,
        "session": classify_session(b_t.dt.hour),
        "atr14_pips": round(float(f["atr14_pips"]), 3),
        "atr_bucket": classify_atr_bucket(float(f["atr14_pips"])),
        "m5_bbw_pips": round(float(m5["m5_bbw_pips"]), 3),
        "m5_slope3_pips": round(float(m5["m5_slope3_pips"]), 3),
        "m5_ref_close_utc": m5["m5_close_dt"].strftime("%Y-%m-%d %H:%M:%S"),
        "continuity_status": "VALID_6BAR_CONTINUOUS" if is_valid else "INVALID_GAP",
        "invalid_reasons": "|".join(reasons) if reasons else "PASS",
    }

    if eval_is_baseline and is_valid and b_t1 is not None and b_t6 is not None:
        stress_pts = max(1, pip_points // 10)
        favorable_pts = (
            (b_t6.o_pts - b_t1.o_pts)
            if direction == "HIGH"
            else (b_t1.o_pts - b_t6.o_pts)
        )
        is_win = favorable_pts > stress_pts
        rec["entry_price_pts"] = b_t1.o_pts
        rec["expiry_price_pts"] = b_t6.o_pts
        rec["favorable_diff_pts"] = favorable_pts
        rec["outcome_01pip_stress"] = "WIN" if is_win else "LOSE"
        rec["ev_unit_185"] = 0.85 if is_win else -1.00
    else:
        rec["entry_price_pts"] = "HOLD_LABEL_FREE"
        rec["expiry_price_pts"] = "HOLD_LABEL_FREE"
        rec["favorable_diff_pts"] = "HOLD_LABEL_FREE"
        rec["outcome_01pip_stress"] = "HOLD_LABEL_FREE" if is_valid else "INVALID"
        rec["ev_unit_185"] = "HOLD_LABEL_FREE"

    return rec


def summarize_opportunities(
    opps: List[Dict[str, object]], gsr_parent_id: str = "GSR-2026W46"
) -> Dict[str, object]:
    summary: Dict[str, object] = {}
    strategies = sorted(set(str(o["strategy"]) for o in opps))

    for strat in strategies:
        sub = [o for o in opps if o["strategy"] == strat]
        valid = [o for o in sub if o["continuity_status"] == "VALID_6BAR_CONTINUOUS"]
        invalid = [o for o in sub if o["continuity_status"] != "VALID_6BAR_CONTINUOUS"]

        by_year = Counter(int(o["year"]) for o in valid)
        by_session = Counter(str(o["session"]) for o in valid)
        by_atr = Counter(str(o["atr_bucket"]) for o in valid)
        by_reasons = Counter(str(o["invalid_reasons"]) for o in invalid)

        dts = sorted(
            datetime.strptime(str(o["expected_entry_utc"]), "%Y-%m-%d %H:%M:%S")
            for o in valid
        )
        overlap_300s_pairs = 0
        for j in range(1, len(dts)):
            if (dts[j] - dts[j - 1]).total_seconds() <= 300:
                overlap_300s_pairs += 1

        unique_days = len(set(d.strftime("%Y-%m-%d") for d in dts))

        summary[strat] = {
            "case_id": GSR_STRATEGY_CASE_IDS.get(strat, "GSR-SURVEY-001"),
            "parent_case_id": gsr_parent_id,
            "total_candidates": len(sub),
            "valid_6bar_count": len(valid),
            "invalid_gap_count": len(invalid),
            "unique_utc_days": unique_days,
            "within_300s_adjacent_pairs": overlap_300s_pairs,
            "by_year_valid": dict(sorted(by_year.items())),
            "by_session_valid": dict(sorted(by_session.items())),
            "by_atr_bucket_valid": dict(sorted(by_atr.items())),
            "invalid_reason_breakdown": dict(sorted(by_reasons.items())),
        }

    return summary


def audit_existing_report_csvs(
    report_glob: str,
    raw_m1_csv: Optional[Path],
    pip_points: int = 10,
    gsr_parent_id: str = "GSR-2026W46",
) -> List[Dict[str, object]]:
    m1_ts_set = set()
    if raw_m1_csv and raw_m1_csv.exists():
        with raw_m1_csv.open("r", encoding="utf-8-sig", newline="") as f:
            for row in csv.reader(f):
                dt, _ = parse_timestamp(row)
                if dt is not None:
                    m1_ts_set.add(dt)

    results = []
    for fpath_str in sorted(glob.glob(report_glob, recursive=True)):
        fpath = Path(fpath_str)
        if not fpath.is_file():
            continue
        sha = compute_sha256(fpath)
        with fpath.open("r", encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))

        if not rows:
            continue

        total = len(rows)
        wins_raw = 0
        ties_raw = 0
        wins_after_01pip_stress = 0
        expiry_mismatch_5m = 0
        overlap_5m_count = 0
        m1_gap_broken_count = 0

        prev_entry_dt: Optional[datetime] = None
        entry_dts: List[datetime] = []

        for r in rows:
            e_str = (r.get("EntryTime") or "").strip()
            s_str = (r.get("SettleTime") or "").strip()
            t_dir = (r.get("Type") or "").strip().upper()
            res_str = (r.get("Result") or "").strip().upper()

            e_dt, _ = parse_timestamp([e_str, "0", "0", "0", "0", "0"])
            s_dt, _ = parse_timestamp([s_str, "0", "0", "0", "0", "0"])

            if e_dt:
                entry_dts.append(e_dt)
                if prev_entry_dt and (e_dt - prev_entry_dt).total_seconds() < 300:
                    overlap_5m_count += 1
                prev_entry_dt = e_dt

            if e_dt and s_dt:
                if (s_dt - e_dt) != timedelta(minutes=5):
                    expiry_mismatch_5m += 1

            if e_dt and m1_ts_set:
                all_6_present = all(
                    (e_dt + timedelta(minutes=m)) in m1_ts_set for m in range(0, 6)
                )
                if not all_6_present:
                    m1_gap_broken_count += 1

            if res_str == "WIN":
                wins_raw += 1

            try:
                ep = Decimal(str(r.get("EntryPrice", "0")).strip())
                sp = Decimal(str(r.get("SettlePrice", "0")).strip())
                diff = (sp - ep) if t_dir == "HIGH" else (ep - sp)
                if diff == 0:
                    ties_raw += 1
                exponent = ep.as_tuple().exponent
                pt_unit = Decimal(10) ** exponent if isinstance(exponent, int) else Decimal("0.001")
                if diff > pt_unit:
                    wins_after_01pip_stress += 1
            except InvalidOperation:
                pass

        wr_raw = (wins_raw / total * 100.0) if total > 0 else 0.0
        wr_stress = (wins_after_01pip_stress / total * 100.0) if total > 0 else 0.0
        ev_stress = (wins_after_01pip_stress * 0.85 - (total - wins_after_01pip_stress) * 1.0) / total if total > 0 else 0.0

        results.append(
            {
                "case_id": GSR_SURVEY_CASE_ID,
                "parent_case_id": gsr_parent_id,
                "pair_folder": fpath.parent.name,
                "file": fpath.name,
                "path": str(fpath),
                "sha256_prefix": sha[:12],
                "total_trades": total,
                "first_entry": entry_dts[0].strftime("%Y-%m-%d %H:%M") if entry_dts else None,
                "last_entry": entry_dts[-1].strftime("%Y-%m-%d %H:%M") if entry_dts else None,
                "raw_win_rate_pct": round(wr_raw, 2),
                "ties_count": ties_raw,
                "stress_01pip_win_rate_pct": round(wr_stress, 2),
                "stress_01pip_ev_unit": round(ev_stress, 4),
                "overlap_within_5m_count": overlap_5m_count,
                "settle_not_5m_count": expiry_mismatch_5m,
                "m1_t1_t6_gap_broken_count": m1_gap_broken_count if m1_ts_set else "M1_NOT_PROVIDED",
            }
        )
    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stage 1: IS (2015-2021) BO Market Structure Profiler & Existing Model Continuity Auditor (v1.3.0)"
    )
    parser.add_argument(
        "--m1-csv",
        type=Path,
        default=None,
        help="Path to raw M1 CSV file (if omitted, auto-discovers EURUSD1.csv & USDJPY1.csv on local PC)",
    )
    parser.add_argument(
        "--point-unit",
        type=str,
        default="0.00001",
        help="1 point unit as string ('0.00001' for 5-digit FX, '0.001' for 3-digit JPY pairs)",
    )
    parser.add_argument(
        "--pip-points",
        type=int,
        default=10,
        help="Integer points per 1 pip (default: 10)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory to write profiling ledgers and JSON summary (defaults to Stage 1 folder on Drive)",
    )
    parser.add_argument(
        "--eval-is-baseline",
        action="store_true",
        help="If set, compute IS (2015-2021) Win/Lose/EV under 0.1pip stress. Default is Label-Free.",
    )
    parser.add_argument(
        "--audit-reports-glob",
        type=str,
        default="",
        help="Optional glob pattern to audit existing BO_BB3Sigma_Reversal_5M_*.csv reports",
    )
    parser.add_argument(
        "--tag",
        type=str,
        default="auto",
        help="Identifier tag for output filenames",
    )
    parser.add_argument(
        "--gsr-parent-id",
        type=str,
        default="GSR-2026W46",
        help="Weekly pipeline TRACE case_id per GEMINI_DISCOVERY_TRACE_RULE.md (default: GSR-2026W46)",
    )

    args = parser.parse_args()
    now_jst = datetime.now(timezone(timedelta(hours=9)))
    run_stamp = now_jst.strftime("%Y%m%d_%H%M%S")

    if args.output_dir is not None:
        out_dir = args.output_dir
    elif STAGE1_DIR.exists():
        out_dir = STAGE1_DIR / f"output_is_profile_{run_stamp}"
    else:
        out_dir = Path(f"./output_is_profile_{run_stamp}")

    out_dir.mkdir(parents=True, exist_ok=True)

    manifest: Dict[str, object] = {
        "script_version": "1.3.0",
        "trace_rule_compliance": "GEMINI_DISCOVERY_TRACE_RULE.md (2026-11-06 JST)",
        "pipeline_case_id": args.gsr_parent_id,
        "candidate_case_ids": GSR_STRATEGY_CASE_IDS,
        "survey_audit_case_id": GSR_SURVEY_CASE_ID,
        "source_trace_refs_prior_rejected": ["BO-EUR-004", "BO-EUR-005"],
        "executed_at_jst": now_jst.isoformat(timespec="seconds"),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "stage1_storage_dir": str(out_dir.resolve()),
        "stage2_handover_dir": str(STAGE2_DIR),
        "stage3_final_gate_dir": str(STAGE3_DIR),
        "is_period_gate": "2015-01-01 00:00:00 <= dt <= 2021-12-31 23:59:59 (2022+ strictly blocked)",
        "label_free_mode": not args.eval_is_baseline,
    }

    target_m1_jobs: List[Tuple[str, Path, str]] = []
    if args.m1_csv is not None:
        if not args.m1_csv.exists():
            print(f"[ERROR] M1 CSV not found: {args.m1_csv}", file=sys.stderr)
            return 1
        target_m1_jobs.append((args.tag, args.m1_csv, args.point_unit))
    else:
        for pair_name, (pt_unit, cand_paths) in CANDIDATE_M1_SOURCES.items():
            for cp in cand_paths:
                if cp.exists():
                    target_m1_jobs.append((pair_name.lower(), cp, pt_unit))
                    break

    datasets_result: Dict[str, object] = {}
    for job_tag, csv_path, pt_unit in target_m1_jobs:
        bars, load_stats = load_is_m1_bars(csv_path, pt_unit)
        features = build_features_and_m5_context(bars, pip_points=args.pip_points)
        opps = scan_three_proposals(
            bars,
            features,
            pip_points=args.pip_points,
            eval_is_baseline=args.eval_is_baseline,
            gsr_parent_id=args.gsr_parent_id,
        )
        opp_summary = summarize_opportunities(opps, gsr_parent_id=args.gsr_parent_id)

        ledger_path = out_dir / f"is_2015_2021_opportunity_ledger_{job_tag}.csv"
        if opps:
            with ledger_path.open("w", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=list(opps[0].keys()))
                writer.writeheader()
                writer.writerows(opps)

        datasets_result[job_tag] = {
            "m1_data_audit": load_stats,
            "is_opportunity_summary": opp_summary,
            "output_ledger_csv": str(ledger_path.resolve()),
            "output_ledger_sha256": compute_sha256(ledger_path) if ledger_path.exists() else None,
        }
        if args.m1_csv is not None:
            manifest["m1_data_audit"] = load_stats
            manifest["is_opportunity_summary"] = opp_summary
            manifest["output_ledger_csv"] = str(ledger_path.resolve())
            if ledger_path.exists():
                manifest["output_ledger_sha256"] = compute_sha256(ledger_path)

    if datasets_result:
        manifest["datasets_profiled"] = datasets_result

    report_glob_to_use = args.audit_reports_glob
    if not report_glob_to_use and args.m1_csv is None:
        for cg in CANDIDATE_REPORT_GLOBS:
            if glob.glob(cg):
                report_glob_to_use = cg
                break

    if report_glob_to_use:
        report_audits = audit_existing_report_csvs(
            report_glob_to_use,
            args.m1_csv,
            pip_points=args.pip_points,
            gsr_parent_id=args.gsr_parent_id,
        )
        manifest["existing_reports_audit"] = report_audits
        audit_csv_path = out_dir / f"existing_reports_continuity_audit_{args.tag}.csv"
        if report_audits:
            with audit_csv_path.open("w", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=list(report_audits[0].keys()))
                writer.writeheader()
                writer.writerows(report_audits)
            manifest["existing_reports_audit_csv"] = str(audit_csv_path.resolve())

    summary_json_path = out_dir / f"is_profile_and_audit_summary_{args.tag}.json"
    summary_json_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
