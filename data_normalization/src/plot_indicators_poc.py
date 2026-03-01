#!/usr/bin/env python3
import argparse
import os
from pathlib import Path

# Avoid matplotlib cache warnings in constrained environments.
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-cache")

import matplotlib.pyplot as plt
import pandas as pd


def main():
    parser = argparse.ArgumentParser(
        description="Generate proof-of-concept indicators chart from weekly normalized data."
    )
    parser.add_argument(
        "--input",
        default="../OUTPUT/weekly_growth_index_wide.csv",
        help="Path to weekly growth-index wide CSV",
    )
    parser.add_argument(
        "--output",
        default="../OUTPUT/indicators_poc.png",
        help="Output PNG path",
    )
    parser.add_argument(
        "--lookback-weeks",
        type=int,
        default=260,
        help="Number of most recent weeks to plot",
    )
    parser.add_argument(
        "--max-series",
        type=int,
        default=10,
        help="Maximum number of symbol series to plot",
    )
    parser.add_argument(
        "--rebase-window-start",
        action="store_true",
        help="Rebase each plotted series to 100 at first non-null value in the plotted window.",
    )
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)
    if "week_end" not in df.columns:
        raise SystemExit("Expected 'week_end' column in normalized wide dataset.")

    df["week_end"] = pd.to_datetime(df["week_end"], errors="coerce")
    df = df.dropna(subset=["week_end"]).sort_values("week_end")

    feature_cols = [c for c in df.columns if c != "week_end"]
    non_null_counts = (
        df[feature_cols].apply(pd.to_numeric, errors="coerce").notna().sum().sort_values(ascending=False)
    )
    selected = list(non_null_counts.head(args.max_series).index)
    if not selected:
        raise SystemExit("No series available to plot.")

    plot_df = df[["week_end"] + selected].copy()
    plot_df[selected] = plot_df[selected].apply(pd.to_numeric, errors="coerce")
    plot_df = plot_df.tail(args.lookback_weeks)

    if args.rebase_window_start:
        for col in selected:
            series = plot_df[col]
            first_valid = series.dropna()
            if first_valid.empty:
                continue
            base = float(first_valid.iloc[0])
            if base == 0:
                continue
            plot_df[col] = (series / base) * 100.0

    plt.style.use("ggplot")
    fig, ax = plt.subplots(figsize=(14, 6), dpi=120)

    for col in selected:
        ax.plot(plot_df["week_end"], plot_df[col], linewidth=1.1, label=col)

    ax.set_title("Indicators Proof of Concept (Weekly Growth Index, Rebased=100)")
    ax.set_xlabel("time")
    ax.set_ylabel("indicators")
    ax.grid(True, alpha=0.3)

    legend = ax.legend(
        loc="upper left",
        ncol=1,
        frameon=True,
        fontsize=9,
        borderpad=0.8,
        handlelength=3.5,
    )
    legend.get_frame().set_alpha(0.9)
    legend.get_frame().set_edgecolor("#555555")

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)

    print(f"saved_plot={output_path}")


if __name__ == "__main__":
    main()
