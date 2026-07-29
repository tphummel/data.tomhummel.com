# Lahaina Pali Trail Running Workflow

Adds runs to the [Lahaina Pali Trail](/report/adhoc/lahaina-pali-trail-running/)
page (Maui). Unlike the Santa Monica Mountains / BBT tooling (`tools/bbt/`),
this does **not** fetch OSM tiles, an official trail relation, or SRTM
elevation — the map and elevation charts are rendered straight from each
run's recorded GPS + barometric-altitude stream, so the whole pipeline runs
with no network access.

## Adding a new run

### 1. Export TCX from Garmin Connect

TCX (not GPX) — it carries per-mile Lap data (pace, heart rate, calories)
that the splits tables use.

Save to: `~/Documents/lahaina pali trail running/activity_XXXXXXXXX.tcx`

### 2. Run the import

```
uv run content/report/adhoc/lahaina-pali-trail-running/tools/import_tcx.py
```

Review the output — computed distance, elevation gain/loss, duration, pace,
and average HR per run. It writes a new entry into the `runs:` list in
`content/report/adhoc/lahaina-pali-trail-running/index.md`, classifying the run's
trailhead (`east`/`west`) by proximity to the two recorded starting points in
`lib.py`'s `TRAILHEADS`.

### 3. Regenerate images

```
uv run content/report/adhoc/lahaina-pali-trail-running/tools/generate_maps.py
uv run content/report/adhoc/lahaina-pali-trail-running/tools/generate_elevation.py
```

`generate_maps.py` re-plots the whole-island map (`images/overview-island.png`)
and the trail close-up (`images/overview-trail.png`) from every TCX file in
the source directory, one line per run colored by trailhead.
`generate_elevation.py` writes a full + thumbnail elevation profile PNG per
run (`images/{date}-{trailhead}-elev[-thumb].png`).

### 4. Visual check

```
hugo server
```

Check the map and elevation charts render, and the splits table matches the
Garmin activity.

### 5. Commit and push

```
git add content/report/adhoc/lahaina-pali-trail-running/index.md content/report/adhoc/lahaina-pali-trail-running/images/
git commit -m "Add YYYY-MM-DD Lahaina Pali Trail run"
git push
```

Everything for this post — the page, its images, and this tooling — lives
together under `content/report/adhoc/lahaina-pali-trail-running/`. The
`tools/` and `tools/data/` subdirectories are excluded from the Hugo build
(see `ignoreFiles` in `config.toml`), so only `index.md` and `images/` are
published.

---

## Script reference

| Script | When |
|---|---|
| `import_tcx.py` | Every new run |
| `generate_maps.py` | After `import_tcx.py`, or to force-refresh the overview map |
| `generate_elevation.py` | After `import_tcx.py`, or to force-refresh elevation chart PNGs |

`lib.py` holds the shared TCX parsing and the `TRAILHEADS` proximity
classifier — edit it if a future run starts from a different point (e.g. a
mid-trail access point) than the two recorded so far.
