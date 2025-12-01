import pandas as pd

def extreme_days(df, threshold):
    """
    Count extreme temperature days per year.
    threshold: value above which a day is considered extreme.
    """
    if 'TMAX' not in df.columns:
        raise ValueError("Input DataFrame must contain a 'TMAX' column.")

    extreme_mask = df['TMAX'] > threshold
    counts = extreme_mask.resample('YE').sum()

    return counts
