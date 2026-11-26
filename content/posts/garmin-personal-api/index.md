---
title: "Product of the year: Garmin's Personal API"
date: 2026-11-26T09:00:00+11:00
draft: false
url: /2026/11/garmin-personal-api.html
tags:
  - quantified-self
  - running
  - articles
---

### What it is

Garmin finally has an official API for individuals. Not the undocumented Connect endpoints the community tools scrape, and not a partner-only programme — the [Personal API](https://developer.garmin.com/gc-developer-program/personal/personal-faq/) gives you documented REST access to your own data: daily summaries, sleep (with stages and scores), HRV, stress, body battery, weight, hydration, nutrition, activities, and full FIT file downloads. You create a key in Garmin Connect's web settings, and that's the whole sign-up.

The shape of it is simple. You POST your key to a token endpoint and get back a 24-hour JWT (as plain text, not JSON — first gotcha). Then you hit `personal.connectapi.garmin.com` with a Bearer token. No OAuth dance, no refresh tokens: fetch a fresh token per run and you're done.

Some things I learned the hard way, so you don't have to:

- **The stress endpoint caps at ~28 days.** A 30-day window returns an empty 400. Chunk requests at 7 days and everything is fine.
- **Weight comes back in grams.**
- **Hydration is already inside the daily summaries** — no separate call needed.
- **There is no VO2 max field.** This is the big one. The API exposes a rounded integer at best. The precise per-activity value lives in the FIT file: download the activity ZIP, parse the FIT message (`unknown_140`, field `unknown_7`, × 3.5 / 65536), and treat sub-10 values as noise from non-cardio activities. I recovered seven years of VO2 max history this way.
- Keep a `raw` JSON column next to your parsed columns. Every time Garmin's payload shape surprised me, I repaired the database from stored raw payloads without re-downloading anything.

### Getting started: one prompt

Create your key in Garmin Connect (web, not mobile), put it in an environment variable, then paste this into Claude Code and walk away:

```text
Build me a Python sync script for the Garmin Personal API.

Auth: POST https://personal.connectapi.garmin.com/personalapitoken-service/personal-api/personal-api-key/token
with header "Authorization: ApiKey <GARMIN_PERSONAL_API_KEY>". The response is the JWT
as PLAIN TEXT (starts with "eyJ", content-type text/plain) — do not json.loads it. Tokens last
24h; fetch a fresh one every run. Read the key from the
GARMIN_PERSONAL_API_KEY environment variable; never print it.

API base: https://personal.connectapi.garmin.com with "Authorization: Bearer <token>".
Pull these, in 30-day windows with a 1-second pause between calls:
- /usersummary-service/v2/dailysummaries (steps, calories, resting HR,
  intensity minutes, stress, body battery, hydration — nested under
  movement./calories./heartRate./stress./bodyBattery./hydration.)
- /sleep-service/sleep/dailySleepSummariesByDate (stages in seconds,
  score at sleepScores.overall.value)
- /hrv-service/hrv/daily/{from}/{to}
- /usersummary-service/stats/stress/daily/{from}/{to} — CAPS AT 28 DAYS,
  use 7-day chunks
- /weight-service/weight/all/{from}/{to} — values are GRAMS
- /wellness-service/wellness/bodyBattery/reports/daily
- /activitylist-service/activities/search/activities

Storage: SQLite database with one table per data type, an upsert keyed on
date, and a raw JSON column storing the full API payload for every row.
Support incremental sync (track last synced date) and a full backfill via
env var. Support a backfill window far enough to cover my entire history.

Daily summary 2019-01-01 to today. Print per-table row counts when done.
Handle HTTP 429/401 with backoff and a clear error message.
```

That gets you a working local database in one shot. The FIT/VO2 parsing is worth adding as a follow-up prompt once the base sync works.

### What it unlocked for me

The point of the API was never the dashboard. I have an agent that plans my training week, and the Personal API is its ground truth. The consideration list I actually use:

**Time and place**

- Preferred windows are 6:30–9:30am, or lunch for strength only
- Sessions end 30 minutes before any 9am meeting; invites include a 20-minute buffer
- The work calendar has a standing lunch hold — one item means I'm free, multiple items means I'm booked

**Training load and structure**

- No rest days — they wreck my sleep. Instead: easy days
- No recovery-pace runs on weekends; long runs are weekend-only
- Strength taxonomy with caps: core kettlebell work 2–3×/week, swings 1–2×/week, split squats every other week and never before a quality session, rings at most once a week and only at lunch
- Strength is 30 minutes unless it's the only session that day, then up to an hour
- Recovery pace must be explicitly slower than base pace, or everything drifts to the same speed
- Stay in the Optimal band of my Training Balance; watch the 10-day acute load, not just this week

**Environment**

- Air quality terrible → no runs, swap to an indoor session
- Air quality bad only at certain hours → shift the session within the windows
- 35°C or hotter → strength instead of a run
- Both personal and work calendars are checked before anything is booked

**For readers who want to go further**

The fun part is what the API makes possible beyond my list, and I'd love to hear what people add. Some hypotheticals worth building:

- **Track availability** — your local track's opening hours, club night bookings, school-term exclusions
- **Gym equipment contention** — rings and racks are busy at lunch; query real occupancy or just model your gym's patterns
- **Travel weeks** — hotel gym inventory, timezone shifts, conference calendars
- **Race calendar integration** — automatic tapers and recovery blocks keyed to a target event
- **Sleep debt awareness** — HRV and sleep score from this API decide whether today's quality session moves
- **Shoe mileage** — rotate training across shoes by remaining lifespan
- **Daylight and heat curves** — shift run windows by sunrise/sunset through the seasons
- **Training partners** — someone to run with beats an optimal plan

As mentioned on Reddit, this is one of the best product releases from Garmin in a long time. Finally!