"""判定時刻までに確定した足だけを選ぶ最小ユーティリティ。"""

import pandas as pd


def available_bars(bars: pd.DataFrame, decision_time: pd.Timestamp) -> pd.DataFrame:
    """CloseTime <= decision_time の行を返す。補間・時差推定はしない。

    CloseTime はタイムゾーン付きdatetime列、判定時刻もタイムゾーン必須。
    入力は変更せず、利用可能な足がなければ空のDataFrameを返す。
    実データの配信遅延・生成元・足の定義は呼び出し側で確認する。
    """
    close_times = bars["CloseTime"]
    if not isinstance(close_times.dtype, pd.DatetimeTZDtype):
        raise ValueError("CloseTimeにはタイムゾーン付きdatetime列が必要です")
    decision_time = pd.Timestamp(decision_time)
    if decision_time.tzinfo is None or pd.isna(decision_time):
        raise ValueError("判定時刻には有効なタイムゾーン付き時刻が必要です")
    if close_times.isna().any():
        raise ValueError("CloseTimeの欠損は許容しません")
    return bars.loc[close_times <= decision_time].copy()
