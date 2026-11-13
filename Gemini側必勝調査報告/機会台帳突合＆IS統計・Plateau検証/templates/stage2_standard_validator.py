"""
QUANTITATIVE STAGE 2 STANDARD VALIDATOR TEMPLATE (v2.2)
用途: 水曜・第2工程（機会台帳突合 & IS統計・Plateau検証）および Spark独立監査マニフェスト生成
対応モード: BO_STANDARD / BO_ONETOUCH / FX_EXPANSION
"""

import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
import numpy as np
import pandas as pd

JST = timezone(timedelta(hours=9))

# ==========================================
# 1. 評価契約（Evaluation Contract）設定
# ==========================================
CONFIG = {
    "case_id": "BO-XXX-000",
    "domain_mode": "BO_STANDARD",        # BO_STANDARD | BO_ONETOUCH | FX_EXPANSION
    "is_end_timestamp": "2021-12-31 23:59:59",  # これ以降のデータが混入したら強制停止
    "payout_ratio": 0.85,                # BO 1.85倍 -> 損益分岐 54.054054%
    "fx_risk_pct": 0.01,                 # FX 1トレード1%リスク
    "friction_pips": [0.0, 0.1, 0.2, 0.3],
    "pip_size": 0.0001,                  # USDJPY等クロス円の場合は 0.01 に変更
    "min_cell_samples": 100,             # 局所スパイク排除用の最小サンプル数基準
}

def calc_sha256(filepath: Path) -> str:
    """正本ファイルのSHA256ハッシュを算出"""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def verify_gate1_ledger_and_lock(df: pd.DataFrame, time_col: str = "decision_time") -> dict:
    """Gate 1: OOS未閲覧ロックの強制確認と台帳連続性チェック"""
    df[time_col] = pd.to_datetime(df[time_col])
    max_time = df[time_col].max()
    is_limit = pd.to_datetime(CONFIG["is_end_timestamp"])

    # OOS期間混入時は例外を出して物理遮断
    if max_time > is_limit:
        raise RuntimeError(
            f"[CRITICAL VIOLATION] OOS期間のデータが混入しています: max={max_time} > limit={is_limit}"
        )

    ohlc_violation = 0
    if {"open", "high", "low", "close"}.issubset(df.columns):
        bad_h = df["high"] < df[["open", "close"]].max(axis=1)
        bad_l = df["low"] > df[["open", "close"]].min(axis=1)
        ohlc_violation = int((bad_h | bad_l).sum())

    return {
        "total_rows": int(len(df)),
        "min_time": str(df[time_col].min()),
        "max_time": str(max_time),
        "oos_locked": True,
        "ohlc_violations": ohlc_violation,
        "gate1_pass": (len(df) > 0 and ohlc_violation == 0),
    }

def calc_hac_clb975(wins: np.ndarray, max_lag: int = 5) -> float:
    """Gate 2: 系列相関を考慮したNewey-West HAC頑健標準誤差による97.5%片側信頼下限"""
    n = len(wins)
    if n < 30:
        return 0.0
    p_hat = float(np.mean(wins))
    u = wins - p_hat
    gamma_0 = np.dot(u, u) / n
    hac_var = gamma_0
    for lag in range(1, min(max_lag + 1, n)):
        weight = 1.0 - lag / (max_lag + 1.0)
        gamma_l = np.dot(u[lag:], u[:-lag]) / n
        hac_var += 2.0 * weight * gamma_l
    se_hac = np.sqrt(max(hac_var, 1e-12) / n)
    return float(p_hat - 1.959964 * se_hac)

def evaluate_bo_standard_with_friction(
    df: pd.DataFrame, direction_col: str, entry_open_col: str, expiry_close_col: str
) -> dict:
    """Gate 2 & Gate 5: 次足始値参入・同値LOSE・価格摩擦負荷（+0.1〜+0.3 pip）の検証"""
    be_winrate = 1.0 / (1.0 + CONFIG["payout_ratio"])
    results = {}

    entry = df[entry_open_col].to_numpy(dtype=float)
    expiry = df[expiry_close_col].to_numpy(dtype=float)
    direction = df[direction_col].to_numpy(dtype=int)  # 1: HIGH(CALL), -1: LOW(PUT)

    for fp in CONFIG["friction_pips"]:
        shift = fp * CONFIG["pip_size"]
        # 不利方向へ参入価格をシフト、同値(Draw: diff == 0)は厳格にLOSE(0)扱い
        diff = (expiry - (entry + direction * shift)) * direction
        wins = (diff > 0.0).astype(float)
        n = len(wins)
        wr = float(np.mean(wins)) if n > 0 else 0.0
        clb = calc_hac_clb975(wins) if n >= 30 else 0.0
        ev = wr * CONFIG["payout_ratio"] - (1.0 - wr)

        results[f"friction_{fp:.1f}pip"] = {
            "n": int(n),
            "win_rate": round(wr, 6),
            "clb_975": round(clb, 6),
            "ev_per_unit": round(ev, 6),
            "beats_breakeven_raw": wr > be_winrate,
            "beats_breakeven_clb975": clb > be_winrate,
        }
    return results

def audit_non_cumulative_marginal_plateau(
    df: pd.DataFrame, param_col: str, win_col: str
) -> list:
    """
    Gate 3: 累積条件(<=)の入れ子による『擬似プラトー』を防ぐため、
    パラメータの各値（非累積の独立スライス）ごとの成績と隣接差分を出力する
    """
    be_winrate = 1.0 / (1.0 + CONFIG["payout_ratio"])
    marginals = []
    for val, grp in df.groupby(param_col, sort=True):
        wins = grp[win_col].to_numpy(dtype=float)
        n = len(wins)
        wr = float(np.mean(wins)) if n > 0 else 0.0
        clb = calc_hac_clb975(wins)
        marginals.append({
            "param": param_col,
            "exact_value_slice": val,
            "n": int(n),
            "win_rate": round(wr, 6),
            "clb_975": round(clb, 6),
            "is_valid_sample_size": n >= CONFIG["min_cell_samples"],
            "slice_beats_be": (wr > be_winrate) and (n >= CONFIG["min_cell_samples"]),
        })
    return marginals

def export_spark_handover_manifest(
    output_path: Path,
    ledger_path: Path,
    script_path: Path,
    gate1_summary: dict,
    control_vs_candidate: dict,
    friction_summary: dict,
    marginal_summary: list,
    gemini_decision: str,
) -> None:
    """水曜のGemini検証からSpark独立監査・金曜第3工程へ引き継ぐ正本JSONマニフェスト"""
    manifest = {
        "schema_version": "2.2",
        "generated_at_jst": datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S"),
        "case_id": CONFIG["case_id"],
        "domain_mode": CONFIG["domain_mode"],
        "asset_hashes": {
            "opportunity_ledger_csv": ledger_path.name,
            "opportunity_ledger_sha256": calc_sha256(ledger_path) if ledger_path.exists() else "unknown",
            "validator_script_py": script_path.name,
            "validator_script_sha256": calc_sha256(script_path) if script_path.exists() else "unknown",
        },
        "verification_status": "実行確認済み",  # AGENTS.md 4区分準拠
        "gate1_ledger_and_lock": gate1_summary,
        "gate2_and_gate5_friction": friction_summary,
        "gate3_non_cumulative_marginals": marginal_summary,
        "gate4_control_vs_candidate": control_vs_candidate,
        "gemini_stage2_decision": gemini_decision,  # 採用候補 / 棄却 / 保留
    }
    output_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")