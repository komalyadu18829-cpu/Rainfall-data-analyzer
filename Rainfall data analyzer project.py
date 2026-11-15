import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ------------------------------
# Rainfall Data Analyzer
# ------------------------------

FILE_NAME = "rain.csv"


# Load and validate CSV file
def load_data():

    try:
        df = pd.read_csv(
            FILE_NAME,
            dtype=str,
            keep_default_na=False,
            on_bad_lines="skip"
        )

        if not {"Month", "Rainfall_mm"}.issubset(df.columns):
            print("Error: CSV must contain Month and Rainfall_mm columns.")
            return pd.DataFrame(columns=["Month", "Rainfall_mm"])

        valid_data = []

        for i, row in df.iterrows():

            month = str(row["Month"]).strip()
            rainfall = str(row["Rainfall_mm"]).strip()

            if not month:
                print(f"Row {i + 1} skipped: Month is missing.")
                continue

            try:
                value = float(rainfall)

            except (ValueError, TypeError):
                print(
                    f"Row {i + 1} skipped: "
                    f"invalid Rainfall '{rainfall}'."
                )
                continue

            if not np.isfinite(value):
                print(
                    f"Row {i + 1} skipped: "
                    f"invalid Rainfall '{rainfall}'."
                )
                continue

            if value < 0:
                print(
                    f"Row {i + 1} skipped: "
                    "Rainfall cannot be negative."
                )
                continue

            valid_data.append([month, value])

        return pd.DataFrame(
            valid_data,
            columns=["Month", "Rainfall_mm"]
        )

    except FileNotFoundError:
        print("Error: rain.csv file not found.")
        return pd.DataFrame(columns=["Month", "Rainfall_mm"])

    except Exception as e:
        print("Error loading CSV:", e)
        return pd.DataFrame(columns=["Month", "Rainfall_mm"])


# Calculate statistics using NumPy
def show_statistics(df):

    if df.empty:
        print("No valid rainfall data available.")
        return

    rainfall = df["Rainfall_mm"].to_numpy()

    total = np.sum(rainfall)
    mean = np.mean(rainfall)
    maximum = np.max(rainfall)
    minimum = np.min(rainfall)
    std_dev = np.std(rainfall)

    max_month = df.loc[
        df["Rainfall_mm"].idxmax(), "Month"
    ]

    min_month = df.loc[
        df["Rainfall_mm"].idxmin(), "Month"
    ]

    print("\n========== RAINFALL STATISTICS ==========")

    print(f"Total: {total:g} mm")
    print(f"Mean: {mean:.2f} mm")
    print(f"Max: {max_month} ({maximum:g})")
    print(f"Min: {min_month} ({minimum:g})")
    print(f"Std Dev: {std_dev:.2f}")

    # Heavy rainfall means more than 200 mm
    heavy = df[df["Rainfall_mm"] > 200]

    if heavy.empty:
        print("No month above 200 mm")
    else:
        months = ", ".join(heavy["Month"].tolist())
        print("Heavy rainfall months:", months)


# Compare rainfall with average
def compare_average(df):

    if df.empty:
        print("No valid rainfall data available.")
        return

    mean = np.mean(df["Rainfall_mm"])

    above = df[df["Rainfall_mm"] > mean]
    below = df[df["Rainfall_mm"] < mean]

    print(f"\nAverage Rainfall: {mean:.2f} mm")

    if not above.empty:
        result = " | ".join(
            f"{row['Month']} ({row['Rainfall_mm']:g})"
            for _, row in above.iterrows()
        )
        print("Above average:", result)
    else:
        print("No month above average.")

    if not below.empty:
        result = " | ".join(
            f"{row['Month']} ({row['Rainfall_mm']:g})"
            for _, row in below.iterrows()
        )
        print("Below average:", result)
    else:
        print("No month below average.")


# Display Bar and Line Charts
def plot_charts(df):

    if df.empty:
        print("No data available for plotting.")
        return

    months = df["Month"]
    rainfall = df["Rainfall_mm"]

    # Bar Chart
    plt.figure(figsize=(9, 5))
    plt.bar(months, rainfall)

    plt.title("Monthly Rainfall - Bar Chart")
    plt.xlabel("Months")
    plt.ylabel("Rainfall (mm)")
    plt.grid(axis="y")
    plt.tight_layout()

    # Line Chart
    plt.figure(figsize=(9, 5))
    plt.plot(months, rainfall, marker="o")

    plt.title("Monthly Rainfall - Line Chart")
    plt.xlabel("Months")
    plt.ylabel("Rainfall (mm)")
    plt.grid(True)
    plt.tight_layout()

    print("\nBar chart and Line chart displayed.")

    plt.show()


# Main Menu
def main():

    df = load_data()

    if df.empty:
        print("No valid data found. Please check rain.csv.")
        return

    while True:

        print("\n========== RAINFALL DATA ANALYZER ==========")
        print("1. Statistics")
        print("2. Display Charts")
        print("3. Compare with Average and Plot")
        print("4. Show All Analysis")
        print("0. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            show_statistics(df)

        elif choice == "2":
            plot_charts(df)

        elif choice == "3":
            compare_average(df)
            plot_charts(df)

        elif choice == "4":
            show_statistics(df)
            compare_average(df)
            plot_charts(df)

        elif choice == "0":
            print("Thank you for using Rainfall Data Analyzer!")
            break

        else:
            print("Invalid choice! Please select 0 to 4.")


# Program execution
if __name__ == "__main__":
    main()
