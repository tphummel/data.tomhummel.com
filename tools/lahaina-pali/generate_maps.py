#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["matplotlib"]
# ///
"""
Render the Lahaina Pali Trail overview map: the whole island of Maui for
geographic context, with the two runs' recorded GPS tracks overlaid, plus a
zoomed inset showing the trail detail.

Unlike the BBT maps (tools/bbt/generate_maps.py), this does not fetch OSM
tiles or an official trail relation at generation time — the island outline
is a small pre-extracted GeoJSON checked into tools/lahaina-pali/data/ (see
that directory's README for provenance), and the trail lines are the actual
recorded tracks. That keeps this script network-free.

Run after adding new runs via import_tcx.py:
    uv run tools/lahaina-pali/generate_maps.py
"""

import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

sys.path.insert(0, str(Path(__file__).parent))
from lib import load_tcx  # noqa: E402

REPO_ROOT = Path(__file__).parent.parent.parent
TCX_DIR = Path.home() / "Documents" / "lahaina pali trail running"
OUT_DIR = REPO_ROOT / "static" / "images" / "lahaina-pali"
ISLANDS_PATH = Path(__file__).parent / "data" / "maui-county.geojson"

COLORS = {
    "east": "#c1440e",  # matches BBT "covered" orange family
    "west": "#1f6f8b",
}
LABELS = {
    "east": "From Māʻalaea (East)",
    "west": "From Ukumehame (West)",
}
OCEAN_COLOR = "#dce9f0"
LAND_COLOR = "#e8e2d3"
LAND_EDGE_COLOR = "#b9ae95"


def load_islands():
    data = json.loads(ISLANDS_PATH.read_text())
    islands = []
    for feat in data["features"]:
        geom = feat["geometry"]
        polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
        for poly in polys:
            islands.append(poly[0])  # exterior ring only
    return islands


def draw_islands(ax, islands, lon_scale):
    for ring in islands:
        lons = [pt[0] * lon_scale for pt in ring]
        lats = [pt[1] for pt in ring]
        ax.fill(lons, lats, facecolor=LAND_COLOR, edgecolor=LAND_EDGE_COLOR, linewidth=1, zorder=1)


def draw_tracks(ax, runs, lon_scale, linewidth):
    for run in runs:
        lats = [p["lat"] for p in run["points"]]
        lons = [p["lon"] * lon_scale for p in run["points"]]
        color = COLORS.get(run["trailhead"], "#555555")
        ax.plot(lons, lats, color=color, linewidth=linewidth, solid_capstyle="round",
                 label=LABELS.get(run["trailhead"], run["trailhead"]), zorder=3)
        start = run["points"][0]
        ax.scatter([start["lon"] * lon_scale], [start["lat"]], color=color, s=90,
                    zorder=4, edgecolor="white", linewidth=1.2)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tcx_files = sorted(TCX_DIR.glob("activity_*.tcx"))
    if not tcx_files:
        print(f"No TCX files found in {TCX_DIR}")
        return

    runs = [load_tcx(p) for p in tcx_files]
    islands = load_islands()

    all_lats = [p["lat"] for r in runs for p in r["points"]]
    all_lons = [p["lon"] for r in runs for p in r["points"]]
    mean_lat = sum(all_lats) / len(all_lats)
    lon_scale = math.cos(math.radians(mean_lat))

    # Main island (largest ring by point count is Maui itself in this dataset)
    maui_ring = max(islands, key=len)
    maui_lons = [pt[0] * lon_scale for pt in maui_ring]
    maui_lats = [pt[1] for pt in maui_ring]

    pad = 0.10
    isl_lon_span = (max(maui_lons) - min(maui_lons)) * (1 + 2 * pad)
    isl_lat_span = (max(maui_lats) - min(maui_lats)) * (1 + 2 * pad)
    isl_lon_mid = (max(maui_lons) + min(maui_lons)) / 2
    isl_lat_mid = (max(maui_lats) + min(maui_lats)) / 2

    fig_w = 9.0
    title_allowance_in = 0.7
    fig_h = fig_w * (isl_lat_span / isl_lon_span) + title_allowance_in

    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)
    fig.subplots_adjust(top=1 - title_allowance_in / fig_h, bottom=0, left=0, right=1)
    fig.patch.set_facecolor("white")
    ax.set_facecolor(OCEAN_COLOR)

    draw_islands(ax, islands, lon_scale)
    draw_tracks(ax, runs, lon_scale, linewidth=3.5)

    ax.set_xlim(isl_lon_mid - isl_lon_span / 2, isl_lon_mid + isl_lon_span / 2)
    ax.set_ylim(isl_lat_mid - isl_lat_span / 2, isl_lat_mid + isl_lat_span / 2)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title("Lahaina Pali Trail — Maui", fontsize=14, fontweight="bold", pad=14)
    ax.legend(loc="lower right", frameon=False, fontsize=9)

    # --- Zoomed inset showing the trail detail ---
    trail_pad = 0.18
    trail_lon_span = (max(p["lon"] for r in runs for p in r["points"])
                       - min(p["lon"] for r in runs for p in r["points"])) * lon_scale
    trail_lat_span = max(all_lats) - min(all_lats)
    trail_lon_mid = (max(p["lon"] for r in runs for p in r["points"])
                      + min(p["lon"] for r in runs for p in r["points"])) / 2 * lon_scale
    trail_lat_mid = (max(all_lats) + min(all_lats)) / 2

    axins = ax.inset_axes([0.04, 0.50, 0.46, 0.46])
    draw_islands(axins, islands, lon_scale)
    draw_tracks(axins, runs, lon_scale, linewidth=2.5)
    axins.set_xlim(trail_lon_mid - trail_lon_span * (1 + 2 * trail_pad) / 2,
                    trail_lon_mid + trail_lon_span * (1 + 2 * trail_pad) / 2)
    axins.set_ylim(trail_lat_mid - trail_lat_span * (1 + 2 * trail_pad) / 2,
                    trail_lat_mid + trail_lat_span * (1 + 2 * trail_pad) / 2)
    axins.set_aspect("equal")
    axins.set_xticks([])
    axins.set_yticks([])
    axins.set_facecolor(OCEAN_COLOR)
    for spine in axins.spines.values():
        spine.set_edgecolor("#666666")
        spine.set_linewidth(1)
    mark_inset(ax, axins, loc1=2, loc2=4, edgecolor="#666666", linewidth=1, zorder=5)

    out_path = OUT_DIR / "overview.png"
    fig.savefig(out_path, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Wrote {out_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
