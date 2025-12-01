import pandas as pd
from analysis import extreme_days
import pytest

def test_extreme_days_basic():
    # Simple dataset for one year
    df = pd.DataFrame(
        {"TMAX": [10, 20, 30, 5]},
        index=pd.to_datetime(["2000-01-01", "2000-01-02", "2000-01-03", "2000-01-04"])
    )
    result = extreme_days(df, threshold=25)

    # Expect 1 extreme day (only 30 > 25)
    assert int(result.iloc[0]) == 1


def test_extreme_days_two_years():
    # Dataset covering two years
    df = pd.DataFrame(
        {"TMAX": [30, 5, 40, 15]},
        index=pd.to_datetime(["2000-12-30", "2000-12-31", "2001-01-01", "2001-01-02"])
    )
    result = extreme_days(df, threshold=20)

    # 30 > 20 → 1 extreme in 2000
    # 40 > 20 → 1 extreme in 2001
    assert int(result.loc["2000-12-31"]) == 1
    assert int(result.loc["2001-12-31"]) == 1

def test_no_extreme_days():
    df = pd.DataFrame(
        {"TMAX": [5, 10, 15, 18]},
        index=pd.to_datetime(["2000-01-01", "2000-01-02", "2000-01-03", "2000-01-04"])
    )
    result = extreme_days(df, threshold=25)

    # All values below threshold → 0 extreme days
    assert int(result.iloc[0]) == 0

def test_all_extreme_days():
    df = pd.DataFrame(
        {"TMAX": [30, 35, 40, 45]},
        index=pd.to_datetime(["2001-01-01", "2001-01-02", "2001-01-03", "2001-01-04"])
    )
    result = extreme_days(df, threshold=20)

    # 4 extreme days in 2001
    assert int(result.iloc[0]) == 4


def test_missing_tmax_column():
    df = pd.DataFrame(
        {"TEMP": [10, 20, 30]},
        index=pd.to_datetime(["2002-01-01", "2002-01-02", "2002-01-03"])
    )

    # Should raise a ValueError
    with pytest.raises(ValueError):
        extreme_days(df, threshold=25)

def test_threshold_equal_not_extreme():
    df = pd.DataFrame(
        {"TMAX": [25, 30]},
        index=pd.to_datetime(["2003-01-01", "2003-01-02"])
    )
    result = extreme_days(df, threshold=25)

    # 25 == threshold → NOT counted
    # 30  > threshold → counted
    assert int(result.iloc[0]) == 1

def test_irregular_dates():
    df = pd.DataFrame(
        {"TMAX": [30, 32, 28, 27]},
        index=pd.to_datetime([
            "2000-01-01",
            "2000-06-15",
            "2001-02-10",
            "2001-12-31"
        ])
    )

    result = extreme_days(df, threshold=29)

    # 2000 → 30, 32 (2 extreme days)
    assert int(result.loc["2000-12-31"]) == 2

    # 2001 → 28, 27 (0 extreme days)
    assert int(result.loc["2001-12-31"]) == 0

def test_leap_year_dates():
    df = pd.DataFrame(
        {"TMAX": [10, 35, 5]},
        index=pd.to_datetime([
            "2004-02-28",
            "2004-02-29",
            "2004-03-01"
        ])
    )

    result = extreme_days(df, threshold=30)

    # Only Feb 29 is extreme
    assert int(result.iloc[0]) == 1

def test_unsorted_index():
    df = pd.DataFrame(
        {"TMAX": [40, 20, 35]},
        index=pd.to_datetime(["2005-03-01", "2005-01-01", "2005-02-01"])
    )  # leave it unsorted on purpose

    # Do NOT sort before passing to extreme_days
    result = extreme_days(df, threshold=30)

    # 40 and 35 > 30 → 2 extremes in 2005
    assert int(result.iloc[0]) == 2


def test_duplicate_dates():
    df = pd.DataFrame(
        {"TMAX": [30, 32, 31]},
        index=pd.to_datetime(["2006-01-01", "2006-01-01", "2006-01-01"])
    )

    result = extreme_days(df, threshold=29)

    # All three entries for the same day > threshold → counted
    assert int(result.iloc[0]) == 3

def test_extreme_threshold():
    df = pd.DataFrame(
        {"TMAX": [10, 20, 15]},
        index=pd.to_datetime(["2007-01-01", "2007-02-01", "2007-03-01"])
    )

    result = extreme_days(df, threshold=999)

    assert int(result.iloc[0]) == 0

def test_negative_temperatures():
    df = pd.DataFrame(
        {"TMAX": [-30, -25, -40, -10]},
        index=pd.to_datetime(["2008-01-01", "2008-01-02", "2008-01-03", "2008-01-04"])
    )

    result = extreme_days(df, threshold=-20)

    # Days > -20: only -10
    assert int(result.iloc[0]) == 1

def test_large_dataset_performance():
    dates = pd.date_range(start="2000-01-01", periods=10000, freq="D")
    temps = [i % 40 for i in range(10000)]  # Pattern repeating 0–39

    df = pd.DataFrame({"TMAX": temps}, index=dates)

    result = extreme_days(df, threshold=30)

    # Every cycle of 40 days has 9 values > 30
    expected = 9 * (10000 // 40)

    assert result.sum() == expected

def test_mixed_dtypes():
    df = pd.DataFrame(
        {"TMAX": [30, 32.5, 29.9, 33]},
        index=pd.to_datetime([
            "2009-01-01",
            "2009-01-02",
            "2009-01-03",
            "2009-01-04"
        ])
    )

    result = extreme_days(df, threshold=30)

    # 32.5 > 30, 33 > 30 → 2 extremes
    assert int(result.iloc[0]) == 2

