---
title: What I use Hermes for
date: 2026-11-25T14:00:00+11:00
draft: false
url: /2026/11/what-i-use-hermes-for.html
tags:
  - automation
  - articles
---

### Background

For a couple of years I ran a pile of scripts, cron jobs and half-finished dashboards to manage the boring parts of my life. Earlier this year I replaced most of that with [Hermes](https://hermes-agent.nousresearch.com/), an open source agent that runs on a five year old M1 Mac mini in my kitchen cupboard and talks to me over WhatsApp. Here is what it actually does.

### The daily rhythm

At 5:15am it reviews my training plan for the next ten days against a set of rules I gave it, and checks both my calendars for clashes. At 6am I get a briefing: weather, air quality, any smoke heading our way, birthdays worth knowing about. At 6:30am the structured workout it planned is on my Garmin watch, telling me what to run. Every half hour it checks for email I have sent it and treats the body as an instruction, with anything destructive or financial gated behind a confirmation in the chat. At 2am it backs up our data to Google Drive, and an hourly job commits all of the agent's own state files to git so nothing it does is unversioned.

The important part is what it doesn't do. Most days it says nothing. Silence is the success state.

### Watchers that stay quiet

Several watchers run all day and only speak when something needs a decision. If a storm with hail over two centimetres is within six hours of my car, I hear about it. When bushfire smoke is forecast overnight, we get a reminder to close the windows before bed. The agent also watches the front door camera and lets us know when the neighbour's cat comes to visit. And it keeps an eye on prices: flights I'm tracking (currently a fares watch for my partner's trips to Adelaide), various things on the shopping list, and half-price deals at a handful of Sydney's better restaurants. On Tuesday evenings it checks whether weekend events will make parking impossible near Rose Bay, where my partner launches for early Saturday dives, and once a fortnight it asks whether the bins went out.

There is also a watcher on my local council's development application site, because the block behind us is up for redevelopment and I would rather know about it than not.

### Health and training

The agent syncs my Garmin data every morning through Garmin's Personal API. That is seven years of sleep, HRV, stress and weight data in one SQLite file, with VO2 max recovered by parsing FIT files back to 2019.

It also plans my training week. I gave it a list of rules: no rest days (they wreck my sleep), long runs on weekends only, at most one rings session a week and never in the morning, recovery runs slower than base pace, nothing hard the day before a quality session. It reads my intervals.icu history, builds the week around those rules and my actual calendar, creates the planned workouts, checks for clashes against my personal and work calendars, sends the invites, and the whole thing syncs through to Garmin Connect. If the air quality is terrible on a given morning, it swaps the run for an indoor session and tells me before I am out the door. It also keeps an eye on the evidence behind my supplement stack, and speaks up only if credible advice on something I take actually changes.

### Family logistics

My partner gets a briefing before her tutoring sessions, built from her curriculum notes. It reads my daughter's school newsletter each morning, pulls out anything with a date on it, and puts it in her calendar. It also watches the second-hand uniform marketplace at the high school she starts next year, waiting for a sale to be announced. Charging receipts for my EV are fetched, matched to charging sessions, and submitted as expense claims without me touching a spreadsheet.

### Books

A nightly job scrapes my Goodreads history into a local library of a few hundred books, so recommendations come from what I have actually finished rather than what an algorithm thinks I might like.

### What makes it work

Two things. Everything runs on hardware I own, and the data stays in files I can read. And it proposes rather than acts: anything with a side effect outside my own machines waits for my approval in the chat. That single rule is the difference between a useful assistant and a source of anxiety.

If you have a pile of half-finished automations, an agent with a strict "only talk to me when it matters" policy is a surprisingly good consolidation target.