# Project Summary: Rainfall Data Analyzer

## 1. Objective
The objective of the **Rainfall Data Analyzer** project is to build a reliable, user-friendly Python application capable of ingesting raw monthly rainfall records, sanitizing corrupted or incomplete data entries, performing descriptive statistical computations, and generating clear visual insights to support weather pattern analysis.

## 2. Tools & Technologies Used
- **Language:** Python 3
- **Libraries:**
  - `pandas`: Used for CSV file ingestion, DataFrame management, and data validation.
  - `numpy`: Used for fast vectorized mathematical operations (sum, mean, standard deviation, min/max indexing).
  - `matplotlib`: Used for rendering publication-quality line and bar charts.
  - `os`: Used for file path verification and error handling.

## 3. System Workflow & Architecture
1. **Data Ingestion & Sanitization (`load_and_clean_data`):**
   - Verifies file availability and required schema (`Month`, `Rainfall_mm`).
   - Iterates through records to filter out `NaN` values, empty strings, non-numeric entries, and physically impossible negative rainfall values, reporting skipped rows to the user.
2. **Statistical Engine (`show_statistics`):**
   - Computes key metrics: Total Rainfall ($\sum$), Mean ($\mu$), Standard Deviation ($\sigma$), Maximum, and Minimum rainfall months.
   - Applies a threshold filter ($> 200\text{ mm}$) to flag extreme/heavy rainfall months.
3. **Visualization & Comparative Analysis (`plot_rainfall_trend` & `compare_with_average_and_plot`):**
   - Generates a time-series **Line Chart** to observe seasonal fluctuations.
   - Categorizes months into *Above Average* and *Below Average* groups and renders a **Bar Chart** overlaid with a horizontal mean reference line.

## 4. Key Outcomes & Learning
- **Data Integrity:** Ensures accurate statistical outputs by preventing dirty data from skewing averages or crashing visualizations.
- **Actionable Insights:** Translates raw tabular numbers into immediate visual comparisons, making it easy to identify drought months versus monsoon/heavy rainfall peaks.
- **Modular Design:** Structured into clean, single-responsibility functions for maintainability and scalability.