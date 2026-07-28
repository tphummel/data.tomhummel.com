#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["matplotlib"]
# ///
"""
Render an overview route map for the Lahaina Pali Trail page from the
recorded TCX tracks — one line per run, colored by trailhead, with
trailhead + turnaround markers.

Unlike the BBT maps (tools/bbt/generate_maps.py), this does not fetch OSM
tiles or an official trail relation: the two runs' actual GPS tracks are
the map. That keeps this script network-free, which matters because this
trail only needed two out-and-back runs (one from each end, meeting near
the same mid-trail high point) to cover end to end — there's no ongoing
segment-coverage bookkeeping to do.

Run after adding new runs via import_tcx.py:
    uv run tools/lahaina-pali/generate_maps.py
"""

import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
from lib import load_tcx  # noqa: E402

REPO_ROOT = Path(__file__).parent.parent.parent
TCX_DIR = Path.home() / "Documents" / "lahaina pali trail running"
OUT_DIR = REPO_ROOT / "static" / "images" / "lahaina-pali"

COLORS = {
    "east": "#c1440e",  # matches BBT "covered" orange family
    "west": "#1f6f8b",
}
LABELS = {
    "east": "From Māʻalaea (East)",
    "west": "From Ukumehame (West)",
}


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tcx_files = sorted(TCX_DIR.glob("activity_*.tcx"))
    if not tcx_files:
        print(f"No TCX files found in {TCX_DIR}")
        return

    runs = [load_tcx(p) for p in tcx_files]

    # Equirectangular approximation, scaled by cos(lat) so the plot reads
    # as true-shaped at this latitude without needing a tile projection.
    all_lats = [p["lat"] for r in runs for p in r["points"]]
    all_lons = [p["lon"] for r in runs for p in r["points"]]
    mean_lat = sum(all_lats) / len(all_lats)
    lon_scale = math.cos(math.radians(mean_lat))

    pad = 0.12
    lat_span = (max(all_lats) - min(all_lats)) * (1 + 2 * pad)
    lon_span = (max(all_lons) - min(all_lons)) * lon_scale * (1 + 2 * pad)
    fig_w = 9.0
    title_allowance_in = 0.7  # ax.set_title space, reserved outside the data box
    fig_h = fig_w * (lat_span / lon_span) + title_allowance_in

    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)
    fig.subplots_adjust(top=1 - title_allowance_in / fig_h, bottom=0, left=0, right=1)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#f4f1ea")

    for run in runs:
        lats = [p["lat"] for p in run["points"]]
        lons = [p["lon"] for p in run["points"]]
        color = COLORS.get(run["trailhead"], "#555555")
        ax.plot(
            [lo * lon_scale for lo in lons], lats,
            color=color, linewidth=2.5, solid_capstyle="round",
            label=LABELS.get(run["trailhead"], run["trailhead"]), zorder=3,
        )
        start = run["points"][0]
        ax.scatter([start["lon"] * lon_scale], [start["lat"]], color=color,
                   s=90, zorder=4, edgecolor="white", linewidth=1.2)

    lon_mid = (max(all_lons) + min(all_lons)) / 2 * lon_scale
    lat_mid = (max(all_lats) + min(all_lats)) / 2
    ax.set_xlim(lon_mid - lon_span / 2, lon_mid + lon_span / 2)
    ax.set_ylim(lat_mid - lat_span / 2, lat_mid + lat_span / 2)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title("Lahaina Pali Trail — Maui", fontsize=14, fontweight="bold", pad=14)
    ax.legend(loc="lower center", frameon=False, ncol=2, fontsize=10)

    out_path = OUT_DIR / "overview.png"
    fig.savefig(out_path, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Wrote {out_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
