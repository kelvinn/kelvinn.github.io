---
title: 2026 Q1 Health Review
date: 2026-03-31T21:30:00.002+11:00
draft: true
url: /2026/03/2026-q1-health-review.html
tags:
  - longevity
  - health
  - articles
---
### Reflection

Q1 2026 was a rebuilding quarter from a training and recovery perspective. The data shows reduced training load, lower daily steps, higher stress, and lower body battery relative to late 2025.

### Focus Areas

As usual, there are four areas that I wanted to focus on:

- *Improve fitness* by training more. My goal is to maintain 800 intensity minutes on average per week.
- *Sleep better* by improving my sleep hygiene and experimenting with meal timing.
- *Reduce stress* by examining meal composition and avoiding anything that might impact my sleep.
- *Improve biomarkers* by looking at my nutrition, as well as the above items.

Overall most metrics moved in the wrong direction this quarter, as we can see with the following key metrics.
  ![Summary Chart](summary.png)

Over the previous quarter (Q4 2025 to Q1 2026):

- Resting heart rate rose from 51 to 54 (+3 bpm).
- Stress rose from 25 to 29 (+16%).
- Average daily steps dropped from 11,289 to 6,420 (-43%).
- Body battery dropped from 89 to 78 (-12%).
- Weekly intensity (median) dropped from 583 to 205 (-65%).

We can see correlations for the quarter with the below correlation matrix.
  ![Correlation Matrix](correlation_matrix.png)

Looking at the correlations, a few stood out:

- `bb_min` and `stress_avg` were strongly negatively correlated (-0.83), which aligns with higher stress days draining recovery.
- Activity and output metrics stayed tightly linked (`steps` with `calories_active_avg`: 0.82; `hr_max` with `calories_active_avg`: 0.80).
- `hr_min` and `rhr_min` remained strongly coupled (0.73), which is expected.

Let us go through how the quarter looked by focus area.

#### Improve Fitness

##### Goals

- Average intensity minutes (Garmin) of 800 or above ❌
- Improve Vo2Max ⚪ (no data)
- Decrease RHR ❌

##### Analysis

I look at intensity minutes as a way to make sure I am getting enough fitness, regardless of whether I am running, at the gym, or kayaking.
  ![Weekly Intensity Minutes](weekly_intensity_minutes.png)

For Q1 2026:

- Average weekly intensity minutes: **258**
- Median weekly intensity minutes: **209**
- Weeks >= 800 minutes: **0 of 13**

In addition to load, resting heart rate is useful for interpreting adaptation and recovery.
  ![Average Resting HR Per Month](average_resting_hr_per_month.png)

Q1 2026 monthly average RHR sat around **54.2 bpm**, up from Q4 2025 levels.

VO2 max could not be evaluated this quarter from the generated data (`monthly_vo2_max_per_month.csv` was empty), likely due to no qualifying running activities in the configured period.

##### Experiments

No fitness experiment notes were recorded in this dataset for Q1. Add qualitative notes here if needed.

#### Improve Sleep

##### Goals

- Keep average sleep score about 80 ⚠️

##### Analysis

Sleep held close to target but was slightly down from Q4.
  ![Average Sleep Score Per Month](average_sleep_score_per_month.png)

Q1 2026 average sleep score was **79.5** (vs **80.6** in Q4 2025).

Day-of-week pattern for Q1:

![Average Sleep Score Per Day of Week](sleep_score_per_day.png)

- Best: Sunday (**83.1**) and Friday (**82.5**)
- Weakest: Wednesday (**76.1**) and Thursday (**78.1**)

##### Experiments

No sleep-specific experiment notes were captured in the generated data. Add qualitative notes here if needed.

#### Decrease Stress

##### Goals

- Decrease stress ❌

##### Analysis

Stress increased this quarter.

![Average Stress per Day of Week](stress_level_per_day.png)

Quarter average stress was **30.2**. Highest days were Thursday (**33.2**) and Wednesday (**31.8**), while Sunday was lowest (**27.1**).

