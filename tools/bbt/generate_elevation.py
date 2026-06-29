#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["requests", "requests-cache", "ruamel.yaml", "srtm.py", "matplotlib"]
# ///
"""
Generate elevation profile charts for each BBT segment.
Orange = covered portion, blue = not yet run.

Outputs (per segment):
  static/images/bbt/{slug}-elev.png        full-size (under segment map)
  static/images/bbt/{slug}-elev-thumb.png  thumbnail (summary table)

Usage:
    uv run tools/bbt/generate_elevation.py
"""

import math
import xml.etree.ElementTree as ET
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import requests
import requests_cache
import srtm
from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).parent.parent.parent
PAGE_PATH = REPO_ROOT / "content" / "report" / "adhoc" / "santa-monica-mountains-running.md"
GPX_DIR = Path.home() / "Documents" / "santa monica mountains running"
DATA_DIR = REPO_ROOT / "tools" / "bbt" / "data"
IMG_DIR = REPO_ROOT / "static" / "images" / "bbt"

OVERPASS_URL = "https://maps.mail.ru/osm/tools/overpass/api/interpreter"
BBT_THRESH_M = 50

SEGMENT_SPLITS = [
    ("Ray Miller TH",        34.0788, -119.0255),
    ("Danielson Ranch",      34.0753, -118.9200),
    ("Mishe Mokwa TH",       34.0805, -118.8505),
    ("Encinal Canyon Rd",    34.0815, -118.8200),
    ("Latigo Canyon Rd",     34.0820, -118.7910),
    ("Piuma TH",             34.0721, -118.7232),
    ("Saddle Peak",          34.0843, -118.6350),
    ("Trippet Ranch",        34.0857, -118.5998),
    ("Will Rogers SHP",      34.0540, -118.5245),
]

SEGMENT_SLUGS = [
    "01-ray-miller-to-danielson",
    "02-mishe-mokwa-to-danielson",
    "03-mishe-mokwa-to-encinal",
    "04-encinal-to-latigo",
    "05-latigo-to-piuma",
    "06-saddle-peak-to-piuma",
    "07-saddle-peak-to-trippet",
    "08-trippet-to-will-rogers",
]

COLOR_COVERED = "#ff6600"
COLOR_UNCOVERED = "#0066cc"


def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((lat2 - lat1) * math.pi / 360) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin((lon2 - lon1) * math.pi / 360) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def closest_idx(coords, lat, lon):
    return min(range(len(coords)), key=lambda i: haversine_m(coords[i][0], coords[i][1], lat, lon))


def build_bbt():
    query = "[out:json][timeout:120];relation(2748910);way(r);out geom;"
    r = requests.get(OVERPASS_URL, params={"data": query}, timeout=120)
    r.raise_for_status()
    ways = sorted(
        [e for e in r.json()["elements"] if e["type"] == "way"],
        key=lambda w: sum(p["lon"] for p in w["geometry"]) / len(w["geometry"])
                     if w.get("geometry") else 0,
        reverse=True,
    )
    bbt = []
    for w in ways:
        pts = [(p["lat"], p["lon"]) for p in w.get("geometry", [])]
        if not pts:
            continue
        if bbt:
            tail = bbt[-1]
            if haversine_m(tail[0], tail[1], pts[-1][0], pts[-1][1]) < \
               haversine_m(tail[0], tail[1], pts[0][0], pts[0][1]):
                pts = list(reversed(pts))
        bbt.extend(pts if not bbt else pts[1:])
    if bbt[0][1] < bbt[-1][1]:
        bbt.reverse()
    return bbt


def compute_covered_sets(bbt, seg_ranges, bbt_runs):
    ns = {"g": "http://www.topografix.com/GPX/1/1"}
    covered = [set() for _ in SEGMENT_SLUGS]
    for run in sorted(bbt_runs, key=lambda r: str(r.get("date", ""))):
        gid = str(run["garmin_id"])
        candidates = list(GPX_DIR.glob(f"activity_{gid}.gpx"))
        if not candidates:
            print(f"  GPX not found: {gid}, skipping")
            continue
        gpx_pts = [(float(p.get("lat")), float(p.get("lon")))
                   for p in ET.parse(candidates[0]).getroot().findall(".//g:trkpt", ns)]
        run_covered = {
            i for i, bp in enumerate(bbt)
            if min(haversine_m(bp[0], bp[1], gp[0], gp[1]) for gp in gpx_pts) <= BBT_THRESH_M
        }
        for seg_i in range(len(SEGMENT_SLUGS)):
            covered[seg_i] |= run_covered & seg_ranges[seg_i]
    return covered


