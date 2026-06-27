---
title: 2026 Q2 Health Review
date: 2026-06-30T00:00:00+10:00
draft: true
url: /2026/06/2026-q2-health-review.html
tags:
  - longevity
  - health
  - articles
---
### Reflection

Q2 2026 is still provisional because the Garmin sync is stale. The latest available daily sleep, stress, and body battery data runs through May 29, 2026, and the activity/steps tables are much thinner than expected. So this is a partial-quarter review rather than a finished one.

Even with that caveat, the available data points to a better recovery quarter than Q1. Stress moved down, body battery moved up, sleep stayed close to the same level, and resting heart rate was basically flat. Fitness is harder to judge because the activity export is incomplete, but VO2 max has at least reappeared with one May reading.

### Focus Areas

As usual, there are five areas that I wanted to focus on:

- *Improve fitness* by rebuilding training volume and getting back toward consistent weekly load.
- *Sleep better* by improving sleep hygiene and meal timing.
- *Reduce stress* by reinforcing daily recovery habits.
- *Improve biomarkers* by focusing on measurable lab outcomes.
- *Improve nutrition* by using food choices to support glucose, recovery, and biomarkers.

Overall quarter snapshot:
![Summary Chart](summary.png)

Data coverage note: the charts and CSVs have been regenerated for the Q2 window, with the overall snapshot boundary shown as July 1, 2026. LifeDB still only exposes daily Garmin data through May 29, 2026 for sleep, stress, and body battery, so June remains missing from the measured dataset.

Quarter-over-quarter highlights from the available Q2 data:

- Average stress fell from **28.8** in Q1 to **25.2** in Q2-to-date, based on 22,437 Q2 stress samples.
- Average max body battery rose from **76.6** in Q1 to **82.9** in Q2-to-date, based on 59 Q2 days.
- Average sleep score was essentially flat: **79.5** in Q1 vs **78.9** in Q2-to-date across 59 nights.
- Average resting heart rate was also flat: **54.2 bpm** in Q1 vs **54.3 bpm** in Q2-to-date.
- Step and intensity data are not complete enough to compare cleanly. The current LifeDB tables only expose five Q2 step days and four Q2 training-load days, which is not representative.

Correlations for the quarter:
![Correlation Matrix](correlation_matrix.png)

The current correlation chart should be treated as provisional because activity, steps, and intensity data are sparse in the synced dataset. The strongest activity-related correlations are mostly artifacts of only a few populated activity days. The more useful signal is still the stress/recovery relationship: higher-stress days generally line up with weaker body battery recovery.

Let us go through how the quarter looked by focus area.

#### Improve Fitness

##### Goals

- Average intensity minutes (Garmin) of 800 or above ❓
- Improve Vo2Max ⚠️
- Decrease RHR ⚠️

##### Analysis

I look at intensity minutes as a way to make sure I am getting enough fitness, regardless of whether I am running, at the gym, or kayaking.
![Weekly Intensity Minutes](weekly_intensity_minutes.png)

The current LifeDB activity export is still too incomplete to evaluate weekly intensity properly. The regenerated weekly intensity CSV has **13** Q2 weeks, but only one populated week: **9** intensity minutes in the week ending May 31. That makes the Q2 average **0.7** minutes/week and median **0**, which is really a sync/data-coverage result rather than a fair training assessment.

Resting heart rate is more complete:
![Average Resting HR Per Month](average_resting_hr_per_month.png)

Across 59 available Q2 nights, average resting heart rate was **54.3 bpm**, almost unchanged from **54.2 bpm** in Q1. That is not the decrease I wanted, but it also did not continue worsening.

VO2 max has one Q2 datapoint: **48.1** on May 7, 2026. That is enough to say the metric is back on the board, but not enough to call a trend yet.

![Monthly VO2 Max](monthly_vo2_max.png)

##### Experiments

TODO: Add qualitative notes on the Q2 training rebuild, especially whether the planned strength/running structure from Q1 actually happened.

#### Improve Sleep

##### Goals

- Keep average sleep score about 80 ⚠️

##### Analysis

