---
title: What I use Hermes for
date: 2026-11-25T14:00:00+11:00
draft: true
url: /2026/11/what-i-use-hermes-for.html
tags:
  - automation
  - articles
---

### Background

For a couple of years I ran various scripts, cron jobs and half-finished dashboards to manage the boring parts of my life. Earlier this year I replaced most of that with [Hermes](https://hermes-agent.nousresearch.com/), an open source agent that lives on the Mac mini under my desk and talks to me over WhatsApp. It has quietly become the most useful piece of software in the house, so I wanted to write down what it actually does.

### The daily rhythm

At 6am I get a briefing: weather for Sydney, air quality, whether there is any smoke around, birthdays I should know about. At 2am it backs up our data to Google Drive. At 5:15am it reviews my training plan for the next ten days against a set of rules I gave it, and checks my calendars for clashes.

The important part of all of this is what it doesn't do. I have a standing rule that it only messages me when something needs a decision. Most days the hail watcher, the bushfire smoke watcher, and the council development application monitor for my street all run and say nothing. Silence is the success state. When a storm with hail over two centimetres is actually within six hours of my car, then I hear about it.

### Health and training

I moved my Garmin data off a local database and into a setup where the agent syncs everything daily through Garmin's new Personal API. That is seven years of sleep, HRV, stress and weight data in one SQLite file, with VO2 max recovered by parsing FIT files all the way back to 2019.

The more interesting piece is training. The agent reads my [intervals.icu](https://intervals.icu/) history, plans my week around constraints I've given it (no rest days, long runs on weekends, strength sessions with warm-up blocks, nothing hard the day before a quality run), creates the planned workouts, checks both my personal and work calendars for clashes, and sends the invites. Garmin then picks up those structured workouts so my watch tells me what to do at 6:30am.

### Family logistics

There is a daily maths quiz running for my daughter's selective exam preparation, built on the site I made for exactly that. My partner gets a briefing for her tutoring work. Nothing fancy, just the kind of repetitive coordination that used to fall through the cracks.

### Books

A nightly job scrapes my Goodreads history into a local library of a few hundred books, so I can ask for reading recommendations against what I have actually finished rather than what an algorithm thinks I might like.

### What makes it work

Two things. First, everything runs on hardware I own, and the data stays in files I can read. Second, it proposes rather than acts: anything with a side effect outside my own machines waits for my approval in the chat. That single rule is the difference between a useful assistant and a source of anxiety.

If you have a pile of half-finished automations, an agent with a strict "only talk to me when it matters" policy is a surprisingly good consolidation target.