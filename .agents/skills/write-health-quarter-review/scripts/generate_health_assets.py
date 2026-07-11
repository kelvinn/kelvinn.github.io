#!/usr/bin/env python3
"""Render health-review assets from a LifeDB MCP export JSON file.

This script intentionally does not connect to GarminDB, SQLite, or LifeDB.
Garmin data must be exported by Codex through the LifeDB MCP server first,
then saved as JSON with the shape documented in references/lifedb-mcp-export.md.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import date, datetime, timedelta
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
from matplotlib.colors import BoundaryNorm, ListedColormap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
TIME_METRICS = ["moderate_activity_time", "vigorous_activity_time", "intensity_minutes"]
CORRELATION_METRICS = [
    "hr_min",
    "hr_max",
    "rhr_min",
    "bb_max",
    "bb_min",
    "sleep_avg",
    "steps",
    "floors",
    "moderate_activity_time",
    "vigorous_activity_time",
    "calories_active_avg",
    "stress_avg",
    "weight_avg",
]


def parse_day(value: str) -> date:
    return date.fromisoformat(value[:10])


def quarter_label_for(value: date) -> str:
    return f"Q{((value.month - 1) // 3) + 1} {value.year}"


def add_quarters(value: date, offset: int) -> date:
    quarter = ((value.month - 1) // 3) + offset
    year = value.year + quarter // 4
    target_quarter = quarter % 4
    return date(year, target_quarter * 3 + 1, 1)


def quarter_start_for(value: date) -> date:
    return date(value.year, ((value.month - 1) // 3) * 3 + 1, 1)


def quarter_windows(first_start: date, focus_start: date) -> list[tuple[str, date, date]]:
    first = quarter_start_for(first_start)
    focus = quarter_start_for(focus_start)
    windows = []
    offset = 0
    while True:
        start = add_quarters(first, offset)
        if start > focus:
            break
        end = add_quarters(start, 1) - timedelta(days=1)
        windows.append((quarter_label_for(start), start, end))
        offset += 1
    return windows


def time_to_minutes(value: object) -> float:
    if value is None or pd.isna(value):
        return np.nan
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if not text:
        return np.nan
    parts = text.split(":")
    try:
        if len(parts) == 3:
            hours, minutes, seconds = parts
            return int(hours) * 60 + int(minutes) + float(seconds) / 60
        if len(parts) == 2:
            minutes, seconds = parts
            return int(minutes) + float(seconds) / 60
        return float(text)
    except ValueError:
        return np.nan


def load_export(path: Path) -> dict:
    payload = json.loads(path.read_text())
    required = ["metadata", "daily_metrics", "vo2_max"]
    missing = [key for key in required if key not in payload]
    if missing:
        raise SystemExit(f"Missing keys in MCP export: {', '.join(missing)}")
    return payload


def to_daily_frame(rows: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    if df.empty:
        return pd.DataFrame(columns=["date"])
    df["date"] = pd.to_datetime(df["date"])
    for metric in TIME_METRICS:
        if metric in df.columns:
            df[metric] = df[metric].map(time_to_minutes)
    if "intensity_minutes" not in df.columns or df["intensity_minutes"].isna().all():
        df["intensity_minutes"] = df.get("moderate_activity_time", 0).fillna(0) + 2 * df.get("vigorous_activity_time", 0).fillna(0)
    for metric in CORRELATION_METRICS:
        if metric not in df.columns:
            df[metric] = np.nan
        df[metric] = pd.to_numeric(df[metric], errors="coerce")
    return df.sort_values("date")


def ensure_dirs(post_dir: Path) -> tuple[Path, Path]:
    image_dir = post_dir
    data_dir = post_dir / "data"
    image_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    return image_dir, data_dir


def month_export(df: pd.DataFrame, metric: str, output_column: str) -> pd.DataFrame:
    usable = df.dropna(subset=[metric]).copy()
    if usable.empty:
        return pd.DataFrame(columns=["year", "month", output_column, "count", "std_dev"])
    usable["year"] = usable["date"].dt.year
    usable["month"] = usable["date"].dt.month
    grouped = usable.groupby(["year", "month"])[metric]
    export = grouped.agg(["mean", "count", "std"]).reset_index()
    export.columns = ["year", "month", output_column, "count", "std_dev"]
    export["std_dev"] = export["std_dev"].fillna(0.0)
    return export


def plot_monthly_line(export: pd.DataFrame, value_col: str, title: str, ylabel: str, output_path: Path, *, band: bool = False) -> None:
    plt.figure(figsize=(14, 8))
    if export.empty:
        plt.text(0.5, 0.5, "No data available", ha="center", va="center", fontsize=18)
        plt.axis("off")
    else:
        dates = pd.to_datetime(export["year"].astype(str) + "-" + export["month"].astype(str) + "-01")
        std_dev = pd.to_numeric(export.get("std_dev", 0), errors="coerce").fillna(0)
        values = pd.to_numeric(export[value_col], errors="coerce")
        if band:
            plt.fill_between(dates, values - std_dev, values + std_dev, alpha=0.25, color="#8ecae6", label="Monthly range")
            yerr = None
            capsize = 0
        else:
            yerr = std_dev
            capsize = 5
        plt.errorbar(dates, values, yerr=yerr, fmt="o-", linewidth=2, markersize=6, capsize=capsize, alpha=0.85, color="#2E86AB", ecolor="#8ecae6")
        plt.title(title, fontsize=16, fontweight="bold", pad=20)
        plt.xlabel("Month", fontsize=12, fontweight="bold")
        plt.ylabel(ylabel, fontsize=12, fontweight="bold")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        interval = 6 if len(export) > 36 else 3
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=interval))
        plt.xlim(dates.min() - pd.Timedelta(days=15), dates.max() + pd.Timedelta(days=15))
        plt.xticks(rotation=45, ha="right")
        plt.grid(True, alpha=0.3)
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def create_monthly_charts(df: pd.DataFrame, metadata: dict, image_dir: Path, data_dir: Path) -> None:
    end = metadata["quarter_end_date"]
    specs = [
        ("sleep_avg", "average_sleep_score", "Average Sleep Score per Month", "Average Sleep Score", "average_sleep_score_per_month"),
        ("rhr_min", "average_resting_hr", "Average Resting Heart Rate per Month", "Resting Heart Rate (BPM)", "average_resting_hr_per_month"),
        ("calories_active_avg", "average_active_calories", "Average Active Calories per Month", "Active Calories", "average_active_calories_per_month"),
    ]
    for metric, value_col, title, ylabel, stem in specs:
        export = month_export(df, metric, value_col)
        export.to_csv(data_dir / f"{stem}.csv", index=False)
        if export.empty:
            start = metadata["query_start_date"]
        else:
            start = f"{int(export.iloc[0]['year']):04d}-{int(export.iloc[0]['month']):02d}-01"
        plot_monthly_line(
            export,
            value_col,
            f"{title} ({start} to {end})",
            ylabel,
            image_dir / f"{stem}.png",
            band=(stem == "average_sleep_score_per_month"),
        )


def create_summary_chart(df: pd.DataFrame, metadata: dict, image_dir: Path, data_dir: Path) -> None:
    end = parse_day(metadata["quarter_end_date"])
    end_month = date(end.year, end.month, 1)
    start = (pd.Timestamp(end_month) - pd.DateOffset(months=11)).date()
    recent = df[(df["date"].dt.date >= start) & (df["date"].dt.date <= end)].copy()
    rows = []
    if not recent.empty:
        monthly = recent.groupby([recent["date"].dt.year, recent["date"].dt.month])
        for (year, month), group in monthly:
            rows.append(
                {
                    "year": year,
                    "month": month,
                    "rhr_avg": group["rhr_min"].mean(),
                    "stress_avg": group["stress_avg"].mean(),
                    "steps": group["steps"].mean(),
                    "bb_max": group["bb_max"].mean(),
                }
            )
    export = pd.DataFrame(rows, columns=["year", "month", "rhr_avg", "stress_avg", "steps", "bb_max"])
    export.to_csv(data_dir / "summary_quartet_per_month.csv", index=False)

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Health Metrics - Monthly Averages (Previous 12 Months)", fontsize=20, fontweight="bold")
    specs = [
        ("rhr_avg", "Resting Heart Rate (BPM)", "#2E86AB"),
        ("stress_avg", "Stress Level", "#A23B72"),
        ("steps", "Steps", "#F18F01"),
        ("bb_max", "Body Battery Max", "#C73E1D"),
    ]
    if export.empty:
        for ax in axes.flat:
            ax.text(0.5, 0.5, "No data available", ha="center", va="center")
            ax.axis("off")
    else:
        dates = pd.to_datetime(export["year"].astype(str) + "-" + export["month"].astype(str) + "-01")
        for ax, (col, name, color) in zip(axes.flat, specs):
            ax.bar(dates, export[col], color=color, alpha=0.7, width=20)
            ax.set_title(name, fontsize=12, fontweight="bold")
            ax.set_xlabel("Month", fontsize=10)
            ax.set_ylabel(name.split("(")[0].strip(), fontsize=10)
            if export[col].notna().sum() >= 2:
                x_values = np.arange(len(export))
                y_values = pd.to_numeric(export[col], errors="coerce")
                valid = y_values.notna()
                slope, intercept = np.polyfit(x_values[valid], y_values[valid], 1)
                ax.plot(dates, slope * x_values + intercept, color="black", linestyle="--", linewidth=1.5, alpha=0.7)
            for x_value, y_value in zip(dates, export[col]):
                if pd.notna(y_value):
                    label = f"{y_value:.0f}" if abs(y_value) >= 100 else f"{y_value:.1f}"
                    ax.text(x_value, y_value, label, ha="center", va="bottom", fontsize=8, rotation=90)
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
            tick_dates = dates.iloc[::2] if len(dates) > 8 else dates
            ax.set_xticks(tick_dates)
            ax.set_xlim(dates.min() - pd.Timedelta(days=15), dates.max() + pd.Timedelta(days=15))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")
            ax.grid(True, alpha=0.3)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
    plt.tight_layout(pad=3.0)
    plt.savefig(image_dir / "summary.png", dpi=300, bbox_inches="tight")
    plt.close()


def create_quarterly_metrics(df: pd.DataFrame, vo2_df: pd.DataFrame, metadata: dict, data_dir: Path) -> None:
    q_start = parse_day(metadata["quarter_start_date"])
    q_end = parse_day(metadata["quarter_end_date"])
    qdf = df[(df["date"].dt.date >= q_start) & (df["date"].dt.date <= q_end)]
    vdf = vo2_df[(vo2_df["date"].dt.date >= q_start) & (vo2_df["date"].dt.date <= q_end)] if not vo2_df.empty else vo2_df
    label = metadata.get("quarter_label") or quarter_label_for(q_start)
    if "intensity_minutes" in qdf and not qdf.empty:
        weekly_intensity = qdf.set_index("date")["intensity_minutes"].resample("W-SUN").sum().median()
    else:
        weekly_intensity = np.nan
    row = {
        "": label,
        "RHR": qdf["rhr_min"].median(),
        "Stress": qdf["stress_avg"].median(),
        "Steps": round(qdf["steps"].mean()) if not qdf["steps"].dropna().empty else np.nan,
        "Body Battery": qdf["bb_max"].median(),
        "Intensity": weekly_intensity,
        "VO2Max": vdf["vo2_max"].quantile(0.95) if not vdf.empty else np.nan,
    }
    pd.DataFrame([row]).to_csv(data_dir / "quarterly_metrics_raw.csv", index=False)


def create_weekly_intensity(df: pd.DataFrame, metadata: dict, image_dir: Path, data_dir: Path) -> None:
    start = parse_day(metadata["quarter_end_date"]) - timedelta(days=365)
    end = parse_day(metadata["quarter_end_date"])
    series_df = df[(df["date"].dt.date >= start) & (df["date"].dt.date <= end)].copy()
    if "intensity_minutes" not in series_df or series_df["intensity_minutes"].isna().all():
        series_df["intensity_minutes"] = series_df["moderate_activity_time"].fillna(0) + 2 * series_df["vigorous_activity_time"].fillna(0)
    series_df["week_start"] = series_df["date"].dt.date.map(lambda value: value - timedelta(days=value.weekday()))
    weekly = series_df.groupby("week_start")["intensity_minutes"].sum().sort_index()
    first_week = start - timedelta(days=start.weekday())
    full_index = pd.date_range(start=first_week, end=end, freq="W-MON").date
    weekly = weekly.reindex(full_index, fill_value=0)
    week_end = [min(value + timedelta(days=6), end) for value in weekly.index]
    export = pd.DataFrame({"week_start": weekly.index, "week_end": week_end, "intensity_minutes": weekly.values})
    export.to_csv(data_dir / "weekly_intensity_minutes_per_week.csv", index=False)

    plt.figure(figsize=(18, 6))
    labels = [value.isoformat() for value in export["week_end"]]
    plt.bar(range(len(export)), export["intensity_minutes"], width=0.8, color="#69b3a2", align="center")
    avg = weekly.mean() if len(weekly) else 0
    plt.axhline(y=800, color="r", linestyle="--", label="Weekly Target (800)")
    plt.axhline(y=avg, color="g", linestyle="--", label=f"Weekly Average ({avg:.0f})")
    plt.title(f"Weekly Intensity Minutes ({start} to {end})", fontsize=20, fontweight="bold", pad=20)
    plt.xlabel("Week End Date")
    plt.ylabel("Total Intensity Minutes")
    tick_step = max(1, len(labels) // 18)
    tick_positions = list(range(0, len(labels), tick_step))
    if labels and tick_positions[-1] != len(labels) - 1:
        tick_positions.append(len(labels) - 1)
    plt.xticks(tick_positions, [labels[idx] for idx in tick_positions], rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig(image_dir / "weekly_intensity_minutes.png", dpi=300, bbox_inches="tight")
    plt.close()


def create_correlation_matrix(df: pd.DataFrame, metadata: dict, image_dir: Path, data_dir: Path) -> None:
    q_start = parse_day(metadata["quarter_start_date"])
    q_end = parse_day(metadata["quarter_end_date"])
    qdf = df[(df["date"].dt.date >= q_start) & (df["date"].dt.date <= q_end)]
    metrics = [metric for metric in CORRELATION_METRICS if metric in qdf.columns and qdf[metric].notna().sum() >= 2]
    if not metrics:
        matrix = pd.DataFrame()
    else:
        matrix = qdf[metrics].corr()
    matrix.to_csv(data_dir / "correlation_matrix.csv")

    plt.figure(figsize=(15, 13))
    if matrix.empty:
        plt.text(0.5, 0.5, "Not enough data for correlation matrix", ha="center", va="center", fontsize=18)
        plt.axis("off")
    else:
        sns.heatmap(
            matrix,
            annot=True,
            cmap="RdYlBu_r",
            vmin=-1,
            vmax=1,
            center=0,
            square=True,
            fmt=".2f",
            linewidths=0.5,
            cbar_kws={"shrink": 0.8},
            annot_kws={"size": 8},
        )
        plt.xticks(rotation=45, ha="right", fontsize=11)
        plt.yticks(rotation=0, fontsize=11)
    plt.title(f"Garmin Health Metrics Correlation Matrix\n{metadata.get('quarter_label', '')} Analysis", fontsize=16, fontweight="bold", pad=20)
    plt.tight_layout()
    plt.savefig(image_dir / "correlation_matrix.png", dpi=300, bbox_inches="tight")
    plt.close()


def create_day_of_week_heatmaps(df: pd.DataFrame, metadata: dict, image_dir: Path, data_dir: Path) -> None:
    q_start = parse_day(metadata["quarter_start_date"])
    for metric, csv_name, image_name, title, cmap, first_col in [
        ("sleep_avg", "sleep_score_per_day_per_quarter.csv", "sleep_score_per_day.png", "Average Sleep Score per Day of Week", "YlOrRd", "Quarter"),
        ("stress_avg", "stress_quarterly_per_quarter.csv", "stress_level_per_day.png", "Average Stress Level per Day of Week", "viridis", "quarter"),
    ]:
        usable = df.dropna(subset=[metric])
        first_data_day = usable["date"].dt.date.min() if not usable.empty else q_start
        windows = quarter_windows(first_data_day, q_start)
        rows = []
        labels = []
        for label, start, end in windows:
            subset = df[(df["date"].dt.date >= start) & (df["date"].dt.date <= end)]
            values = []
            for day_idx in range(7):
                values.append(subset[subset["date"].dt.weekday == day_idx][metric].mean())
            values.append(subset[metric].mean())
            rows.append(values)
            labels.append(label)
        columns = DAY_NAMES + ["Avg"]
        export = pd.DataFrame(rows, columns=columns)
        export.insert(0, first_col, labels)
        export.to_csv(data_dir / csv_name, index=False)
        plot_df = export.set_index(first_col)
        plt.figure(figsize=(12, max(8.5, len(labels) * 0.45)))
        if metric == "sleep_avg":
            values = np.array([
                "#b30000",  # <= 60
                "#d7301f",  # 60-70
                "#fc8d59",  # 70-75
                "#fdbb84",  # 75-80
                "#a6d96a",  # 80-85
                "#7fc97f",  # 85-90
                "#4daf4a",  # 90-95
                "#1a9850",  # 95-100
            ])
            cmap = ListedColormap(values)
            bounds = [0, 60, 70, 75, 80, 85, 90, 95, 100]
            norm = BoundaryNorm(bounds, cmap.N)
            sns.heatmap(
                plot_df,
                annot=True,
                fmt=".1f",
                cmap=cmap,
                norm=norm,
                linewidths=0.5,
                square=True,
                mask=plot_df.isna(),
                cbar_kws={"label": "Average Sleep Score"},
            )
        else:
            sns.heatmap(plot_df, annot=True, fmt=".1f", cmap=cmap, linewidths=0.5, square=True, mask=plot_df.isna())
        plt.title(f"{title} ({labels[0]} to {labels[-1]})", fontsize=16, fontweight="bold", pad=20)
        plt.xlabel("Day of Week", fontsize=14)
        plt.ylabel("Quarter", fontsize=14)
        plt.xticks(rotation=0)
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig(image_dir / image_name, dpi=300, bbox_inches="tight")
        plt.close()


def create_stress_week_heatmap(df: pd.DataFrame, metadata: dict, image_dir: Path) -> None:
    end = parse_day(metadata["quarter_end_date"])
    end_of_last_complete_week = end - timedelta(days=(end.weekday() + 1) % 7)
    start = end_of_last_complete_week - timedelta(days=83)
    subset = df[(df["date"].dt.date >= start) & (df["date"].dt.date <= end_of_last_complete_week)]
    matrix = np.full((12, 7), np.nan)
    for _, row in subset.iterrows():
        day = row["date"].date()
        diff = (day - start).days
        if 0 <= diff < 84:
            matrix[diff // 7][day.weekday()] = row["stress_avg"]
    plt.figure(figsize=(12, 14))
    sns.heatmap(
        matrix,
        xticklabels=DAY_NAMES,
        yticklabels=[f"Week {i + 1}" for i in range(12)],
        annot=True,
        fmt=".1f",
        cmap="YlOrRd",
        linewidths=0.5,
        mask=np.isnan(matrix),
    )
    plt.title(f"Daily Stress Level per Week (Previous 12 Weeks)\n({start} to {end_of_last_complete_week})", fontsize=16, fontweight="bold", pad=20)
    plt.xlabel("Day of Week", fontsize=14)
    plt.ylabel("Week of Year", fontsize=14)
    plt.xticks(rotation=0)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(image_dir / "stress_level_per_week.png", dpi=300, bbox_inches="tight")
    plt.close()


def create_vo2(vo2_rows: list[dict], metadata: dict, image_dir: Path, data_dir: Path) -> pd.DataFrame:
    vo2_df = pd.DataFrame(vo2_rows)
    if vo2_df.empty:
        export = pd.DataFrame(columns=["year", "month", "vo2_max_95th"])
        export.to_csv(data_dir / "monthly_vo2_max_per_month.csv", index=False)
        return pd.DataFrame(columns=["date", "vo2_max"])
    vo2_df["date"] = pd.to_datetime(vo2_df["date"])
    direct = pd.to_numeric(vo2_df.get("vo2_max", pd.Series(index=vo2_df.index)), errors="coerce")
    generic = pd.to_numeric(vo2_df.get("vo2_max_generic", pd.Series(index=vo2_df.index)), errors="coerce")
    cycling = pd.to_numeric(vo2_df.get("vo2_max_cycling", pd.Series(index=vo2_df.index)), errors="coerce")
    vo2_df["vo2_max"] = direct.fillna(generic).fillna(cycling)
    start = parse_day(metadata["query_start_date"])
    end = parse_day(metadata["quarter_end_date"])
    vo2_df = vo2_df[(vo2_df["date"].dt.date >= start) & (vo2_df["date"].dt.date <= end)].dropna(subset=["vo2_max"])
    if vo2_df.empty:
        export = pd.DataFrame(columns=["year", "month", "vo2_max_95th"])
    else:
        monthly = vo2_df.set_index("date")["vo2_max"].resample("ME").quantile(0.95)
        export = monthly.reset_index()
        export["year"] = export["date"].dt.year
        export["month"] = export["date"].dt.month
        export = export.rename(columns={"vo2_max": "vo2_max_95th"})[["year", "month", "vo2_max_95th"]]
    export.to_csv(data_dir / "monthly_vo2_max_per_month.csv", index=False)
    plt.figure(figsize=(12, 6))
    if not export.empty:
        dates = pd.to_datetime(export["year"].astype(str) + "-" + export["month"].astype(str) + "-01")
        plt.plot(dates, export["vo2_max_95th"], marker="o", label="95th Percentile VO2 Max")
        plt.legend()
        data_start = dates.min()
        plt.xlim(data_start - pd.Timedelta(days=15), dates.max() + pd.Timedelta(days=15))
    else:
        plt.text(0.5, 0.5, "No VO2 Max data available", ha="center", va="center", fontsize=16)
    plt.title(f"Monthly 95th Percentile VO2 Max ({metadata['query_start_date']} to {metadata['quarter_end_date']})")
    plt.xlabel("Date")
    plt.ylabel("VO2 Max")
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.savefig(image_dir / "monthly_vo2_max.png", dpi=300, bbox_inches="tight")
    plt.close()
    return vo2_df[["date", "vo2_max"]]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", type=Path, required=True, help="LifeDB MCP export JSON")
    parser.add_argument("--post-dir", type=Path, required=True)
    args = parser.parse_args()

    sns.set_theme(style="whitegrid")
    payload = load_export(args.input_json)
    metadata = payload["metadata"]
    image_dir, data_dir = ensure_dirs(args.post_dir)
    df = to_daily_frame(payload["daily_metrics"])
    if df.empty:
        raise SystemExit("No daily metrics in MCP export.")
    if "intensity_minutes" not in df.columns or df["intensity_minutes"].isna().all():
        df["intensity_minutes"] = df["moderate_activity_time"].fillna(0) + 2 * df["vigorous_activity_time"].fillna(0)
    else:
        df["intensity_minutes"] = pd.to_numeric(df["intensity_minutes"], errors="coerce")

    vo2_df = create_vo2(payload["vo2_max"], metadata, image_dir, data_dir)
    create_monthly_charts(df, metadata, image_dir, data_dir)
    create_summary_chart(df, metadata, image_dir, data_dir)
    create_weekly_intensity(df, metadata, image_dir, data_dir)
    create_correlation_matrix(df, metadata, image_dir, data_dir)
    create_day_of_week_heatmaps(df, metadata, image_dir, data_dir)
    create_stress_week_heatmap(df, metadata, image_dir)
    create_quarterly_metrics(df, vo2_df, metadata, data_dir)
    print(args.post_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
