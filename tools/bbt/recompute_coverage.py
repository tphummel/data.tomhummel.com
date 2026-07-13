#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["requests", "requests-cache", "ruamel.yaml"]
# ///
"""
Force-recompute all BBT segment coverage from scratch using current split points.
Produces per-run-per-segment miles (this run on segment) and new miles (first time).
Run this after changing SEGMENT_SPLITS.
"""

import io
import math
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
import requests_cache
from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).parent.parent.parent
PAGE_PATH = REPO_ROOT / "content" / "report" / "adhoc" / "santa-monica-mountains-running.md"
GPX_DIR = Path.home() / "Documents" / "santa monica mountains running"
DATA_DIR = REPO_ROOT / "tools" / "bbt" / "data"

OVERPASS_URL = "https://maps.mail.ru/osm/tools/overpass/api/interpreter"
BBT_THRESH_M = 50

# Duplicate/redundant road-crossing ways near the Trippet Ranch (Old Topanga Canyon
# Blvd / Greenleaf Canyon Rd) junction. The two "Backbone Trail"-named ways bookending
# this crossing already come within ~40m of each other directly; these extra relation
# members (a stub road spur plus a ~200m there-and-back down Topanga Canyon Blvd)
# make the naive longitude-sorted stitcher zigzag, showing as a stray line on maps.
EXCLUDED_WAY_IDS = {13340743, 122087883, 204589613, 1216972055}

