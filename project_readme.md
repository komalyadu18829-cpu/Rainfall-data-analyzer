# Rainfall Data Analyzer

A Python-based command-line data analysis and visualization tool designed to process, clean, and analyze monthly rainfall datasets from CSV files.

## Features

- **Automated Data Cleaning & Validation:**
  - Checks for file existence and valid CSV formatting.
  - Trims whitespace from column headers and string values.
  - Detects and skips rows with missing, non-numeric, or negative rainfall values while providing detailed console logs.
- **Statistical Analysis:**
  - Calculates total rainfall, mean (average) rainfall, and standard deviation.
  - Identifies months with the highest (Max) and lowest (Min) rainfall.
  - Highlights heavy rainfall months (exceeding $200\text{ mm}$).
- **Data Visualization:**
  - **Line Chart:** Plots the monthly rainfall trend over time.
  - **Bar Chart:** Compares monthly rainfall against the overall average with a threshold indicator line.
- **Interactive Menu Interface:** Easy-to-use CLI menu to navigate between statistics and visualizations.

## Prerequisites & Installation

Ensure you have Python 3.x installed on your system. Install the required libraries using `pip`:

```bash
pip install pandas numpy matplotlib
```

## CSV File Format

The input CSV file must contain at least two columns named `Month` and `Rainfall_mm`.

**Example (`rainfall_data.csv`):**
```csv
Month,Rainfall_mm
January,45.5
February,30
March,62.8
April,110
May,215.4
June,340.2
```

## How to Run

1. Place your CSV dataset in the same directory as the Python script (or provide the full file path).
2. Run the script from your terminal or command prompt:

```bash
python "Rainfall data analyzer project.py"
```

3. Enter the name of your CSV file when prompted (e.g., `rainfall_data.csv`).
4. Choose an option from the interactive menu (`1` to `4`):
   - `1`: View Statistical Summary
   - `2`: Display Monthly Rainfall Trend (Line Chart)
   - `3`: Compare with Average & Display Bar Chart
   - `4`: Exit the application

## Project Structure

```text
├── Rainfall data analyzer project.py   # Main application script
├── README.md                           # Project documentation and setup guide
└── SUMMARY.md                          # Executive project summary and technical overview
```