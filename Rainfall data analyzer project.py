import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def format_num(val: float) -> str:
    """Format whole numbers without decimals and fractional values to 2 decimal places."""
    if float(val).is_integer():
        return str(int(val))
    return f"{val:.2f}"


def load_rainfall_data(filepath: str = "rain.csv") -> tuple[pd.DataFrame, int]:
    """Load CSV with Pandas and validate missing, non-numeric, or negative readings."""
    try:
        raw_df = pd.read_csv(filepath, dtype=str, keep_default_na=False)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)

    if "Month" not in raw_df.columns or "Rainfall_mm" not in raw_df.columns:
        print("Error: CSV must contain 'Month' and 'Rainfall_mm' columns.")
        sys.exit(1)

    valid_rows = []
    skipped_count = 0

    for row_num, row in enumerate(raw_df.itertuples(index=False), start=1):
        month = str(row.Month).strip()
        raw_val = str(row.Rainfall_mm).strip()

        if not month:
            print(f"Row {row_num} skipped: missing Month")
            skipped_count += 1
            continue

        if raw_val == "":
            print(f"Row {row_num} skipped: invalid Rainfall '{raw_val}'")
            skipped_count += 1
            continue

        try:
            rainfall_val = float(raw_val)
            if np.isnan(rainfall_val) or np.isinf(rainfall_val):
                raise ValueError
        except ValueError:
            print(f"Row {row_num} skipped: invalid Rainfall '{raw_val}'")
            skipped_count += 1
            continue

        if rainfall_val < 0:
            print(f"Row {row_num} skipped: Rainfall cannot be negative")
            skipped_count += 1
            continue

        valid_rows.append((month, rainfall_val))

    clean_df = pd.DataFrame(valid_rows, columns=["Month", "Rainfall_mm"])

    if skipped_count > 0:
        total_valid = float(np.sum(clean_df["Rainfall_mm"].to_numpy(dtype=float))) if len(clean_df) > 0 else 0.0
        print(f"Valid rows: {len(clean_df)} | Total: {format_num(total_valid)} mm")

    return clean_df, skipped_count


def show_statistics(df: pd.DataFrame) -> None:
    """Compute and display rainfall statistics using NumPy and boolean filtering."""
    if df.empty:
        print("No valid rainfall data available.")
        return

    months = df["Month"].to_numpy()
    rainfall = df["Rainfall_mm"].to_numpy(dtype=float)

    total = float(np.sum(rainfall))
    mean = float(np.mean(rainfall))
    std_dev = float(np.std(rainfall))  # Population standard deviation (ddof=0)

    # Boolean filtering for heavy-rainfall months (> 200 mm)
    heavy_mask = rainfall > 200
    heavy_months = months[heavy_mask]

    if len(df) == 1:
        print(f"Total: {format_num(total)} mm | Mean: {mean:.2f} | Std Dev: {std_dev:.2f}")
    else:
        max_idx = int(np.argmax(rainfall))
        min_idx = int(np.argmin(rainfall))
        print(f"Total: {format_num(total)} mm | Mean: {mean:.2f}")
        print(f"Max: {months[max_idx]} ({format_num(rainfall[max_idx])}) | Min: {months[min_idx]} ({format_num(rainfall[min_idx])})")
        print(f"Std Dev: {std_dev:.2f}")

    if len(heavy_months) > 0:
        print(f"Heavy rainfall months: {', '.join(heavy_months)}")
    else:
        print("No month above 200 mm")


def plot_line_trend(df: pd.DataFrame) -> None:
    """Plot a Matplotlib line chart showing the monthly rainfall trend."""
    if df.empty:
        print("No valid rainfall data available to plot.")
        return

    months = df["Month"].to_numpy()
    rainfall = df["Rainfall_mm"].to_numpy(dtype=float)

    plt.figure(figsize=(8, 5))
    plt.plot(months, rainfall, marker="o", linestyle="-", linewidth=2, color="#1f77b4", label="Rainfall (mm)")
    plt.title("Monthly Rainfall Trend")
    plt.xlabel("Month")
    plt.ylabel("Rainfall (mm)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()
    print("Line chart 'Monthly Rainfall Trend' displayed")


def compare_with_average_and_plot(df: pd.DataFrame) -> None:
    """Compare monthly rainfall against the mean using boolean filtering and plot a bar chart."""
    if df.empty:
        print("No valid rainfall data available.")
        return

    months = df["Month"].to_numpy()
    rainfall = df["Rainfall_mm"].to_numpy(dtype=float)
    mean = float(np.mean(rainfall))

    # Boolean filtering for above-average and below-average months
    above_mask = rainfall > mean
    below_mask = rainfall < mean

    above_items = [f"{m} ({format_num(r)})" for m, r in zip(months[above_mask], rainfall[above_mask])]
    below_items = [f"{m} ({format_num(r)})" for m, r in zip(months[below_mask], rainfall[below_mask])]

    above_str = " | ".join(above_items) if above_items else "None"
    below_str = " | ".join(below_items) if below_items else "None"

    print(f"Above average ({mean:.2f}): {above_str}")
    print(f"Below average: {below_str}")

    plt.figure(figsize=(8, 5))
    colors = ["#2ca02c" if r > mean else "#ff7f0e" for r in rainfall]
    plt.bar(months, rainfall, color=colors, edgecolor="black", alpha=0.85)
    plt.axhline(mean, color="red", linestyle="--", linewidth=1.5, label=f"Average ({mean:.2f} mm)")
    plt.title("Monthly Rainfall")
    plt.xlabel("Month")
    plt.ylabel("Rainfall (mm)")
    plt.legend()
    plt.tight_layout()
    plt.show()
    print("Bar chart 'Monthly Rainfall' displayed")


def main() -> None:
    df, _ = load_rainfall_data("rain.csv")

    while True:
        print("\n--- Rainfall Data Analyzer ---")
        print("1. Statistics")
        print("2. Plot Rainfall Trend (Line Chart)")
        print("3. Compare with Average and Plot (Bar Chart)")
        print("4. Exit")

        try:
            choice = input("Enter menu option (1-4): ").strip()
        except EOFError:
            break

        if choice == "1":
            show_statistics(df)
        elif choice == "2":
            plot_line_trend(df)
        elif choice == "3":
            compare_with_average_and_plot(df)
        elif choice == "4":
            print("Exiting Rainfall Data Analyzer.")
            break
        else:
            print("Invalid option. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
