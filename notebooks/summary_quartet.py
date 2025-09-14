#!/usr/bin/env python3
"""
Create a quartet map showing monthly averages for the previous 12 months for:
- Resting Heart Rate (rhr)
- Stress (stress_avg) 
- Steps (steps)
- Body Battery (bb_max)

Each subplot is a bar chart with different colors and polynomial trendlines.
"""

import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import pandas as pd
import seaborn as sns
import os
from datetime import datetime, timedelta
from collections import defaultdict
# Using numpy polyfit instead of scipy

from garmindb import GarminConnectConfigManager
from garmindb.garmindb import GarminSummaryDb, DaysSummary, MonitoringDb, MonitoringHeartRate, Sleep, GarminDb
from garmindb.summarydb import DaysSummary, SummaryDb

# Set up seaborn theme
sns.set_theme(style="whitegrid")

def create_quartet_map():
    """Create a quartet map with 4 subplots for health metrics."""
    
    # Create images directory if it doesn't exist
    os.makedirs('images', exist_ok=True)
    
    # Calculate date range for previous 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # 12 months back
    
    print(f"Creating quartet map for data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Initialize database connection
    gc_config = GarminConnectConfigManager()
    db_params_dict = gc_config.get_db_params()
    garmin_db = GarminDb(db_params_dict)
    sum_db = SummaryDb(db_params_dict, False)
    
    # Query daily summary data for the period
    start_ts = datetime.combine(start_date.date(), datetime.min.time())
    end_ts = datetime.combine(end_date.date(), datetime.max.time())
    
    data_period = DaysSummary.get_for_period(sum_db, start_ts, end_ts, DaysSummary)
    print(f"Found {len(data_period)} days of data for the period")
    
    # Group data by month
    monthly_data = defaultdict(lambda: defaultdict(list))
    
    for entry in data_period:
        month_key = entry.day.strftime('%Y-%m')
        
        # Collect RHR data
        if entry.rhr_avg is not None:
            monthly_data[month_key]['rhr'].append(entry.rhr_avg)
        
        # Collect stress data
        if entry.stress_avg is not None:
            monthly_data[month_key]['stress'].append(entry.stress_avg)
        
        # Collect steps data
        if entry.steps is not None:
            monthly_data[month_key]['steps'].append(entry.steps)
        
        # Collect body battery data (assuming it's available in DaysSummary)
        if hasattr(entry, 'bb_max') and entry.bb_max is not None:
            monthly_data[month_key]['bb_max'].append(entry.bb_max)
    
    # Sort months chronologically
    sorted_months = sorted(monthly_data.keys())
    
    # Calculate monthly averages
    metrics_data = {
        'rhr': [],
        'stress': [],
        'steps': [],
        'bb_max': []
    }
    
    month_labels = []
    
    for month in sorted_months:
        month_labels.append(month)
        
        for metric in metrics_data.keys():
            if monthly_data[month][metric]:
                avg_value = np.mean(monthly_data[month][metric])
                metrics_data[metric].append(avg_value)
            else:
                metrics_data[metric].append(np.nan)
    
    # Convert month labels to datetime for proper x-axis formatting
    month_dates = [datetime.strptime(month, '%Y-%m') for month in month_labels]
    
    # Create the quartet map
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Health Metrics - Monthly Averages (Previous 12 Months)', 
                 fontsize=20, fontweight='bold')
    
    # Define colors for each subplot
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
    metric_names = ['Resting Heart Rate (BPM)', 'Stress Level', 'Steps', 'Body Battery Max']
    metric_keys = ['rhr', 'stress', 'steps', 'bb_max']
    
    # Create each subplot
    for i, (ax, color, name, key) in enumerate(zip(axes.flat, colors, metric_names, metric_keys)):
        # Get data for this metric
        data = metrics_data[key]
        
        # Create bar chart
        bars = ax.bar(month_dates, data, color=color, alpha=0.7, width=20)
        
        # Add polynomial trendline
        if len(data) > 2 and not all(np.isnan(data)):
            # Remove NaN values for trendline calculation
            valid_indices = ~np.isnan(data)
            valid_count = np.sum(valid_indices)
            
            if valid_count > 2:
                x_numeric = np.arange(len(data))[valid_indices]
                y_valid = np.array(data)[valid_indices]
                
                try:
                    # Fit polynomial (degree 1 for linear trend, or 3 if enough points)
                    degree = min(3, valid_count - 1) if valid_count > 3 else 1
                    poly_coeffs = np.polyfit(x_numeric, y_valid, degree)
                    poly_func = np.poly1d(poly_coeffs)
                    
                    # Generate trendline points
                    x_trend = np.linspace(0, len(data)-1, 100)
                    y_trend = poly_func(x_trend)
                    
                    # Convert back to dates for plotting - use actual month dates
                    x_trend_dates = []
                    for x in x_trend:
                        # Interpolate between actual month dates
                        if x <= 0:
                            x_trend_dates.append(month_dates[0])
                        elif x >= len(month_dates) - 1:
                            x_trend_dates.append(month_dates[-1])
                        else:
                            # Linear interpolation between month dates
                            idx = int(x)
                            frac = x - idx
                            if idx < len(month_dates) - 1:
                                date1 = month_dates[idx]
                                date2 = month_dates[idx + 1]
                                # Calculate days between dates
                                days_diff = (date2 - date1).days
                                interpolated_date = date1 + timedelta(days=int(frac * days_diff))
                                x_trend_dates.append(interpolated_date)
                            else:
                                x_trend_dates.append(month_dates[idx])
                    
                    # Plot trendline with distinct style
                    ax.plot(x_trend_dates, y_trend, color='black', linewidth=3, alpha=0.9, 
                           linestyle='--', label='Trend Line')
                except np.linalg.LinAlgError:
                    # Fallback to simple linear trend if polynomial fails
                    if valid_count > 1:
                        slope, intercept = np.polyfit(x_numeric, y_valid, 1)
                        x_trend = np.linspace(0, len(data)-1, 100)
                        y_trend = slope * x_trend + intercept
                        
                        # Convert back to dates for plotting - use actual month dates
                        x_trend_dates = []
                        for x in x_trend:
                            # Interpolate between actual month dates
                            if x <= 0:
                                x_trend_dates.append(month_dates[0])
                            elif x >= len(month_dates) - 1:
                                x_trend_dates.append(month_dates[-1])
                            else:
                                # Linear interpolation between month dates
                                idx = int(x)
                                frac = x - idx
                                if idx < len(month_dates) - 1:
                                    date1 = month_dates[idx]
                                    date2 = month_dates[idx + 1]
                                    # Calculate days between dates
                                    days_diff = (date2 - date1).days
                                    interpolated_date = date1 + timedelta(days=int(frac * days_diff))
                                    x_trend_dates.append(interpolated_date)
                                else:
                                    x_trend_dates.append(month_dates[idx])
                        
                        ax.plot(x_trend_dates, y_trend, color='black', linewidth=3, alpha=0.9, 
                               linestyle='--', label='Trend Line')
        
        # Customize subplot
        ax.set_title(name, fontsize=12, fontweight='bold')
        ax.set_xlabel('Month', fontsize=10)
        ax.set_ylabel(name.split('(')[0].strip(), fontsize=10)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(interval=2))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Adjust x-axis label position
        ax.tick_params(axis='x', labelsize=8)
        
        # Add grid
        ax.grid(True, alpha=0.3)
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Add legend for trendline
        ax.legend(loc='upper right', fontsize=8)
        
        # Add value labels on bars
        for bar, value in zip(bars, data):
            if not np.isnan(value):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                       f'{value:.0f}', ha='center', va='bottom', fontsize=8)
    
    # Adjust layout with more padding
    plt.tight_layout(pad=3.0)
    
    # Additional adjustment for subplot spacing
    plt.subplots_adjust(hspace=0.4, wspace=0.3)
    
    # Save the plot
    plt.savefig('images/summary.png', dpi=300, bbox_inches='tight')
    print("Quartet map saved as 'images/summary.png'")

    
    # Print summary statistics
    print(f"\nSummary Statistics:")
    print(f"Total months with data: {len(month_labels)}")
    
    for metric, data in metrics_data.items():
        valid_data = [d for d in data if not np.isnan(d)]
        if valid_data:
            print(f"{metric.upper()}: {len(valid_data)} months, avg={np.mean(valid_data):.1f}, std={np.std(valid_data):.1f}")
        else:
            print(f"{metric.upper()}: No data available")

if __name__ == "__main__":
    create_quartet_map()
