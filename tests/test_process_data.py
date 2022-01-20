import pandas as pd
from pandas.testing import assert_frame_equal

from src.process_data import (get_age, get_enrollment_years,
                              get_total_purchases, scale_features)


def test_get_age():
    df = pd.DataFrame({"Year_Birth": [1999, 2000]})
    assert_frame_equal(
        get_age(df),
        pd.DataFrame({"Year_Birth": [1999, 2000], "age": [22, 21]}),
    )


def test_get_total_purchases():
    df = pd.DataFrame({"FirstPurchases": [1, 2], "SecondPurchases": [3, 4]})
    out = get_total_purchases(df)
    assert out["total_purchases"].tolist() == [4, 6]


def test_get_enrollment_years():
    df = pd.DataFrame({"Dt_Customer": ["04-09-2012"]})
    assert_frame_equal(
        get_enrollment_years(df),
        pd.DataFrame(
            {
                "Dt_Customer": [pd.Timestamp("2012-04-09 00:00:00")],
                "enrollment_years": [10],
            }
        ),
    )


def test_scale_features():
    df = pd.DataFrame(
        {"FirstPurchases": [1, 2, 5], "SecondPurchases": [3, 4, 7]}
    )
    out = scale_features.run(df)
    assert_frame_equal(
        out,
        pd.DataFrame(
            {
                "FirstPurchases": [-0.980, -0.392, 1.373],
                "SecondPurchases": [-0.980, -0.392, 1.373],
            }
        ),
        atol=2,
    )
