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
- Decrease MCV ❓
- Decrease RDW ❓
- Increase Albumin ❓
- Decrease hsCRP ❓

##### Analysis

No blood biomarker data was included in the generated files for this quarter. Add updated panel results and interpretation when available.

##### Experiments

No biomarker-linked experiment notes were captured in this dataset.

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
- Re-run nutrition and biomarker workflows so those sections can be quantified.
