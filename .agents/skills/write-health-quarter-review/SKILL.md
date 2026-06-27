---
name: write-health-quarter-review
description: Create, update, or complete quarterly personal health review blog posts in this repo. Use when asked to write a quarterly health post, fill a health-review template, generate Garmin/LifeDB health analysis, update health-review charts or CSVs, or compare quarterly biomarkers from the Life Planning Google Sheet.
---

# Write Health Quarter Review

## Overview

Use this skill to edit quarterly health review posts under `content/posts/YYYY-qN-health-review/`.
It combines repo-local post templates, generated chart/CSV assets, LifeDB Garmin data, and biomarker data from the Life Planning Google Sheet.

## Required Context

Read these before editing a post:

1. `AGENTS.md` in the repo root for the health runbook and LifeDB query rules.
2. `references/post-style.md` for the expected post structure and voice.
3. `references/data-sources.md` for asset, CSV, LifeDB, and Google Sheet sources.
4. `references/biomarker-rules.md` before writing the biomarkers section.
5. `references/migration-from-notebooks.md` before changing chart or analysis generation.

Also read:

- The target quarter `index.md` if it exists.
- The previous quarter post.
- At least one other recent completed health review when style or continuity is uncertain.

## Workflow

1. Determine the target year and quarter from the user request, current post path, or current date.
2. Compute quarter boundaries:
   - Q1: Jan 1 to Mar 31
   - Q2: Apr 1 to Jun 30
   - Q3: Jul 1 to Sep 30
   - Q4: Oct 1 to Dec 31
3. If the target post folder does not exist, create it from `content/posts/20NN-qN-health-review-TEMPLATE/` with `scripts/create_quarter_post.py`.
4. If generated assets or CSVs are missing or stale, generate them with `scripts/generate_health_assets.py`.
5. Summarize generated CSVs with `scripts/summarize_health_data.py`.
6. Use LifeDB MCP for Garmin health, fitness, sleep, stress, body battery, HRV, steps, VO2 max, or activity data that is missing, suspicious, or freshness-sensitive.
7. Use the Google Sheets connector for biomarker and PhenoAge data.
8. Edit `index.md` directly.
9. Validate the result with `scripts/validate_health_post.py`.

When the quarter has not ended yet, write the post as provisional and keep `draft: true`.

## Writing Rules

- Preserve the post's existing frontmatter fields unless they are wrong for the target quarter.
- Keep image references relative, such as `summary.png`.
- Replace template prompts with evidence-backed prose.
- Use explicit TODOs only for personal context that cannot be inferred from data, such as subjective experiment notes or travel/work explanations.
- Do not invent personal causes for metric changes. Say what the data shows and mark likely explanations as hypotheses.
- Include counts when using aggregates, for example number of nights, days, weeks, or activities.
- Prefer exact quarter labels such as `Q2 2026`.
- Carry forward prior-quarter biomarker goals, then add critical new out-of-range biomarkers.

## Useful Scripts

Create a new post from the template:

```bash
python .agents/skills/write-health-quarter-review/scripts/create_quarter_post.py --year 2026 --quarter 3
```

Generate assets with the current notebook pipeline:

```bash
python .agents/skills/write-health-quarter-review/scripts/generate_health_assets.py --year 2026 --quarter 2
```

Summarize generated data:

```bash
python .agents/skills/write-health-quarter-review/scripts/summarize_health_data.py content/posts/2026-q2-health-review
```

Validate a finished post:

```bash
python .agents/skills/write-health-quarter-review/scripts/validate_health_post.py content/posts/2026-q2-health-review
```
