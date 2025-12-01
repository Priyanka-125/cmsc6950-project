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
Run:

```bash
pip install pandas matplotlib seaborn scipy pytest
```
### **1. Generate All Figures**
```bash
python make_figures.py
```
This script will:

-Download NOAA climate data

-Clean and interpolate gaps

-Calculate yearly/decadal metrics

-Identify extreme heat events under multiple thresholds

-Save all 8 reproducible figures into the /figures folder
### **2. Run Unit Tests**

Tests ensure the core function behaves correctly under many scenarios:

```bash
pytest -v
python -m pytest -q                                             
```

---
## 📊 Figures Produced

1. **Daily Average Temperature Time Series**  
2. **Annual Mean Temperature Trend + Regression Line**  
3. **Extreme Hot Days Per Year (Mean + 2σ)**  
4. **Sensitivity Analysis (2σ, 2.5σ, 3σ)**  
5. **Trend in Extreme Days**  
6. **Rolling 365-Day Variability (TMAX)**  
7. **Monthly Variability (Std Dev by Month)**  
8. **Decadal Variability (Std Dev by Decade)**  

All figures are reproducible by running the standalone script.

---

## 📂 Repository Structure
```
project/
│
├── analysis.py                     # Contains extreme_days() logic
├── make_figures.py                 # Main script that regenerates all figures
├── test_analysis.py                # Full unit tests for extreme_days()
├── temperature_variability_analysis.ipynb   # Notebook used during development
│
└── figures/                        # Output images (generated automatically)
```

---


## 📚 Citation

NOAA National Centers for Environmental Information (NCEI),  
Daily Global Historical Climatology Network (GHCN).

---

## ✅ Final Deliverables

- `make_figures.py` (complete reproducible pipeline)  
- All figures inside `/figures/`  
- `analysis.py` + `test_analysis.py` (full tested logic)  
- README.md (this file)

---

