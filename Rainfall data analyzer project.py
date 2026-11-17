import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_and_clean_data(filename):
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return None

    try:
        df = pd.read_csv(filename)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

    # Columns ke naam se extra space hatane ke liye
    df.columns = [col.strip() for col in df.columns]

    if "Month" not in df.columns or "Rainfall_mm" not in df.columns:
        print("Error: CSV must contain 'Month' and 'Rainfall_mm' columns.")
        return None

    valid_months = []
    valid_rainfall = []

    for idx, row in df.iterrows():
        row_num = idx + 1
        month = str(row["Month"]).strip()
        raw_val = str(row["Rainfall_mm"]).strip()

        # Check for missing values
        if pd.isna(row["Rainfall_mm"]) or raw_val == "" or raw_val.lower() == "nan":
            print(f"Row {row_num} skipped: Missing Rainfall value.")
            continue

        # Check if numeric
        try:
            val = float(raw_val)
        except ValueError:
            print(f"Row {row_num} skipped: invalid Rainfall '{raw_val}'.")
            continue

        # Check for negative values
        if val < 0:
            print(f"Row {row_num} skipped: Rainfall cannot be negative.")
            continue

        valid_months.append(month)
        valid_rainfall.append(val)

    if len(valid_rainfall) < len(df):
        total_valid = np.sum(valid_rainfall) if valid_rainfall else 0
        formatted_total = (
            int(total_valid)
            if float(total_valid).is_integer()
            else round(total_valid, 2)
        )
        print(f"Valid rows: {len(valid_rainfall)} | Total: {formatted_total} mm")

    if not valid_rainfall:
        print("No valid rainfall data available for analysis.")
        return None

    return pd.DataFrame({
        "Month": valid_months,
        "Rainfall_mm": np.array(valid_rainfall, dtype=float),
    })


def format_num(val):
    return f"{int(val)}" if float(val).is_integer() else f"{val:.2f}"


def show_statistics(df):
    months = df["Month"].to_numpy()
    rain = df["Rainfall_mm"].to_numpy()

    total = np.sum(rain)
    mean_val = np.mean(rain)
    std_dev = np.std(rain)

    if len(rain) == 1:
        print(
            f"Total: {format_num(total)} mm | Mean: {mean_val:.2f} | Std Dev: {std_dev:.2f}"
        )
        if rain[0] > 200:
            print(f"Heavy rainfall months: {months[0]}")
        else:
            print("No month above 200 mm")
        return

    max_idx = np.argmax(rain)
    min_idx = np.argmin(rain)

    print(f"Total: {format_num(total)} mm | Mean: {mean_val:.2f}")
    print(
        f"Max: {months[max_idx]} ({format_num(rain[max_idx])}) | Min: {months[min_idx]} ({format_num(rain[min_idx])})"
    )
    print(f"Std Dev: {std_dev:.2f}")

    heavy_months = months[rain > 200]
    if len(heavy_months) > 0:
        print(f"Heavy rainfall months: {', '.join(heavy_months)}")
    else:
        print("No month above 200 mm")


def plot_rainfall_trend(df):
    months = df["Month"].to_numpy()
    rain = df["Rainfall_mm"].to_numpy()

    plt.figure(figsize=(8, 5))
    plt.plot(
        months,
        rain,
        marker="o",
        linestyle="-",
        color="teal",
        linewidth=2,
        markersize=8,
    )
    plt.title("Monthly Rainfall Trend", fontsize=14, fontweight="bold")
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Rainfall (mm)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()
    print("Line chart 'Monthly Rainfall Trend' displayed")


def compare_with_average_and_plot(df):
    months = df["Month"].to_numpy()
    rain = df["Rainfall_mm"].to_numpy()
    mean_val = np.mean(rain)

    above_items = [
        f"{m} ({format_num(r)})"
        for m, r in zip(months[rain > mean_val], rain[rain > mean_val])
    ]
    below_items = [
        f"{m} ({format_num(r)})"
        for m, r in zip(months[rain < mean_val], rain[rain < mean_val])
    ]

    above_str = " | ".join(above_items) if above_items else "None"
    below_str = " | ".join(below_items) if below_items else "None"

    print(f"Above average ({mean_val:.2f}): {above_str}")
    print(f"Below average: {below_str}")

    plt.figure(figsize=(8, 5))
    plt.bar(months, rain, color="royalblue", edgecolor="black", width=0.5)
    plt.axhline(
        mean_val,
        color="red",
        linestyle="--",
        linewidth=1.5,
        label=f"Average ({mean_val:.2f} mm)",
    )
    plt.title("Monthly Rainfall", fontsize=14, fontweight="bold")
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Rainfall (mm)", fontsize=12)
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()
    print("Bar chart 'Monthly Rainfall' displayed")


def main():
    print("=== Rainfall Data Analyzer ===")
    filename = input("Enter CSV file name: ").strip()

    df = load_and_clean_data(filename)
    if df is None:
        return

    while True:
        print("\n--- Menu ---")
        print("1. Statistics")
        print("2. Plot Rainfall Trend (Line Chart)")
        print("3. Compare with average and plot (Bar Chart)")
        print("4. Exit")

        choice = input("Enter menu option (1-4): ").strip()

        if choice == "1":
            show_statistics(df)
        elif choice == "2":
            plot_rainfall_trend(df)
        elif choice == "3":
            compare_with_average_and_plot(df)
        elif choice == "4":
            print("Exiting Rainfall Data Analyzer.")
            break
        else:
            print("Invalid option. Please choose between 1 and 4.")


if __name__ == "__main__":
    main()
