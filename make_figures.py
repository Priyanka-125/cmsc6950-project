import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
from analysis import extreme_days
import seaborn as sns


# ----------------------------------------------------------
# Setup
# ----------------------------------------------------------

# Create folder for figures
os.makedirs("figures", exist_ok=True)

# NOAA dataset URL (same as in your notebook)
URL = (
    "https://www.ncei.noaa.gov/access/services/data/v1?"
    "dataset=daily-summaries&dataTypes=TAVG,TMAX,TMIN,PRCP"
    "&stations=IN009010100&startDate=1901-01-01&endDate=2024-04-15"
    "&includeStationName=true&includeStationLocation=1&units=metric"
)

print("Downloading dataset...")
df = pd.read_csv(URL, parse_dates=["DATE"], index_col="DATE", na_values=["NaN"])
print("Initial shape:", df.shape)

# ----------------------------------------------------------
# Data Cleaning & Preprocessing (same as notebook)
# ----------------------------------------------------------

# Interpolate gaps smoothly and fill remaining NaN
df = df.interpolate(method="time").ffill().bfill()

# Keep only needed columns
data = df[["TAVG", "TMAX", "TMIN", "PRCP"]].copy()

# Fix missing TAVG using mean of TMIN and TMAX
mask = data["TAVG"].isna()
data.loc[mask, "TAVG"] = (data.loc[mask, "TMAX"] + data.loc[mask, "TMIN"]) / 2

# Drop any remaining missing rows
data = data.dropna()

# ----------------------------------------------------------
# FIGURE 1: Daily Average Temperature Time Series
# ----------------------------------------------------------

plt.figure(figsize=(14, 5))
plt.plot(data.index, data["TAVG"], color="blue")
plt.title("Daily Average Temperature Over Time")
plt.xlabel("Year")
plt.ylabel("Temperature (°C)")
plt.grid(True)
plt.savefig("figures/01_daily_avg_temperature.png", dpi=200)
plt.close()

# ----------------------------------------------------------
# FIGURE 2: Annual Mean Temperature Trend (+ regression line)
# ----------------------------------------------------------

annual_mean = data["TAVG"].resample("YE").mean()
years = annual_mean.index.year

slope, intercept, r, p, se = linregress(years, annual_mean.values)

plt.figure(figsize=(14, 5))
plt.plot(years, annual_mean.values, marker="o", label="Annual Mean Temperature")
plt.plot(years, intercept + slope * years, "r--", label="Trend Line")
plt.title("Annual Mean Temperature Trend")
plt.xlabel("Year")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.grid(True)
plt.savefig("figures/02_annual_mean_trend.png", dpi=200)
plt.close()

# ----------------------------------------------------------
# FIGURE 3: Extreme Days Per Year (Threshold = Mean + 2σ)
# ----------------------------------------------------------

mean = data["TMAX"].mean()
std = data["TMAX"].std()
threshold_main = mean + 2 * std

extreme_counts = extreme_days(data, threshold_main)

plt.figure(figsize=(14, 5))
plt.bar(extreme_counts.index.year, extreme_counts.values)
plt.title(f"Extreme Hot Days Per Year (Threshold = Mean + 2σ = {threshold_main:.2f}°C)")
plt.xlabel("Year")
plt.ylabel("Number of Extreme Days")
plt.grid(True)
plt.savefig("figures/03_extreme_days_mean_plus_2sd.png", dpi=200)
plt.close()

# ----------------------------------------------------------
# FIGURE 4: Sensitivity Analysis (Mean + 2σ, 2.5σ, 3σ)
# ----------------------------------------------------------

thresholds = {
    "Mean + 2σ": mean + 2 * std,
    "Mean + 2.5σ": mean + 2.5 * std,
    "Mean + 3σ": mean + 3 * std,
}

plt.figure(figsize=(14, 5))

for label, th in thresholds.items():
    counts = extreme_days(data, th)
    plt.plot(counts.index.year, counts.values, label=f"{label} ({th:.1f}°C)")

plt.title("Sensitivity of Extreme Temperature Days to Threshold Choice")
plt.xlabel("Year")
plt.ylabel("Number of Extreme Days")
plt.legend()
plt.grid(True)
plt.savefig("figures/04_sensitivity_analysis.png", dpi=200)
plt.close()

# ----------------------------------------------------------
# FIGURE 5: Trend in Extreme Hot Days (Mean + 2σ)
# ----------------------------------------------------------

extreme_main = extreme_days(data, threshold_main)
years_ext = extreme_main.index.year

slope2, intercept2, r2, p2, se2 = linregress(years_ext, extreme_main.values)

plt.figure(figsize=(14, 5))
plt.plot(years_ext, extreme_main.values, marker="o", label="Extreme Days")
plt.plot(years_ext, intercept2 + slope2 * years_ext, "r--", label="Trend Line")
plt.title("Trend in Yearly Extreme Hot Days (Mean + 2σ)")
plt.xlabel("Year")
plt.ylabel("Extreme Days")
plt.legend()
plt.grid(True)
plt.savefig("figures/05_extreme_days_trend.png", dpi=200)
plt.close()

# ----------------------------------------------------------
# FIGURE 6: Rolling 365-Day Variability in TMAX
# ----------------------------------------------------------

data["rolling_std_TMAX"] = data["TMAX"].rolling(365).std()

plt.figure(figsize=(14, 5))
plt.plot(data["rolling_std_TMAX"], color="purple")
plt.title("Rolling 365-Day Variability in Daily Maximum Temperature")
plt.xlabel("Year")
plt.ylabel("Standard Deviation (°C)")
plt.grid(True)
plt.savefig("figures/06_rolling_variability.png", dpi=200)
plt.close()

# ----------------------------------------------------------
# FIGURE 7: Monthly Variability of Daily Maximum Temperature
# ----------------------------------------------------------

monthly_variability = data["TMAX"].groupby(data.index.month).std()

plt.figure(figsize=(10, 5))
sns.barplot(x=monthly_variability.index, y=monthly_variability.values, palette="viridis")
plt.title("Monthly Variability of Daily Maximum Temperature")
plt.xlabel("Month")
plt.ylabel("Standard Deviation (°C)")
plt.grid(True)
plt.savefig("figures/07_monthly_variability.png", dpi=200)
plt.close()

# ----------------------------------------------------------
# FIGURE 8: Decadal Variability of TMAX
# ----------------------------------------------------------

data["decade"] = (data.index.year // 10) * 10
decadal_variability = data.groupby("decade")["TMAX"].std()

plt.figure(figsize=(12, 5))
plt.plot(decadal_variability.index, decadal_variability.values, marker="o")
plt.title("Decadal Variability of Daily Maximum Temperature")
plt.xlabel("Decade")
plt.ylabel("Standard Deviation (°C)")
plt.grid(True)
plt.savefig("figures/08_decadal_variability.png", dpi=200)
plt.close()

print("✔ All figures generated and saved in /figures")
