---
title: 2025 Q3 Health Review
date: 2025-09-01T21:30:00.002+11:00
draft: true
url: /2025/10/2025-q3-health-review.html
tags:
  - longevity
  - health
  - articles
---
  

### Reflection

Add a reflection here.
### Focus Areas

As usual, there are four areas that I wanted to focus on:

- *Improve fitness* by training more. My goal is to get above a 75 fitness score on intervals.icu
- *Sleep better* by improving my sleep hygiene and experimenting with meal timing.
- *Reduce Stress* by examining meal composition and avoiding anything that might impact my sleep
- *Improve Biomarkers* by looking at my nutrition, as well as the above items.

Overall most metrics are improving, as we can see with the following key metrics.

  ![Summary Chart](summary.png)

Over the previous year we can see that:

* Resting Heart Rate is **decreasing** ✅
* Stress is **decreasing** ✅
* Steps are **maintaining** ✅
* Body Battery (max/day) is increasing ✅

We can see correlations for the quarter with the below correlation matrix.
  ![Correlation Matrix](correlation_matrix.png)

Looking at the correlations, here's an analysis of the relationships and whether they make intuitive sense:
##### Activity-Related Correlations (Very Strong)
* Calories Active & Vigorous Activity (0.949): ✅ Makes perfect sense - vigorous activity is the primary driver of active calorie burn
* Steps & Vigorous Activity (0.939): ✅ Logical - more steps often mean more intense activity
* Calories Active & Steps (0.937): ✅ Expected - walking/running are major calorie-burning activities
* Moderate activity shows surprisingly weak correlations across the board
* Stress has stronger correlations with recovery metrics (Body Battery) than with activity metrics, which suggests psychological stress might impact recovery more than physical activity does
##### Recovery Metrics
* Stress vs Body Battery Min (-0.701): ✅ Very intuitive - higher stress depletes body battery more
* Body Battery Max vs Min (0.682): ✅ Natural correlation - good recovery leads to both higher max and min levels
* RHR Min vs Body Battery Max (-0.679): ✅ Makes sense - lower resting heart rate indicates better recovery potential
##### Sleep and Recovery
* Sleep Average vs Body Battery Max (0.673): ✅ Strongly intuitive - better sleep leads to better recovery
* Sleep Average vs Stress (-0.433): ✅ Expected - better sleep typically reduces stress levels (or lower stress means better sleep)
* Sleep average has relatively weak correlations with activity metrics, which might suggest daily activity doesn't impact sleep as much as commonly thought
##### Physical Activity Metrics
* Floors vs Steps (0.685): ✅ Logical - climbing floors naturally involves steps
* HR Max vs Calories Active (0.679): ✅ Expected - more intense activity raises heart rate and burns calories 
##### Weight Correlations
* The correlations with weight are generally weaker, which makes sense as weight is a longer-term metric that doesn't change significantly day-to-day

Let’s go through how I did this quarter and what I experimented with.
#### Improve Fitness

##### Goals  

- Average intensity minutes (Garmin) of 800 or above ✅
- Improve Vo2Max ✅
- Decrease RHR ✅
##### Analysis

I look at intensity minutes as a way to make sure I'm getting enough fitness, regardless if I'm running or at the gym or kayaking. My goal is 800 minutes per week 80% of the weeks, which is significantly higher than the commonly recommended 150 minutes per week. The reason I've chosen to say "80% of the weeks" is because there are some weeks when I need to travel for work, and it is harder to reach this target.

For example, on one of my trips to China I only managed 348 minutes. Part of this was due to accidentally leaving my running it in my check-in bag, but there was no way I was going to hit 800 minutes: I was working 12 - 16 hour days every day, and it was 40C outside, so could only run on a treadmill.
  ![Weekly Intensity Minutes](weekly_intensity_minutes.png)

I hit my intensity target {INSERT PERCENTAGE} of the weeks this year.