Sleep stayed close to target but slightly below where I want it.
![Average Sleep Score Per Month](average_sleep_score_per_month.png)

For the available Q2 data:

- Nights with sleep-score data: **59** (April 1 through May 29)
- Average sleep score: **78.9**
- Average sleep duration: **7.38 hours**
- Q1 comparison: **79.5** average sleep score and **7.27 hours** average sleep duration

Day-of-week sleep pattern:
![Average Sleep Score Per Day of Week](sleep_score_per_day.png)

The strongest sleep-score days were Tuesday (**83.4**, 8 nights) and Saturday (**83.1**, 8 nights). The weakest were Wednesday (**75.8**, 9 nights) and Monday (**76.6**, 8 nights). That looks like the mid-week weakness from Q1 persisted, though the exact cause needs qualitative context.

##### Experiments

TODO: Add notes on meal timing, evening routine, travel, and whether dropping tart cherry/melatonin changed sleep quality in practice.

#### Decrease Stress

##### Goals

- Decrease stress ✅

##### Analysis

Stress is the clearest improvement in the available Q2 data.

![Average Stress per Day of Week](stress_level_per_day.png)

Average stress dropped from **28.8** in Q1 to **25.2** in Q2-to-date, based on **22,437** Q2 stress samples. That is a meaningful move in the right direction.

Weekly stress trend:
![Average Stress Level per Week](stress_level_per_week.png)

The highest-stress days were Thursday (**26.8**) and Wednesday (**26.0**). Monday was lowest (**22.5**), with Saturday also relatively low (**23.7**). So the mid-week stress pattern is still visible, but the whole baseline looks lower than Q1.

##### Experiments

TODO: Add qualitative notes on what changed during April and May: work load, travel, training, caffeine, meals, breathwork, or any deliberate recovery habit.

#### Improve Biomarkers

##### Goals

- Decrease IGF-1 ❓
- Keep MCV in range ✅
- Decrease fasting glucose ❌
- Keep RDW stable ⚠️
- Increase or maintain albumin ❓
- Maintain hsCRP ✅
- Follow up free testosterone / SHBG / FSH ⚠️

##### Analysis

The latest biomarker follow-up in the sheet is from April 22-23, 2026, which sits inside Q2.

| Biomarker | Prior | Latest | Trend | Status |
| --- | --- | --- | --- | --- |
| **IGF-1** | 35 nmol/L (2025-10-10) | Not retested in Apr 2026 | No update | Previously above range |
| **MCV** | 101 fL (2026-01-17) | 95 fL (2026-04-22) | Decreased | Back in range |
| **Glucose** | 5.1 mmol/L (2025-10-10) | 5.4 mmol/L (2026-04-22) | Increased | Borderline / worse |
| **RDW** | 12.5% (2026-01-17) | 12.8% (2026-04-22) | Increased slightly | In range |
| **Albumin** | 45 g/L (2026-01-17) | Not retested in Apr 2026 | No update | Previously in range |
| **hsCRP** | <4.0 mg/L (2026-01-17) | <0.2 mg/L (2026-04-22) | Improved / clearer low result | Excellent |
| **Free Testosterone** | 260 pmol/L (2025-03-28) | 183 pmol/L (2026-04-22) | Decreased | Below range |
| **SHBG** | 68 nmol/L (2025-03-28) | 57 nmol/L (2026-04-22) | Decreased | Still above range |
| **FSH** | 7.7 IU/L (2025-03-28) | 10 IU/L (2026-04-22) | Increased | Slightly above range |

Key interpretation:

- The clearest win is **MCV**, which moved from out of range back into range.
- **hsCRP** is excellent at **<0.2 mg/L**.
- **Glucose** is now the main metabolic marker to watch, sitting at the top edge of the reference threshold.
- **Free testosterone / SHBG / FSH** still need follow-up. SHBG improved but remains high; free testosterone is below range; FSH is slightly above range.
- **IGF-1** and **albumin** still need retesting because they were not included in the April follow-up.

PhenoAge also updated on April 23, 2026:

- Chronological age: **43.2**
- Phenotypic age: **32.34**
- Difference: **10.84 years younger**

