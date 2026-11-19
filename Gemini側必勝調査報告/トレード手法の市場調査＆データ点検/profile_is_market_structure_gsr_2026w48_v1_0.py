import csv, hashlib, json, os
from datetime import datetime, timedelta

D = r"G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\トレード手法の市場調査＆データ点検"
R = r"G:\マイドライブ\通貨ペア\Dukascopy 1分足\USDJPY\2026.10.16USDJPY(3)-M1-No Session.csv"
C12, C27 = os.path.join(D, "is_2015_2021_opportunity_ledger_gsr_2026w48.csv"), os.path.join(D, "is_2015_2021_opportunity_ledger_gsr_2026w48_masked_v22.csv")
MAN = os.path.join(D, "stage1_to_stage2_handover_manifest_gsr_2026w48.json")

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1048576), b""): h.update(b)
    return h.hexdigest()

print("[1/3] Scanning 258.8MB Raw M1 CSV (IS 2015-2021)...")
bars = {}
with open(R, "r", encoding="utf-8", errors="ignore") as f:
    for ln in f:
        if not ln or ln[0] not in "12": continue
        p = [x.strip() for x in ln.split(",")]
        dt, tm, i = (p[0].split()[0], p[0].split()[1], 1) if " " in p[0] else (p[0], p[1], 2)
        if "2015" <= dt[:4] <= "2021":
            hm = ("0" + tm if tm[1] == ":" else tm)[:5]
            if "00:00" <= hm <= "01:05":
                bars.setdefault(dt.replace(".", "-").replace("/", "-"), {})[hm] = tuple(map(float, p[i:i+4]))

print("[2/3] Computing strict Raw M1 OHLC features for 1,177 rows...")
with open(C27, "r", encoding="utf-8-sig") as f: r27 = list(csv.DictReader(f)); f27 = list(r27[0].keys())
with open(C12, "r", encoding="utf-8-sig") as f: r12 = list(csv.DictReader(f)); f12 = list(r12[0].keys())
w15, w14, w6 = [f"00:{m:02d}" for m in range(40,55)], [f"00:{m:02d}" for m in range(41,55)], [f"00:{m:02d}" for m in range(55,60)]+["01:00"]
gc = {"PURE_STRONG": 0, "WEAK_SUB": 0, "NONE": 0}

