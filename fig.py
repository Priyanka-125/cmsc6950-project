import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


STATION_ID = "IN009010100"   # Bangalore station (NOAA/NCEI)
START_DATE = "1901-01-01"
END_DATE   = "2024-04-15"
UNITS      = "metric"
CITY_LABEL = "Bangalore, India"  
OUT_DIR    = Path("figures")
OUT_FILE   = OUT_DIR / "figure1_daily_avg_temperature.png"

# NOAA NCEI Daily Summaries CSV endpoint
URL = (
    "https://www.ncei.noaa.gov/access/services/data/v1?"
    "dataset=daily-summaries"
    "&dataTypes=TAVG,TMAX,TMIN,PRCP"
    f"&stations={STATION_ID}"
    f"&startDate={START_DATE}&endDate={END_DATE}"
    "&includeStationName=true&includeStationLocation=1"
    f"&units={UNITS}&format=csv"
)

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load data
    df = pd.read_csv(URL)
    df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
    df = df.sort_values("DATE").dropna(subset=["DATE"])

    # Ensure numeric columns
    for col in ["TAVG", "TMAX", "TMIN", "PRCP"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Impute TAVG from TMAX/TMIN when possible
    mask = df["TAVG"].isna() & df["TMAX"].notna() & df["TMIN"].notna()
    df.loc[mask, "TAVG"] = (df.loc[mask, "TMAX"] + df.loc[mask, "TMIN"]) / 2
    df = df.dropna(subset=["TAVG"])

    # 30-day rolling mean for smooth trend
    df["TAVG_30d"] = df["TAVG"].rolling(window=30, min_periods=15, center=True).mean()

    # Plot WITH city name in the title
    plt.figure(figsize=(12, 5))
    plt.plot(df["DATE"], df["TAVG"], linewidth=0.6, alpha=0.6, label="Daily TAVG (°C)")
    plt.plot(df["DATE"], df["TAVG_30d"], linewidth=1.8, label="30-day mean (°C)")
    plt.title(f"{CITY_LABEL} — Daily Average Temperature Over Time", loc="left")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.grid(True, linewidth=0.3, alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_FILE, dpi=200)
    print(f"[OK] Figure saved → {OUT_FILE}")

if __name__ == "__main__":
    main()
