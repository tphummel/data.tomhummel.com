# BBT / SMM Running Workflow

## Adding a new run

### 1. Export GPX from Garmin Connect
Save to: `~/Documents/santa monica mountains running/activity_XXXXXXXXX.gpx`

### 2. Run sync

```
uv run tools/bbt/sync.py
```

Review the output:

```
activity_23409544287.gpx
  2026-06-28  "Rogers Road Trail..."  7.4 mi  +1,177/-1,182 ft
  area: other (needs review)
  BBT: YES — touches 08-trippet-to-will-rogers
```

Check:
- `area:` — correct? Options: `bbt`, `sullivan-mandeville`, `topanga`, `temescal`, `malibu-creek`, `mulholland`, `beaches`, `other`
- `(auto)` vs `(needs review)` — the latter means no keyword matched; fix manually
- `BBT:` — sync always runs the proximity check regardless of area

### 3. Fix front matter if needed

Find the new run in `content/report/adhoc/santa-monica-mountains-running.md` and fix:
- `area:` — correct area key
- `bbt:` — set `true` if sync missed a BBT overlap
- `notes:` — anything worth recording

If you change `bbt: false → true`, continue to step 4. Otherwise skip to step 5.

### 4. Recompute (only if BBT flag was manually corrected)

```
uv run tools/bbt/recompute_coverage.py
uv run tools/bbt/generate_maps.py
uv run tools/bbt/generate_elevation.py
```

### 5. Visual check (BBT runs only)

Inspect PNGs in `static/images/bbt/` or run `hugo server`:
- Touched segments: orange where covered, blue where not
- Per-run table on each touched segment looks right

### 6. Commit and push a PR

```
git checkout -b smm-YYYY-MM-DD
git add content/report/adhoc/santa-monica-mountains-running.md static/images/bbt/
git commit -m "Add YYYY-MM-DD SMM run: <route name>"
git push -u origin smm-YYYY-MM-DD
gh pr create
```

---

## Script reference

| Script | When |
|---|---|
| `sync.py` | Every new run |
| `recompute_coverage.py` | After manually fixing a `bbt:` flag, or after changing `SEGMENT_SPLITS` |
| `generate_maps.py` | After `recompute_coverage.py`, or to force-refresh map PNGs |
| `generate_elevation.py` | After `recompute_coverage.py`, or to force-refresh elevation chart PNGs |

---

## Troubleshooting

**`area: other (needs review)`** — fix manually or add keywords to `AREA_KEYWORDS` in `sync.py`.

**BBT not detected** — set `bbt: true` manually, then run `recompute_coverage.py` + `generate_maps.py`.

**Stale OSM/tile cache** — delete `tools/bbt/data/http_cache.sqlite` to force a full re-fetch.
