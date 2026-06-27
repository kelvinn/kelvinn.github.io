# Health Review Post Style

Use the existing quarterly posts as the primary style source. Completed examples include:

- `content/posts/2026-q1-health-review/index.md`
- `content/posts/2025-q4-health-review/index.md`

## Structure

Keep this order:

1. `### Reflection`
2. `### Focus Areas`
3. quarter snapshot and quarter-over-quarter highlights
4. correlation matrix and correlation notes
5. `#### Improve Fitness`
6. `#### Improve Sleep`
7. `#### Decrease Stress`
8. `#### Improve Biomarkers`
9. `#### Improve Nutrition`
10. `### Supplement Stack`
11. `### Focus For Next Quarter`

Each focus area usually contains:

- `##### Goals`
- `##### Analysis`
- `##### Experiments`

## Voice

- Personal, reflective, and direct.
- Data-grounded rather than clinical.
- Willing to call out bad quarters plainly, but framed around learning and next actions.
- Prefer "I" for lived experience and "the data shows" for measured claims.
- Avoid over-polished marketing language.

## Goal Status Symbols

Use:

- `✅` achieved
- `❌` missed or moved in the wrong direction
- `⚠️` mixed, borderline, or slightly below target
- `❓` insufficient data or not yet clear
- `⚪` not evaluated / no data

## Image Conventions

Use relative image paths from the post folder:

```markdown
![Summary Chart](summary.png)
![Correlation Matrix](correlation_matrix.png)
![Weekly Intensity Minutes](weekly_intensity_minutes.png)
```

Do not use old absolute repo paths like `content/posts/...` in new posts.

## Template Cleanup

Remove template prompts like:

- `Which 3-5 metrics changed...`
- `[Biomarker 1]`
- `[Supplement + dose]`
- `What defined this quarter overall?`

Leave `TODO:` only when a personal note is required from the user.