SEGMENT_SPLITS = [
    ("Ray Miller TH",        34.0788, -119.0255),
    ("Danielson Ranch",      34.0753, -118.9200),
    ("Mishe Mokwa TH",       34.0805, -118.8505),
    ("Encinal Canyon Rd",    34.0815, -118.8200),
    ("Latigo Canyon Rd",     34.0820, -118.7910),
    ("Piuma TH",             34.0799, -118.7037),
    ("Saddle Peak",          34.0819, -118.6441),
    ("Trippet Ranch",        34.0934, -118.5878),
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


def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((lat2 - lat1) * math.pi / 360) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin((lon2 - lon1) * math.pi / 360) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def seg_len_m(coords):
    return sum(haversine_m(coords[i][0], coords[i][1], coords[i+1][0], coords[i+1][1])
               for i in range(len(coords) - 1))


def closest_idx(coords, lat, lon):
    return min(range(len(coords)), key=lambda i: haversine_m(coords[i][0], coords[i][1], lat, lon))


def miles_from_index_set(indices, bbt):
    """Sum trail distance for a set of BBT point indices, grouping contiguous runs."""
    if not indices:
        return 0.0
    sorted_idxs = sorted(indices)
    total = 0.0
    span = [sorted_idxs[0]]
    for i in sorted_idxs[1:]:
        if i == span[-1] + 1:
            span.append(i)
        else:
            if len(span) > 1:
                total += seg_len_m([bbt[j] for j in span])
            span = [i]
    if len(span) > 1:
        total += seg_len_m([bbt[j] for j in span])
    return round(total / 1609.344, 2)


def build_bbt():
    query = "[out:json][timeout:120];relation(2748910);way(r);out geom;"
    r = requests.get(OVERPASS_URL, params={"data": query}, timeout=120)
    r.raise_for_status()
    ways = sorted(
        [e for e in r.json()["elements"] if e["type"] == "way"
         and "School Trail" not in e.get("tags", {}).get("name", "")
         and e.get("id") not in EXCLUDED_WAY_IDS],
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


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    requests_cache.install_cache(str(DATA_DIR / "http_cache"), backend="sqlite", expire_after=-1)

    print("Loading BBT route (cached)...")
    bbt = build_bbt()
    print(f"  {len(bbt)} pts")

    split_idxs = sorted(
        [closest_idx(bbt, lat, lon) for _, lat, lon in SEGMENT_SPLITS], reverse=True
    )
    # seg_ranges[i] = set of bbt indices belonging to segment i
    seg_ranges = [
        set(range(split_idxs[i + 1], split_idxs[i] + 1))
        for i in range(len(SEGMENT_SLUGS))
    ]

    text = PAGE_PATH.read_text()
    _, fm_text, body = text.split("---", 2)
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    data = yaml.load(fm_text)

    bbt_runs = sorted(
        [r for r in data.get("runs", []) if r.get("bbt")],
        key=lambda r: str(r.get("date", "")),
    )
    print(f"\nProcessing {len(bbt_runs)} BBT track(s) chronologically...")

    ns = {"g": "http://www.topografix.com/GPX/1/1"}
    ELEV_THRESH_M = 11.0

    # per-segment: set of already-covered bbt indices (for new-miles tracking)
    seg_already_covered = [set() for _ in SEGMENT_SLUGS]
    # per-segment: list of run dicts to store
    seg_run_entries = [[] for _ in SEGMENT_SLUGS]
    # bbt_idx -> (best_dist_m, elev_m) — populated from GPX elevation data
    bbt_elev = {}

    for run in bbt_runs:
        gid = str(run["garmin_id"])
        candidates = list(GPX_DIR.glob(f"activity_{gid}.gpx"))
        if not candidates:
            print(f"  {run['date']} {gid}: GPX not found, skipping")
            continue

        trkpts = ET.parse(candidates[0]).getroot().findall(".//g:trkpt", ns)
        gpx_pts = [(float(p.get("lat")), float(p.get("lon"))) for p in trkpts]
        gpx_elevs = [
            float(p.find("g:ele", ns).text) if p.find("g:ele", ns) is not None else None
            for p in trkpts
        ]

        # BBT indices covered by this run
        covered_by_run = {
            i for i, bp in enumerate(bbt)
            if min(haversine_m(bp[0], bp[1], gp[0], gp[1]) for gp in gpx_pts) <= BBT_THRESH_M
        }

        # Update bbt_elev for covered indices using nearest GPX point with elevation
        for i in covered_by_run:
            bp = bbt[i]
            for gp, ge in zip(gpx_pts, gpx_elevs):
                if ge is None:
                    continue
                d = haversine_m(bp[0], bp[1], gp[0], gp[1])
                if d <= BBT_THRESH_M and (i not in bbt_elev or d < bbt_elev[i][0]):
                    bbt_elev[i] = (d, ge)

        touched_any = False
        for seg_i, slug in enumerate(SEGMENT_SLUGS):
            in_seg = covered_by_run & seg_ranges[seg_i]
            if not in_seg:
                continue
            new_in_seg = in_seg - seg_already_covered[seg_i]
            miles_this_seg = miles_from_index_set(in_seg, bbt)
            miles_overlap = miles_from_index_set(in_seg & seg_already_covered[seg_i], bbt)
            miles_new = round(miles_this_seg - miles_overlap, 2)
            seg_already_covered[seg_i] |= in_seg
            seg_run_entries[seg_i].append({
                "garmin_id": run["garmin_id"],
                "date": run["date"],
                "miles_this_seg": miles_this_seg,
                "miles_new": miles_new,
            })
            touched_any = True
            print(f"  {run['date']} {gid} → {slug}: {miles_this_seg} mi ({miles_new} new)")

        if not touched_any:
            print(f"  {run['date']} {gid}: no BBT overlap")

    def compute_seg_elev_gain(covered_idxs):
        sorted_idxs = sorted(covered_idxs)
        elevs = [bbt_elev[i][1] for i in sorted_idxs if i in bbt_elev]
        if len(elevs) < 2:
            return 0
        gain_m = 0.0
        last = elevs[0]
        for e in elevs[1:]:
            d = e - last
            if d > ELEV_THRESH_M:
                gain_m += d
                last = e
            elif d < -ELEV_THRESH_M:
                last = e
        return int(round(gain_m * 3.28084))

    # Write results back to bbt_segments
    print("\nUpdating segments...")
    for seg_data in data.get("bbt_segments", []):
        slug = seg_data.get("slug")
        try:
            seg_i = SEGMENT_SLUGS.index(slug)
        except ValueError:
            continue

        run_entries = seg_run_entries[seg_i]
        total_covered = miles_from_index_set(seg_already_covered[seg_i], bbt)
        total_seg = miles_from_index_set(seg_ranges[seg_i], bbt)
        elev_gain = compute_seg_elev_gain(seg_already_covered[seg_i]) if seg_already_covered[seg_i] else None

        old = seg_data.get("miles_covered", 0)
        seg_data["miles_approx"] = round(total_seg, 1)
        seg_data["miles_covered"] = total_covered
        seg_data["touched"] = total_covered > 0
        seg_data["elev_gain_ft"] = elev_gain
        # Replace date/garmin_id with runs list
        seg_data.pop("date", None)
        seg_data.pop("garmin_id", None)
        seg_data["runs"] = run_entries
        print(f"  {slug}: {old} -> {total_covered} / {total_seg:.1f} mi, elev +{elev_gain} ft, {len(run_entries)} run(s)")

    yaml2 = YAML()
    yaml2.preserve_quotes = True
    yaml2.width = 4096
    yaml2.default_flow_style = False
    stream = io.StringIO()
    yaml2.dump(data, stream)
    PAGE_PATH.write_text(f"---\n{stream.getvalue()}---{body}")
    print("\nSaved.")


if __name__ == "__main__":
    main()
