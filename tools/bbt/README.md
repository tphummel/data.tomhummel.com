# BBT / SMM Running Workflow

## Adding a new run

### 1. Export GPX from Garmin Connect
Save to: `~/Documents/santa monica mountains running/activity_XXXXXXXXX.gpx`

The filename must follow the `activity_<garmin_id>.gpx` pattern.

---

### 2. Run sync

```
uv run tools/bbt/sync.py
```

Review the output carefully:

```
activity_23409544287.gpx
  2026-06-28  "Rogers Road Trail and Inspiration Loop from Will Rogers SP"  7.4 mi  +1,177/-1,182 ft
  area: other (needs review)          ← flag: needs manual fix
  BBT: YES — touches 08-trippet-to-will-rogers
```

**Check:**
- `area:` — is the auto-classification correct? Options: `bbt`, `sullivan-mandeville`, `topanga`, `temescal`, `malibu-creek`, `mulholland`, `beaches`, `other`
- `(auto)` vs `(needs review)` — `(needs review)` means no keyword matched; fix manually
- `BBT: YES / no overlap detected` — sync always runs the proximity check regardless of area
- Which segments were touched (if BBT)

---

### 3. Edit the front matter if needed

Open `content/report/adhoc/santa-monica-mountains-running.md` and find the new run entry (it will be at the bottom of the `runs:` list, sorted chronologically after save).

Fix any of:
- `area:` — change from `other` to the correct area key
- `bbt:` — set to `true` if the run touches the BBT and sync missed it (rare)
- `notes:` — add anything worth recording

If you change `bbt: false → true`, you must recompute (see step 4). If you only change `area` or `notes`, skip to step 5.

---

### 4. If BBT flag needed manual correction

```
uv run tools/bbt/recompute_coverage.py
uv run tools/bbt/generate_maps.py
```

This recomputes per-segment miles and new-miles from scratch using all BBT-flagged runs, then regenerates all 9 map PNGs.

---

### 5. Visual check (BBT runs only)

Open the Hugo dev server or inspect the PNGs in `static/images/bbt/`:
- Touched segments should show orange where covered, blue where not
- Total covered miles in the summary should tick up
- Confirm the per-run table on each touched segment looks right (seg miles, new miles)

---

### 6. Commit and push a PR

```
git checkout -b smm-YYYY-MM-DD
git add content/report/adhoc/santa-monica-mountains-running.md static/images/bbt/
git commit -m "Add YYYY-MM-DD SMM run: <route name>"
git push -u origin smm-YYYY-MM-DD
gh pr create
```

---

## When to run each script

| Script | When |
|---|---|
| `sync.py` | Every new run — detects new GPX, updates page, regenerates maps if BBT |
| `recompute_coverage.py` | After manually fixing a `bbt:` flag, or after changing `SEGMENT_SPLITS` |
| `generate_maps.py` | After `recompute_coverage.py`, or to force-refresh all PNGs |
| `migrate_elev.py` | One-time only — already run, can be deleted |

---

## Common issues

**`area: other (needs review)`** — run name didn't match any keyword. Add keywords to `AREA_KEYWORDS` in `sync.py` or just fix the front matter manually.

**BBT not detected when it should be** — set `bbt: true` manually, then run `recompute_coverage.py` + `generate_maps.py`.

**Segment map shows wrong color** — check that `SEGMENT_SPLITS` coordinates in `generate_maps.py` and `sync.py` match. Run `recompute_coverage.py` to refresh data.

**Stale OSM/tile cache** — delete `tools/bbt/data/http_cache.sqlite` to force a full re-fetch of the BBT route and map tiles.