![Average Stress Level per Week](stress_level_per_week.png)

The 12-week heatmap shows consistently elevated stress through the quarter rather than a short isolated spike.

##### Experiments

No stress-specific interventions were logged in this dataset for Q1.

#### Improve Nutrition

##### Goals

- Stick below 20g of saturated fat per day ❓
- Get between 110 and 125g of protein per day ❓
- Get over 70g of fibre per day ❓
- Meet 100% coverage of micronutrients ❓

Nutrition exports were not part of the generated `2026-q1-health-review/data` outputs in this run, so this section needs manual update or a nutrition pipeline run.

#### Improve Biomarkers

##### Goals

- Decrease IGF-1 ❓
- Decrease MCV ✅
- Decrease RDW ⚠️
- Increase Albumin ❓
- Decrease hsCRP ✅

##### Analysis

The latest biomarker follow-up happened after quarter-end, so the April 22-23, 2026 results are compared against the most recent prior available result for each marker.

| Biomarker | Prior | Latest | Trend | Status |
|-----------|-------|--------|-------|--------|
| **IGF-1** | 35 nmol/L (2025-10-10) | Not retested in Apr 2026 | No update | Previously above range |
| **MCV** | 101 fL (2026-01-17) | 95 fL (2026-04-22) | Decreased | Back in range |
| **RDW** | 12.5% (2026-01-17) | 12.8% (2026-04-22) | Increased slightly | Still in range |
| **Albumin** | 45 g/L (2026-01-17) | Not retested in Apr 2026 | No update | Previously in range |
| **hsCRP** | 0.2 mg/L (2025-10-10) | <0.2 mg/L (2026-04-22) | Stable to slightly improved | Excellent / in range |

- **MCV** was the clearest win, dropping from 101 fL on January 17, 2026 to 95 fL on April 22, 2026 and returning to the normal range.
- **hsCRP** remained very low, improving slightly from 0.2 mg/L on October 10, 2025 to <0.2 mg/L on April 22, 2026.
- **RDW** moved slightly in the wrong direction from 12.5% to 12.8%, but it still sits comfortably within range.
- **IGF-1** still needs retesting, since the latest result on file remains the elevated 35 nmol/L result from October 10, 2025.
- **Albumin** cannot be reassessed yet because it was not rerun in the April 2026 follow-up.

Additional April follow-up items also stood out:

- Free testosterone fell from 260 pmol/L on March 28, 2025 to 183 pmol/L on April 23, 2026 and is now below range.
- SHBG improved from 68 nmol/L on March 28, 2025 to 57 nmol/L on April 23, 2026, but it remains above range.
- FSH increased from 7.7 IU/L on March 28, 2025 to 10 IU/L on April 23, 2026, putting it slightly above range.
- Total testosterone fell from 20.5 nmol/L on March 28, 2025 to 13.1 nmol/L on April 23, 2026, though it remains in range.

##### Experiments

The CSV captures lab results rather than a structured intervention log, so there is less context here on what changed between draws. What the follow-up does show is that the earlier MCV issue improved materially, while the April hormone panel created a new area to keep an eye on in the next cycle.

### Supplement Stack

Some principles that I tried to follow:

- Avoid pill burden; prefer food over pills.
- Wait until a supplement is on the ITP supported interventions page, or has significant evidence behind it.
- Have a biomarker in mind that a certain supplement will change.

Quarter-specific supplement changes were not available in these generated files. Add the Q1 2026 stack update manually.

### Focus For Next Quarter

Based on Q1 2026 data, key priorities for Q2 2026 are:

- Rebuild weekly training volume gradually toward the 800-minute target.
- Recover average daily steps back into 10k+ territory.
- Prioritize stress-reduction habits on mid-week days (especially Wed/Thu).
- Bring average sleep score back above 80 consistently.
- Re-test IGF-1 and Albumin, confirm that the MCV improvement holds, and follow up the Free Testosterone / SHBG / FSH pattern.
