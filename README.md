# CMSC6950 Final Project  
## Time-Series Forecasting of Daily Average Temperature

### Author: Priyanka Kumaran  
### Semester: Fall 2025  

---

## 1. Project Summary

This project analyzes more than a century of daily temperature records for station **IN009010100** (NOAA GHCN).  
The goals of the project are to:

- Process and clean the temperature time-series dataset  
- Explore temporal variability (daily, monthly, decadal)  
- Detect extreme heat events using a custom function  
- Study how results change under different threshold definitions  
- Identify long-term statistical trends in temperature and extreme events  
- Produce reproducible figures from a standalone Python script  

All code, tests, and figures follow the CMSC6950 project requirements.

---

## 2. Dataset

The dataset is retrieved automatically from the **NOAA Daily Global Historical Climatology Network (GHCN)** API.

- **Variables used:** TAVG, TMAX, TMIN, PRCP  
- **Time period:** 1901–2024  
- **Download method:** The dataset is downloaded directly inside `make_figures.py`  
- **Missing values:** Filled via time interpolation and basic correction steps  

No local data files are required.

---

## 3. Custom Function: `extreme_days()`

Defined in **analysis.py**, this function:

- Computes whether each day exceeds a temperature threshold  
- Counts the number of extreme days per year  
- Returns a yearly time-series of extreme-event counts  
- Raises a ValueError if `TMAX` is missing  

This function is used in all extreme-event analyses.  
(See full tests in `test_analysis.py`.)

---

## 4. Running the Project

### Install required packages:
```bash
pip install pandas matplotlib seaborn scipy pytest

Generate all figures used in the report:
python make_figures.py


This creates a folder:

figures/


containing all final images.

Run unit tests:
pytest


Tests verify correctness across:

Normal cases

Edge cases (duplicates, leap years, unsorted index)

Negative temperatures

Performance

Mixed data types

## 5. Reproducible Figures (Script-Generated)

make_figures.py produces all figures required in the report:

Daily Average Temperature Time Series

Annual Mean Temperature Trend + Regression Line

Extreme Hot Days Per Year (threshold = mean + 2σ)

Sensitivity Analysis (2σ, 2.5σ, 3σ thresholds)

Trend in Extreme Heat Events

Rolling 365-Day Temperature Variability

Monthly Variability of TMAX

Decadal Variability of TMAX

All figures are saved reproducibly without using Jupyter Notebook.

## 6. File Structure
project/
│
├── analysis.py                 # extreme_days() implementation
├── test_analysis.py            # full unit test suite
├── make_figures.py             # generates all figures for the report
├── temperature_variability_analysis.ipynb   # development notebook (not graded)
├── figures/                    # auto-generated figures
└── README.md                   # project documentation
