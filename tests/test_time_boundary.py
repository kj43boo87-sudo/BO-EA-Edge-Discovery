"""実市場データではない人工CSVによる時刻境界テスト。"""
from pathlib import Path

import pandas as pd
import pytest

from bo_validation.time_boundary import available_bars


@pytest.fixture
def bars():
    frame = pd.read_csv(Path(__file__).parents[1] / "data/sample/bars.csv")
    frame["CloseTime"] = pd.to_datetime(frame["CloseTime"])
    return frame


def test_excludes_future_bars(bars):
    original = bars.copy(deep=True)
    result = available_bars(bars, pd.Timestamp("2026-01-01T09:12:00+09:00"))
    assert result["Close"].tolist() == [100, 101]
    pd.testing.assert_frame_equal(bars, original)


def test_includes_equal_close_time(bars):
    result = available_bars(bars, pd.Timestamp("2026-01-01T09:10:00+09:00"))
    assert result["Close"].tolist() == [100, 101]


def test_no_future_backfill(bars):
    result = available_bars(bars, pd.Timestamp("2026-01-01T09:04:00+09:00"))
    assert result.empty
    assert result.columns.tolist() == bars.columns.tolist()


def test_equivalent_utc_decision_time(bars):
    result = available_bars(bars, pd.Timestamp("2026-01-01T00:10:00Z"))
    assert result["Close"].tolist() == [100, 101]


def test_rejects_naive_decision_time(bars):
    with pytest.raises(ValueError, match="タイムゾーン"):
        available_bars(bars, pd.Timestamp("2026-01-01T09:10:00"))


def test_rejects_naive_close_times(bars):
    bars["CloseTime"] = bars["CloseTime"].dt.tz_localize(None)
    with pytest.raises(ValueError, match="タイムゾーン"):
        available_bars(bars, pd.Timestamp("2026-01-01T09:10:00+09:00"))


def test_rejects_missing_close_time(bars):
    bars.loc[0, "CloseTime"] = pd.NaT
    with pytest.raises(ValueError, match="欠損"):
        available_bars(bars, pd.Timestamp("2026-01-01T09:10:00+09:00"))


@pytest.mark.parametrize("operation", ["modify", "delete", "append"])
def test_future_data_changes_do_not_change_past_result(bars, operation):
    decision = pd.Timestamp("2026-01-01T09:10:00+09:00")
    expected = available_bars(bars, decision)
    future = bars["CloseTime"] > decision
    altered = bars.copy(deep=True)
    if operation == "modify":
        altered.loc[future, "Close"] = -999999
    elif operation == "delete":
        altered = altered.loc[~future]
    else:
        extra = altered.loc[future].copy()
        extra["CloseTime"] += pd.Timedelta(days=1)
        extra["Close"] = 123456
        altered = pd.concat([altered, extra], ignore_index=True)
    pd.testing.assert_frame_equal(available_bars(altered, decision), expected)
