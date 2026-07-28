#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["matplotlib"]
# ///
"""
Render an elevation-vs-distance profile PNG (full + thumbnail) for each run
on the Lahaina Pali Trail page, straight from the TCX-recorded altitude
stream (the Forerunner's barometric altimeter) — no SRTM/network lookup
needed, unlike tools/bbt/generate_elevation.py.

Run after adding new runs via import_tcx.py:
    uv run tools/lahaina-pali/generate_elevation.py
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
from lib import TRAILHEADS, load_tcx  # noqa: E402

REPO_ROOT = Path(__file__).parent.parent.parent
TCX_DIR = Path.home() / "Documents" / "lahaina pali trail running"
OUT_DIR = REPO_ROOT / "static" / "images" / "lahaina-pali"

COLORS = {
    "east": "#c1440e",
    "west": "#1f6f8b",
}
ROUTE_NAME = {
    key: f"Lahaina Pali Trail from {th['label']}" for key, th in TRAILHEADS.items()
}


def moving_avg(vals, window=11):
    n = len(vals)
    return [
        sum(vals[max(0, i - window // 2):min(n, i + window // 2 + 1)])
        / len(vals[max(0, i - window // 2):min(n, i + window // 2 + 1)])
        for i in range(n)
    ]


def slug_for(run):
    return f"{run['date']}-{run['trailhead']}"


def make_chart(run, out_path, thumb=False):
    points = run["points"]
    dist_mi = [p["dist_m"] / 1609.344 for p in points]
    elev_ft = moving_avg([p["elev_m"] * 3.28084 for p in points], window=11)
    color = COLORS.get(run["trailhead"], "#555555")

    elev_min, elev_max = min(elev_ft), max(elev_ft)
    base = elev_min - (elev_max - elev_min) * 0.12

    if thumb:
        fig, ax = plt.subplots(figsize=(3.5, 0.9), dpi=100)
    else:
        fig, ax = plt.subplots(figsize=(9, 2.8), dpi=150)

    fig.patch.set_facecolor("white")
    ax.set_facecolor("#f9f9f9")
    ax.fill_between(dist_mi, elev_ft, base, color=color, alpha=0.35, linewidth=0)
    ax.plot(dist_mi, elev_ft, color=color, linewidth=1.6)
    ax.set_ylim(base, elev_max + (elev_max - elev_min) * 0.1)
    ax.set_xlim(0, dist_mi[-1])

    if thumb:
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
    else:
        for mile in range(1, int(dist_mi[-1]) + 1):
            ax.axvline(mile, color="#999999", linewidth=0.6, linestyle=":", zorder=1)
        ax.set_xlabel("Miles")
        ax.set_ylabel("Elevation (ft)")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        name = ROUTE_NAME.get(run["trailhead"], "Lahaina Pali Trail")
        ax.set_title(f"{name} — {run['date']}", fontsize=11, loc="left")

    fig.tight_layout()
    fig.savefig(out_path, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Wrote {out_path.relative_to(REPO_ROOT)}")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tcx_files = sorted(TCX_DIR.glob("activity_*.tcx"))
    if not tcx_files:
        print(f"No TCX files found in {TCX_DIR}")
        return

    for path in tcx_files:
        run = load_tcx(path)
        slug = slug_for(run)
        make_chart(run, OUT_DIR / f"{slug}-elev.png", thumb=False)
        make_chart(run, OUT_DIR / f"{slug}-elev-thumb.png", thumb=True)


if __name__ == "__main__":
    main()
