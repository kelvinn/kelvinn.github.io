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
- The post is written by the author, in their voice. It must never read as coaching or advice from an assistant.
- Prefer "I" for lived experience and "the data shows" for measured claims.
- Avoid over-polished marketing language.

### No advice or coaching

- Do not give the reader (the author) tips, recommendations, or instructions. Avoid imperatives and advisory phrasing such as "Keep that cadence...", "treat X as the thing to avoid", "you should", "consider...", "it would be worth...", "the next step is to...".
- Report what happened and what the data shows. Describe plans only as the author's own intent in first person ("I want to...", "My plan is...", "I'll test...") and only where the author has stated that intent or it continues a documented experiment. Otherwise leave a `TODO:` for the author's plan rather than inventing one.
- Hypotheses are fine when framed as the author's own, or as open questions ("the ferritin trend might point to iron, which I want to look at"). Do not turn lab-report comments into instructions.
- Do not put new suggestions in `### Focus For Next Quarter`; limit it to the author's stated goals, carry-overs from open experiments, and `TODO:` placeholders.
- Before finishing, re-read the post for second-person address ("you") and advisory sentences, and rewrite them as observations or first-person statements.

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