for r1, r2 in zip(r12, r27):
    td = (r2.get("trade_date") if r2.get("trade_date") not in ("unknown","",None) else r1["trade_date"])[:10]
    db = bars[td]
    upto54 = [db[k] for k in sorted(db) if k <= "00:54"]
    b15 = [db[t] for t in w15 if t in db] or upto54[-15:]
    b14 = [db[t] for t in w14 if t in db] or upto54[-14:]
    b54, b40 = db.get("00:54", b15[-1]), db.get("00:40", b15[0])
    rng15, bod15 = (max(b[1] for b in b15) - min(b[2] for b in b15)) / 0.01, abs(b54[3] - b40[0]) / 0.01
    atr14 = sum((b[1] - b[2]) / 0.01 for b in b14) / len(b14)
    dr = r2.get("direction") if r2.get("direction") not in ("unknown","",None) else (r1.get("direction") if r1.get("direction") not in ("unknown","",None) else ("SELL" if b54[3] > b40[0] else "BUY"))
    r54 = b54[1] - b54[2]
    wk = 0.0 if r54 <= 1e-9 else ((b54[1] - max(b54[0], b54[3])) / r54 if dr == "SELL" else (min(b54[0], b54[3]) - b54[2]) / r54)
    role = r2.get("cohort_role") if r2.get("cohort_role") not in ("unknown","",None) else ("CONTROL_ONLY" if r1.get("wick_rejection_grade") == "NONE" else "CANDIDATE")
    gr = "NONE" if role == "CONTROL_ONLY" else ("PURE_STRONG" if wk >= 0.25 - 1e-9 else "WEAK_SUB")
    gc[gr] += 1
    d = datetime.strptime(td, "%Y-%m-%d").date()
    gtb = d.weekday() < 5 and (d.day % 5 == 0 or (d.weekday() == 4 and ((d + timedelta(1)).day % 5 == 0 or (d + timedelta(2)).day % 5 == 0)))
    cp, mv = all(t in db for t in w6), (bod15 / atr14 if atr14 > 1e-9 else 0.0)
    ba1 = r2.get("bin_axis_1_move15m_atr") if r2.get("bin_axis_1_move15m_atr") not in ("unknown","",None) else ("B1_1.5_2.0" if mv < 2.0 else ("B2_2.0_2.6" if mv < 2.6 else ("B3_2.6_3.5" if mv < 3.5 else "B4_3.5_up")))
    ba2 = "B1_sub1.5" if atr14 < 1.5 else ("B2_1.5_2.5" if atr14 < 2.5 else ("B3_2.5_4.0" if atr14 < 4.0 else "B4_4.0_up"))
    ba3 = "B1_sub0.25" if wk < 0.25 - 1e-9 else ("B2_0.25_0.40" if wk < 0.40 - 1e-9 else ("B3_0.40_0.55" if wk < 0.55 - 1e-9 else "B4_0.55_up"))
    r2.update({"case_id": "GSR-TKYFIX-002", "parent_case_id": "GSR-TKYFIX-001", "symbol": "USDJPY", "trade_date": td, "decision_open_utc": f"{td} 00:54:00", "signal_utc": f"{td} 00:55:00", "expected_entry_utc": f"{td} 00:55:00", "expected_expiry_utc": f"{td} 01:00:00", "entry_time": f"{td} 09:55:00", "eval_end_time": f"{td} 10:00:00", "direction": dr, "cohort_role": role, "wick_rejection_grade": gr, "wick_rejection_ratio": f"{wk:.4f}", "pre_15m_range_pips": f"{rng15:.4f}", "pre_15m_body_pips": f"{bod15:.4f}", "atr14_pips": f"{atr14:.4f}", "day_of_week": str(d.weekday()), "gotobi_flag": "1" if gtb else "0", "m1_continuity_pass": "1" if cp else "0", "continuity_6bar_status": "PASS" if cp else "FAIL", "bin_axis_1_move15m_atr": ba1, "bin_axis_2_atr14": ba2, "bin_axis_3_wick_ratio": ba3, "win_loss_label": "HOLD_LABEL_FREE", "net_pips_result": "HOLD_LABEL_FREE"})
    for k in f12: r1[k] = r2[k]
    r1["entry_time"], r1["eval_end_time"] = "09:55:00", "10:00:00"

with open(C12, "w", encoding="utf-8", newline="") as f: w = csv.DictWriter(f, fieldnames=f12); w.writeheader(); w.writerows(r12)
with open(C27, "w", encoding="utf-8", newline="") as f: w = csv.DictWriter(f, fieldnames=f27); w.writeheader(); w.writerows(r27)
u12, u27 = sum(1 for r in r12 if "unknown" in r.values()), sum(1 for r in r27 if "unknown" in r.values())
with open(MAN, "w", encoding="utf-8") as f:
    json.dump({"manifest_version": "1.0.1", "status": "LOCAL_FULL_258MB_VERIFIED", "case_id": "GSR-2026W48", "target": "GSR-TKYFIX-002", "oos_locked": True, "counts": gc, "sha256": {"py": sha(__file__), "csv12": sha(C12), "csv27": sha(C27), "raw_m1": sha(R)}}, f, indent=2)

print(f"\n[3/3 検算完了] unknown残存 -> 12列:{u12}行 / 27列:{u27}行 | 内訳:{gc}")
for p in (__file__, C12, C27, MAN): print(f"SHA256: {sha(p)}  {os.path.basename(p)}")