In addition to load we can have a look at Resting Heart Rate, as that is often related to sufficient recovery.
  ![Average Resting HR Per Month](average_resting_hr_per_month.png)
##### Experiments

Towards the end of August I decided to make one big change to my fitness routine: trying to get both my run and strength training session completed before work. There are two reasons for this: 

* Firstly, I sometimes run out of time to go to the gym at lunch, or I have to cut workouts short.
* Secondly, to group all my exercise together. If doing a significant amount of exercise this could be a problem, but a 60min run and 30min strength session isn't really that much. What I am about to say is my opinion only, and I haven't read any research to substantiate. Here goes... due to my splitting of running and strength training, I'm activating mTOR twice per day, and sometimes consuming extra protein at lunch for the gym session. Additionally, when going to lunch, my Garmin highlights a significant amount of stress, which is why I avoid going to the gym at night (plus it being logistically challenging).  
 
My experiment was to wake up, have a protein shake supplemented with EAA, and go run straight away, and when returning home doing a strength session immediately afterwards. Then I'll have an extra large Nutty Pudding + LF yogurt + granola with my morning supplements, then shower. If I can turn this in to a long term habit I should be able to save some time each day, as it will cut down on the extra shower at lunch.

#### Improve Sleep
##### Goals
- Improve sleep quality ✅
##### Analysis

Let's have a look at my sleep scores since buying my Garmin:

  ![Average Sleep Score Per Month](average_sleep_score_per_month.png)


And then when comparing each quarter this year we can see some trends with each day of the week. Although this quarter has seen an improvement, it looks like something happens midweek that knocks me off my sleep game.


![Average Sleep Score Per Month](sleep_score_per_day.png)

My trip to China was also challenging for my sleep, even though I managed to avoid an overnight flight. My hotel room the first night was too close to the elevators and kept me up - until I requested to change rooms at 11PM - but even then I never really got back to sleep.

However, it really validated some hunches I was having: eating a heavy carb meal seems to disrupt my sleep. I can see this even on my Garmin, where my stress levels spike after certain meals, but not after others. I ordered a small bowl of noodles around 4:30PM when I arrived, and while glorious, my stress levels were elevated for hours. I even did a little walk afterwards to try and stabilise my blood sugar and insulin levels. 
##### Experiments

I conducted a few experiments this quarter, including:

- Nutrition: adjusting my final meal of the day to be a bit earlier (~4pm) and then also reducing the amount of lentils in it, increasing broccoli, and eliminating the raisin toppings. I also adjusted the seeds I topped it with to try and hit my Omega 3 : 6 ratio better.
- Hygiene: I continued to use my blue light blocking snap-on glasses every evening
- Morning light: I continued to use my DIY SAD light whenever possible.
- Caffeine: I continued to consume almost none, except for a tsp of matcha in my morning smoothie.
- Supplements: I'll continue with Tart Cherry for now, but I'm not certain on its efficacy.

Overall I'd consider these experiments a success.
#### Decrease Stress

##### Goals
- Decrease stress ❌
##### Analysis
Let's have a look at stress per quarter grouped by day of the week:

![Average Stress per DoW per QTR](stress_level_per_day.png)

We can see an overall decrease in stress, and the lowest for the year. My stress levels on Tuesdays have decreased on average, but I think that is more likely because I slowed down going to the gym due to injury. Monday is the least stressful day of the week; my guess here is because that is when I tend to have a rest day.

  
![Average Stress Level Per Week QTR](stress_level_per_week.png)

Week 31 appears to have been fairly stressful, and coincidentally I started feeling like I was fighting something the week after. At the end of Week 32 I travelled to China, and then was there for all of Week 33. The days were quite long, and I had less control over my nutrition than I normally would.
##### Experiments
No stress-related experiments for the quarter.
#### Improve Biomarkers

