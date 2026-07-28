#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["matplotlib", "ruamel.yaml", "pillow"]
# ///
"""
Render two maps for the Lahaina Pali Trail page from the recorded TCX
tracks: a whole-island view for geographic context, and a close-up of the
trail itself.

Unlike the BBT maps (tools/bbt/generate_maps.py), this does not fetch OSM
tiles or an official trail relation at generation time — the island outline
is a small pre-extracted GeoJSON checked into content/report/adhoc/lahaina-pali-trail-running/tools/data/ (see
that directory's README for provenance), and the trail lines are the actual
recorded tracks. That keeps this script network-free.

Run after adding new runs via import_tcx.py:
    uv run content/report/adhoc/lahaina-pali-trail-running/tools/generate_maps.py
"""

import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ruamel.yaml import YAML

sys.path.insert(0, str(Path(__file__).parent))
from lib import load_tcx, savefig_webp  # noqa: E402

BUNDLE_DIR = Path(__file__).parent.parent  # content/report/adhoc/lahaina-pali-trail-running/
PAGE_PATH = BUNDLE_DIR / "index.md"
TCX_DIR = Path.home() / "Documents" / "lahaina pali trail running"
OUT_DIR = BUNDLE_DIR / "images"
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

TITLE_ALLOWANCE_IN = 0.7
FIG_W = 9.0


def load_photos():
    yaml = YAML()
    text = PAGE_PATH.read_text()
    _, fm_text, _ = text.split("---", 2)
    data = yaml.load(fm_text)
    return data.get("photos", [])


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


def draw_photos(ax, photos, lon_scale):
    if not photos:
        return
    lons = [p["lon"] * lon_scale for p in photos]
    lats = [p["lat"] for p in photos]
    ax.scatter(lons, lats, marker="o", s=55, facecolor="white", edgecolor="#222222",
               linewidth=1.3, zorder=5, label="Photo")


def make_map(out_path, islands, runs, lon_scale, lon_mid, lat_mid, lon_span, lat_span,
             title, track_linewidth, legend_loc, photos=None):
    fig_h = FIG_W * (lat_span / lon_span) + TITLE_ALLOWANCE_IN
    fig, ax = plt.subplots(figsize=(FIG_W, fig_h), dpi=150)
    fig.subplots_adjust(top=1 - TITLE_ALLOWANCE_IN / fig_h, bottom=0, left=0, right=1)
    fig.patch.set_facecolor("white")
    ax.set_facecolor(OCEAN_COLOR)

    draw_islands(ax, islands, lon_scale)
    draw_tracks(ax, runs, lon_scale, linewidth=track_linewidth)
    draw_photos(ax, photos, lon_scale)

    ax.set_xlim(lon_mid - lon_span / 2, lon_mid + lon_span / 2)
    ax.set_ylim(lat_mid - lat_span / 2, lat_mid + lat_span / 2)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=14)
    ax.legend(loc=legend_loc, frameon=False, fontsize=9)

    savefig_webp(fig, out_path)
    plt.close(fig)
    print(f"Wrote {out_path.relative_to(BUNDLE_DIR)}")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tcx_files = sorted(TCX_DIR.glob("activity_*.tcx"))
    if not tcx_files:
        print(f"No TCX files found in {TCX_DIR}")
        return

    runs = [load_tcx(p) for p in tcx_files]
    islands = load_islands()
    photos = load_photos()

    all_lats = [p["lat"] for r in runs for p in r["points"]]
    all_lons = [p["lon"] for r in runs for p in r["points"]]
    mean_lat = sum(all_lats) / len(all_lats)
    lon_scale = math.cos(math.radians(mean_lat))

    # --- Island map: whole Maui for geographic context ---
    maui_ring = max(islands, key=len)  # largest ring by point count is Maui itself
    maui_lons = [pt[0] * lon_scale for pt in maui_ring]
    maui_lats = [pt[1] for pt in maui_ring]

    isl_pad = 0.10
    isl_lon_span = (max(maui_lons) - min(maui_lons)) * (1 + 2 * isl_pad)
    isl_lat_span = (max(maui_lats) - min(maui_lats)) * (1 + 2 * isl_pad)
    isl_lon_mid = (max(maui_lons) + min(maui_lons)) / 2
    isl_lat_mid = (max(maui_lats) + min(maui_lats)) / 2

    make_map(
        OUT_DIR / "overview-island.webp", islands, runs, lon_scale,
        isl_lon_mid, isl_lat_mid, isl_lon_span, isl_lat_span,
        title="Lahaina Pali Trail — Maui", track_linewidth=3.5, legend_loc="lower right",
    )

    # --- Trail map: close-up of the actual tracks ---
    trail_pad = 0.18
    trail_lons = [p["lon"] * lon_scale for r in runs for p in r["points"]]
    trail_lats = all_lats
    trail_lon_span = (max(trail_lons) - min(trail_lons)) * (1 + 2 * trail_pad)
    trail_lat_span = (max(trail_lats) - min(trail_lats)) * (1 + 2 * trail_pad)
    trail_lon_mid = (max(trail_lons) + min(trail_lons)) / 2
    trail_lat_mid = (max(trail_lats) + min(trail_lats)) / 2

    make_map(
        OUT_DIR / "overview-trail.webp", islands, runs, lon_scale,
        trail_lon_mid, trail_lat_mid, trail_lon_span, trail_lat_span,
        title="Lahaina Pali Trail — Detail", track_linewidth=2.5, legend_loc="lower center",
        photos=photos,
    )


if __name__ == "__main__":
    main()