That is a tiny improvement in phenotypic age from **32.41** on January 17, 2026, though the overall difference only widened because chronological age also moved forward.

##### Experiments

The improved MCV result still points in the right direction for the B12/folate work from previous quarters.

The glucose experiment was the main nutrition-linked biomarker experiment this quarter. The CGM made it much easier to see which meals were uneventful and which meals caused a large spike. The laksa example was the clearest warning shot: the spike was obvious, and even walking afterward did not fully blunt it.

#### Improve Nutrition

##### Goals

- Improve glucose control.
- Keep meal prep consistent enough that eating out does not become the default.
- Use nutrition changes to support sleep, stress, and biomarker follow-up.

##### Analysis

The April glucose value of **5.4 mmol/L** makes glucose the obvious nutrition focus. It is not catastrophic, but it moved in the wrong direction and sits right at the top of the listed range.

The CGM experiment made this less abstract. Some regular meals looked fine, including toast with peanut butter and fig jam, the Nutty Pudding-inspired smoothie, and pasta with vegetables. The standout exception was laksa, which caused a large glucose spike.

##### Experiments

The main experiment that I ran this quarter was around fasting glucose. While not terrible, I wanted to try and drive this number down. I decided to re-visit getting a CGM and see which foods spike my levels. The first day was relatively uneventful: toast with peanut butter and fig jam was fine, as was my "Nutty Pudding"-inspired smoothie, same with some pasta and vegetables. On day two though I decided to try a new laksa place, which isn't a type of food I even typically eat that often, and stood back as I could see my fasting glucose levels soar. When I saw them raise I immediately went on a walk, but even that didn't help.

![](Pasted%20image%2020260502111803.png)

### Supplement Stack

Some principles that I tried to follow:

- Avoid pill burden; prefer food over pills.
- Wait until a supplement is on the ITP supported interventions page, or has significant evidence behind it.
- Have a biomarker in mind that a certain supplement will change.

Current stack:

| Morning | Evening | Ad Hoc |
| --- | --- | --- |
| Vitamin D (5000 IU) | Glycine (10g) | Iron (20mg) |
| Vitamin K2 mk7 (100mcg) | NAC (1g) | Vitamin C (500mg) |
| B-complex / methylated B vitamins | Magnesium | B5 P-5-P (50mg) |
| Zinc (15mg) |  |  |
| Hyaluronic Acid (200mg) |  |  |
| Iodine (150mcg) |  |  |
| Creatine (5g - in smoothie) |  |  |
| TMG (1.5g - in smoothie) |  |  |
| Boron (1mg - in smoothie) |  |  |
| Taurine (3g - in smoothie) |  |  |
| Fish Oil (6g) |  |  |

##### Experiments

- The B-vitamin simplification is the supplement change most tied to a measurable result, because MCV stayed back in range.
- Fish oil remains in the stack for now because sardines were not frequent enough to make food-only omega-3 intake reliable.
- TODO: Confirm whether astaxanthin, tart cherry, and melatonin were fully dropped during Q2 and whether any sleep change was noticeable.

### Focus For Next Quarter

Based on the partial Q2 data, key priorities for Q3 2026 are:

##### General

- Fix the Garmin / LifeDB sync so Q2 can be finalized with complete June data.
- Keep pressure on the mid-week recovery pattern, especially Wednesday and Thursday.
- Bring average sleep score back above 80 consistently.

##### Exercise

- Rebuild weekly training volume toward the 800-minute target.
- Get a complete activity/intensity export working so training can be evaluated properly.
- Use the May VO2 max datapoint as a baseline and look for enough qualifying activities to judge the trend.

##### Biomarkers

- Re-test IGF-1 and albumin.
- Confirm that MCV stays in range.
- Follow up glucose with either fasting glucose, HbA1c, fasting insulin, or a structured CGM review.
- Follow up free testosterone, SHBG, and FSH.

##### Nutrition

- Keep using CGM feedback to identify meals that produce outsized spikes.
- Treat high-spike restaurant meals as experiments rather than defaults.
- Keep meal prep boring enough to be reliable.

Wish me luck!