##### Goals
- Decrease IGF-1 ❌
- Decrease MCV ✅
- Decrease RDW ✅
- Increase Albumin ✅
- Decrease hsCRP ✅
##### Analysis

[INSERT CHART FROM PHENOAGE]:

We can see that...
##### Experiments

I did have a fair amount of experimentation here, including:

- **MCV & RDW**: After my biomarkers showed that I remain low on B12, Iron, and Vitamin D, I opted to focus on getting those in to better ranges. I swapped out the B Complete with a B12 (methylcobalamin) and L-Methylfolate combination, which I hope will increase absorption. I have also started to take a sublingual B12 every morning. There's also a need to optimise my iron balance by increasing my ferritin levels from 41 µg/L to somewhere between 60-80 µg/L; I've increased my frequency of taking a 20mg iron supplement.
- I've added in iodine (via kelp) now, too, given I'm essentially on a vegan diet and don't eat much salt.
- Updated my daily smoothie to have a carrot to try and increase my beta-carotene (vitamin A) intake without supplementing.
- Increased Vitamin D from 1,000 IU to 4,000 IU because my vitamin D levels have been deficient all year.
- Started eating sardines. Ideally I would like to drop or reduce the fish oil, as this has shown no impact on health or life span via the ITP.
- Started eating watermelon for the lycopene.
- Albumin: Potentially related to the FMD, or perhaps I just need more protein due to higher levels of training. I have contemplated cutting down on my protein consumption to lower IGF-1, but I think I'll keep the pea protein in my daily smoothie.

Because of subscribing to Cronometer I'm able to get more reports, such as my Nutrient Balances and Nutrient Targets, which have encouraged me to tweak the food I eat.

For example, here are my Nutrient Targets (without supplementation):

[NUTRIENT TARGETS CHART]:

And here are my Balances (with supplementation):

[NUTRIENT BALANCES CHART]:
### Supplement Stack

Some principles that I tried to follow:

- Avoid bill burden; prefer food over pills.
- Wait until a supplement is on the ITP supported interventions page
- Have a biomarker in mind that a certain supplement will change

And here's what is currently in my stack:

| Morning                     | Evening           | Ad Hoc            |
| --------------------------- | ----------------- | ----------------- |
| Fish Oil (6g)               | Astaxanthin (7mg) | Iron (20mg)       |
| Niacin (50mg)               | Glycine (5g)      | Vitamin C (500mg) |
| Calcium (333mg)             | NAC (1g)          |                   |
| Vitamin D (4000 IU)         |                   |                   |
| Vitamin K2 mk7 (100mcg)     |                   |                   |
| B12 Methyl (1000 mcg)       |                   |                   |
| B12 (Liposomal, 1000 mcg)   |                   |                   |
| L-Methylfolate  (1000 mcg)  |                   |                   |
| Lysine (1g)                 |                   |                   |
| Zinc (5mg)                  |                   |                   |
| Hyaluronic Acid (200mg)     |                   |                   |
| Iodine (150mcg)             |                   |                   |
| Creatine (3g - in smoothie) |                   |                   |
| TMG (2g - in smoothie)      |                   |                   |

Here are the changes that I made this quarter:

* Increased **TMG** from 500mg to 2g to try and better support methylation and decrease homocysteine.
* Removed **HCP** in order to try and decrease IGF-1.
* Added a **liposomal form of B12**, just in case I have absorption issues. 
* Moved **iron** from being ad hoc to every evening, and taken alongside **vitamin C**.
* Removed **magnesium glycinate** from evening stack, as getting enough from diet.

If we're going to discuss supplements, then we should probably also discuss nutrition!
### Focus For Next Quarter

I think the next quarter will remain similar to this one. I've subscribed to Cronometer, so I'm getting some additional insight from that. I'm contemplating dropping the following supplements, as it appears as though I am getting enough from food:

* Calcium - remove
* Fish oil - move to evening pills
* Lysine - remove
* Zinc - remove
* Iron - remove