def moving_avg(vals, window=11):
    n = len(vals)
    result = []
    for i in range(n):
        s, e = max(0, i - window // 2), min(n, i + window // 2 + 1)
        result.append(sum(vals[s:e]) / (e - s))
    return result


def make_chart(bbt, seg_idxs, covered_set, elev_data, out_path, thumb=False):
    # cumulative distance along segment (miles)
    dists = [0.0]
    for j in range(1, len(seg_idxs)):
        a, b = bbt[seg_idxs[j - 1]], bbt[seg_idxs[j]]
        dists.append(dists[-1] + haversine_m(a[0], a[1], b[0], b[1]) / 1609.344)

    # SRTM terrain elevation
    raw = []
    for idx in seg_idxs:
        lat, lon = bbt[idx]
        e = elev_data.get_elevation(lat, lon)
        raw.append(float(e) if e is not None else None)

    # fill None gaps by linear interpolation
    for j in range(len(raw)):
        if raw[j] is None:
            prev = next((raw[k] for k in range(j - 1, -1, -1) if raw[k] is not None), None)
            nxt = next((raw[k] for k in range(j + 1, len(raw)) if raw[k] is not None), None)
            if prev is not None and nxt is not None:
                raw[j] = (prev + nxt) / 2
            else:
                raw[j] = prev or nxt or 0.0

    elev_ft = [v * 3.28084 for v in moving_avg(raw, window=11)]
    covered_mask = [idx in covered_set for idx in seg_idxs]

    elev_min, elev_max = min(elev_ft), max(elev_ft)
    base = elev_min - (elev_max - elev_min) * 0.12

    if thumb:
        fig, ax = plt.subplots(figsize=(3.5, 0.9), dpi=100)
    else:
        fig, ax = plt.subplots(figsize=(9, 2.8), dpi=150)

    fig.patch.set_facecolor("white")
    ax.set_facecolor("#f9f9f9")

    # plot fill + line per contiguous color group; overlap by 1 pt to avoid gaps
    start = 0
    while start < len(seg_idxs):
        end = start + 1
        while end < len(covered_mask) and covered_mask[end] == covered_mask[start]:
            end += 1
        sl = slice(start, min(end + 1, len(dists)))
        color = COLOR_COVERED if covered_mask[start] else COLOR_UNCOVERED
        ax.fill_between(dists[sl], base, elev_ft[sl], alpha=0.5, color=color, linewidth=0)
        ax.plot(dists[sl], elev_ft[sl], color=color, linewidth=1.3 if not thumb else 0.9)
        start = end

    ax.set_xlim(0, dists[-1])
    ax.set_ylim(bottom=base)

    if thumb:
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
    else:
        ax.set_xlabel("miles", fontsize=8)
        ax.set_ylabel("elevation (ft)", fontsize=8)
        ax.tick_params(labelsize=7)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        legend = [
            Patch(facecolor=COLOR_COVERED, alpha=0.7, label="covered"),
            Patch(facecolor=COLOR_UNCOVERED, alpha=0.7, label="not yet"),
        ]
        ax.legend(handles=legend, fontsize=7, loc="upper right", framealpha=0.6)

    plt.tight_layout(pad=0.2 if thumb else 0.5)
    plt.savefig(out_path, bbox_inches="tight", facecolor="white")
    plt.close()


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    requests_cache.install_cache(str(DATA_DIR / "http_cache"), backend="sqlite", expire_after=-1)

    print("Loading BBT route (cached)...")
    bbt = build_bbt()
    print(f"  {len(bbt)} pts")

    split_idxs = sorted(
        [closest_idx(bbt, lat, lon) for _, lat, lon in SEGMENT_SPLITS], reverse=True
    )
    seg_ranges = [
        set(range(split_idxs[i + 1], split_idxs[i] + 1))
        for i in range(len(SEGMENT_SLUGS))
    ]

    text = PAGE_PATH.read_text()
    _, fm_text, _ = text.split("---", 2)
    yaml = YAML()
    data = yaml.load(fm_text)

    bbt_runs = [r for r in data.get("runs", []) if r.get("bbt")]
    print(f"\nComputing covered sets from {len(bbt_runs)} BBT run(s)...")
    covered_sets = compute_covered_sets(bbt, seg_ranges, bbt_runs)
    for seg_i, slug in enumerate(SEGMENT_SLUGS):
        print(f"  {slug}: {len(covered_sets[seg_i])} pts covered")

    print("\nLoading SRTM elevation data (downloads tiles on first run)...")
    elev_data = srtm.get_data()

    print("\nGenerating elevation charts...")
    for seg_i, slug in enumerate(SEGMENT_SLUGS):
        # descending BBT index = west→east traversal
        seg_idxs = sorted(seg_ranges[seg_i], reverse=True)
        covered = covered_sets[seg_i]

        full_path = IMG_DIR / f"{slug}-elev.png"
        make_chart(bbt, seg_idxs, covered, elev_data, full_path, thumb=False)
        print(f"  {slug}: {full_path.name}")

        thumb_path = IMG_DIR / f"{slug}-elev-thumb.png"
        make_chart(bbt, seg_idxs, covered, elev_data, thumb_path, thumb=True)
        print(f"  {slug}: {thumb_path.name}")

    print("\nDone.")


if __name__ == "__main__":
    main()
