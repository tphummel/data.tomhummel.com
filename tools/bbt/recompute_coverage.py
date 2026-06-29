#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["requests", "requests-cache", "ruamel.yaml"]
# ///
"""
Force-recompute all BBT segment coverage from scratch using current split points.
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


def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((lat2-lat1)*math.pi/360)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin((lon2-lon1)*math.pi/360)**2
    return 2*R*math.asin(math.sqrt(a))


def seg_len_m(coords):
    return sum(haversine_m(coords[i][0], coords[i][1], coords[i+1][0], coords[i+1][1])
               for i in range(len(coords)-1))


def closest_idx(coords, lat, lon):
    return min(range(len(coords)), key=lambda i: haversine_m(coords[i][0], coords[i][1], lat, lon))


def build_bbt():
    query = f"[out:json][timeout:120];relation(2748910);way(r);out geom;"
    r = requests.get(OVERPASS_URL, params={"data": query}, timeout=120)
    r.raise_for_status()
    ways = sorted(
        [e for e in r.json()["elements"] if e["type"]=="way"],
        key=lambda w: sum(p["lon"] for p in w["geometry"])/len(w["geometry"])
                     if w.get("geometry") else 0,
        reverse=True,
    )
    bbt = []
    for w in ways:
        pts = [(p["lat"], p["lon"]) for p in w.get("geometry", [])]
        if not pts: continue
        if bbt:
            tail = bbt[-1]
            if haversine_m(tail[0],tail[1],pts[-1][0],pts[-1][1]) < \
               haversine_m(tail[0],tail[1],pts[0][0],pts[0][1]):
                pts = list(reversed(pts))
        bbt.extend(pts if not bbt else pts[1:])
    if bbt[0][1] < bbt[-1][1]:
        bbt.reverse()
    return bbt


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    requests_cache.install_cache(str(DATA_DIR/"http_cache"), backend="sqlite", expire_after=-1)

    print("Loading BBT route (cached)...")
    bbt = build_bbt()
    print(f"  {len(bbt)} pts")

    split_idxs = sorted([closest_idx(bbt, lat, lon) for _, lat, lon in SEGMENT_SPLITS], reverse=True)

    text = PAGE_PATH.read_text()
    _, fm_text, body = text.split("---", 2)
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    data = yaml.load(fm_text)

    bbt_runs = [r for r in data.get("runs", []) if r.get("bbt")]
    print(f"\nLoading {len(bbt_runs)} BBT track(s)...")
    ns = {"g": "http://www.topografix.com/GPX/1/1"}
    all_gpx = []
    for r in bbt_runs:
        gid = str(r["garmin_id"])
        candidates = list(GPX_DIR.glob(f"activity_{gid}.gpx"))
        if candidates:
            pts = [(float(p.get("lat")), float(p.get("lon")))
                   for p in ET.parse(candidates[0]).getroot().findall(".//g:trkpt", ns)]
            all_gpx.append(pts)
            print(f"  {r['date']} {gid}: {len(pts)} pts")
        else:
            print(f"  {r['date']} {gid}: GPX not found, skipping")

    print("\nComputing coverage...")
    covered = [
        any(min(haversine_m(bp[0],bp[1],gp[0],gp[1]) for gp in gpx) <= BBT_THRESH_M
            for gpx in all_gpx)
        for bp in bbt
    ]

    for seg_i, slug in enumerate(SEGMENT_SLUGS):
        e = split_idxs[seg_i]
        s = split_idxs[seg_i + 1]
        seg_pts = bbt[s:e+1]
        seg_flags = covered[s:e+1]

        total = 0.0
        span = []
        for pt, flag in zip(seg_pts, seg_flags):
            if flag:
                span.append(pt)
            elif span:
                if len(span) > 1:
                    total += seg_len_m(span)
                span = []
        if len(span) > 1:
            total += seg_len_m(span)
        miles = round(total / 1609.344, 2)

        seg_data = next((s for s in data["bbt_segments"] if s["slug"] == slug), None)
        if seg_data is None:
            continue
        old = seg_data.get("miles_covered", 0)
        seg_data["miles_covered"] = miles
        seg_data["touched"] = miles > 0
        print(f"  {slug}: {old} -> {miles} mi {'✓' if miles > 0 else ''}")

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
