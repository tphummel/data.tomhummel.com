#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["ruamel.yaml"]
# ///
"""
Sync new TCX files from ~/Documents/lahaina pali trail running into the
Lahaina Pali Trail running page: computes per-run stats and mile splits from
Garmin Lap/Trackpoint data and writes them into the page front matter.

Drop a new TCX file in the source directory, then run:
    uv run tools/lahaina-pali/import_tcx.py

Unlike the Santa Monica Mountains (BBT) tooling, this does not fetch any
official trail geometry or basemap tiles — the map/elevation images are
rendered straight from the recorded GPS + elevation stream (see
generate_maps.py / generate_elevation.py), so the whole pipeline runs with
no network access.
"""

import io
import sys
from pathlib import Path

from ruamel.yaml import YAML

sys.path.insert(0, str(Path(__file__).parent))
from lib import (  # noqa: E402
    TRAILHEADS,
    elev_gain_loss_m,
    format_duration,
    format_pace,
    load_tcx,
    turnaround_point,
)

REPO_ROOT = Path(__file__).parent.parent.parent
PAGE_PATH = REPO_ROOT / "content" / "report" / "adhoc" / "lahaina-pali-trail-running.md"
TCX_DIR = Path.home() / "Documents" / "lahaina pali trail running"

TRAILHEAD_ROUTE_NAME = {
    "east": "Lahaina Pali Trail from Māʻalaea (East) Trailhead",
    "west": "Lahaina Pali Trail from Ukumehame (West) Trailhead",
}

PAGE_TEMPLATE = """---
title: "Lahaina Pali Trail Running"
date: __DATE__T00:00:00Z
tags: ["running", "trail", "maui", "hawaii"]
trail:
  name: Lahaina Pali Trail
  system: "Nā Ala Hele — Hawaiʻi Trail & Access System"
  length_mi: 4.8
  elev_gain_ft: 1630
  elev_loss_ft: 1407
  trailheads:
  - key: east
    name: "__EAST_LABEL__"
    address: "Dirt road off Hwy 30, just south of the Hwy 30 / Hwy 380 junction, ~2.5 mi south of Wailuku"
  - key: west
    name: "__WEST_LABEL__"
    address: "Highway 30 pullout ~0.25 mi north of the Lāhainā Pali Tunnel, ~3 mi west of Māʻalaea Harbor"
runs: []
---

<!--more-->

{{< detail.inline >}}
{{< /detail.inline >}}
"""
PAGE_TEMPLATE = (
    PAGE_TEMPLATE
    .replace("__EAST_LABEL__", TRAILHEADS["east"]["label"])
    .replace("__WEST_LABEL__", TRAILHEADS["west"]["label"])
)


def load_page():
    if not PAGE_PATH.exists():
        PAGE_PATH.write_text(PAGE_TEMPLATE.replace("__DATE__", "2026-01-01"))
    text = PAGE_PATH.read_text()
    _, fm_text, body = text.split("---", 2)
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    data = yaml.load(fm_text)
    return data, body


def save_page(data, body):
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    yaml.default_flow_style = False
    stream = io.StringIO()
    yaml.dump(data, stream)
    fm_text = stream.getvalue()
    PAGE_PATH.write_text(f"---\n{fm_text}---{body}")


def build_run_entry(tcx):
    points, laps = tcx["points"], tcx["laps"]
    gain_m, loss_m = elev_gain_loss_m(points)
    elevs = [p["elev_m"] for p in points if p["elev_m"] is not None]
    hrs = [p["hr"] for p in points if p["hr"] is not None]
    total_dist_m = points[-1]["dist_m"]
    total_time_s = sum(lap["time_s"] for lap in laps)
    turn = turnaround_point(points)

    lap_entries = []
    for i, lap in enumerate(laps, start=1):
        dist_mi = lap["distance_m"] / 1609.344
        pace_s_per_mi = lap["time_s"] / dist_mi if dist_mi > 0 else 0
        lap_entries.append({
            "mile": i,
            "distance_mi": round(dist_mi, 2),
            "time": format_duration(lap["time_s"]),
            "pace": format_pace(pace_s_per_mi) if dist_mi >= 0.1 else None,
            "avg_hr": lap["avg_hr"],
            "max_hr": lap["max_hr"],
            "calories": lap["calories"],
        })

    return {
        "date": tcx["date"],
        "garmin_id": tcx["garmin_id"],
        "name": TRAILHEAD_ROUTE_NAME.get(tcx["trailhead"], "Lahaina Pali Trail"),
        "trailhead": tcx["trailhead"],
        "miles": round(total_dist_m / 1609.344, 2),
        "elev_gain_ft": int(round(gain_m * 3.28084)),
        "elev_loss_ft": int(round(loss_m * 3.28084)),
        "elev_min_ft": int(round(min(elevs) * 3.28084)),
        "elev_max_ft": int(round(max(elevs) * 3.28084)),
        "duration": format_duration(total_time_s),
        "avg_pace": format_pace(total_time_s / (total_dist_m / 1609.344)),
        "avg_hr": round(sum(hrs) / len(hrs)) if hrs else None,
        "max_hr": max(hrs) if hrs else None,
        "calories": sum(lap["calories"] for lap in laps if lap["calories"]),
        "start_lat": round(points[0]["lat"], 5),
        "start_lon": round(points[0]["lon"], 5),
        "turnaround_lat": round(turn["lat"], 5),
        "turnaround_lon": round(turn["lon"], 5),
        "laps": lap_entries,
        "notes": "",
    }


def main():
    TCX_DIR.mkdir(parents=True, exist_ok=True)
    data, body = load_page()
    existing_ids = {str(r.get("garmin_id", "")) for r in data.get("runs", [])}

    tcx_files = sorted(TCX_DIR.glob("activity_*.tcx"))
    new_files = [f for f in tcx_files if str(_gid(f)) not in existing_ids]

    if not new_files:
        print("No new TCX files found. Nothing to do.")
        return

    print(f"Found {len(new_files)} new TCX file(s):")
    runs = list(data.get("runs", []))
    for path in new_files:
        tcx = load_tcx(path)
        entry = build_run_entry(tcx)
        runs.append(entry)
        print(f"\n  {path.name}")
        print(f"    {entry['date']}  \"{entry['name']}\"")
        print(f"    {entry['miles']} mi  +{entry['elev_gain_ft']:,}/-{entry['elev_loss_ft']:,} ft"
              f"  {entry['duration']}  avg pace {entry['avg_pace']}  avg HR {entry['avg_hr']}")

    runs.sort(key=lambda r: str(r.get("date", "")))
    data["runs"] = runs
    data["date"] = f"{runs[-1]['date']}T00:00:00Z"  # most recent run date

    save_page(data, body)
    print(f"\nUpdated: {PAGE_PATH.relative_to(REPO_ROOT)}")
    print(f"  {len(new_files)} run(s) added")
    print("\nNext: uv run tools/lahaina-pali/generate_maps.py")
    print("      uv run tools/lahaina-pali/generate_elevation.py")


def _gid(path):
    stem = path.stem
    parts = stem.split("_")
    gid = parts[-1] if len(parts) >= 2 else stem
    return gid


if __name__ == "__main__":
    main()
