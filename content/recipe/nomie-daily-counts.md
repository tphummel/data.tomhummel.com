---
title: "Nomie Daily Counts"
date: 2026-10-14T09:00:00-07:00
tags: ["data-exfil", "analysis-recipe"]
---

Count how often you logged each [Nomie 5](https://nomie5.pages.dev/) tracker, per day, week and month.

<!--more-->

1. In Nomie 5, open the settings and export your data as a JSON backup.
1. Open the [Nomie Daily Counts tool](/nomie-daily-counts/) and choose the exported file.
1. Read the table: one row per day, one column per type (`#tracker`, `@person`, `+context`). Weekly (Monday to Sunday) and monthly total rows sit above the days they cover. Pick a year from the dropdown; it starts on the current year.

The tool is a single static page. Parsing happens in your browser and the file is never uploaded.

Notes:

- A day is the day in the timezone the event was logged in.
- An event counts once per type, so `#sneeze(2)` adds 1, not 2.
- Notes with no tag are not counted.
