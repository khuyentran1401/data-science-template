import pandas as pd
import pytest
from pandas.testing import assert_frame_equal, assert_series_equal
from src.process import drop_columns, get_X_y


@pytest.fixture
def data():
    return pd.DataFrame({"X1": [1, 2], "X2": [3, 4], "Y": [0, 1]})


def test_drop_columns(data):
    res = drop_columns.fn(data, columns=["X1"])
    expected = pd.DataFrame({"X2": [3, 4], "Y": [0, 1]})
    assert_frame_equal(res, expected)


def test_get_X_y(data):
    X, y = get_X_y.fn(data, label="Y")
    X_expected = pd.DataFrame({"X1": [1, 2], "X2": [3, 4]})
    Y_expected = pd.Series([0, 1], name="Y")
    assert_frame_equal(X, X_expected)
    assert_series_equal(y, Y_expected)
