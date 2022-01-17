import os
import sys

PACKAGE_PARENT = ".."
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from src.process_data import get_age


@pytest.fixture
def data():
    return pd.DataFrame({"Year_Birth": [1999, 2000]})


def test_process_data():
    df = pd.DataFrame({"Year_Birth": [1999, 2000]})
    assert_frame_equal(
        get_age.run(df),
        pd.DataFrame({"Year_Birth": [1999, 2000], "age": [22, 21]}),
    )
