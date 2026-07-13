#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["requests", "requests-cache", "ruamel.yaml", "Pillow"]
# ///
"""
Sync new GPX files from ~/Documents/santa monica mountains running into the
SMM running page, check BBT overlap, and regenerate maps if needed.

Drop a new GPX file in the source directory, then run:
    uv run tools/bbt/sync.py
"""

import io
import math
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
import requests_cache
from ruamel.yaml import YAML

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent.parent
PAGE_PATH = REPO_ROOT / "content" / "report" / "adhoc" / "santa-monica-mountains-running.md"
GPX_DIR = Path.home() / "Documents" / "santa monica mountains running"
DATA_DIR = REPO_ROOT / "tools" / "bbt" / "data"

OVERPASS_URL = "https://maps.mail.ru/osm/tools/overpass/api/interpreter"
BBT_RELATION_ID = 2748910
BBT_THRESH_M = 50  # within 50 m = "on the BBT"

# Duplicate/redundant road-crossing ways near the Trippet Ranch (Old Topanga Canyon
# Blvd / Greenleaf Canyon Rd) junction. The two "Backbone Trail"-named ways bookending
# this crossing already come within ~40m of each other directly; these extra relation
# members (a stub road spur plus a ~200m there-and-back down Topanga Canyon Blvd)
# make the naive longitude-sorted stitcher zigzag, showing as a stray line on maps.
EXCLUDED_WAY_IDS = {13340743, 122087883, 204589613, 1216972055}

# Approximate segment boundary coords (east to west).
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

AREA_KEYWORDS = {
    "sullivan-mandeville": ["sullivan", "mandeville", "westridge", "west ridge", "bayliss"],
    "topanga":             ["topanga", "trippet", "dead horse", "eagle rock"],
    "temescal":            ["temescal"],
    "malibu-creek":        ["malibu creek", "las virgenes", "malibu sp"],
    "mulholland":          ["mulholland", "eagle junction", "marvin braude", "nike missile"],
    "beaches":             ["oceanfront", "beach", "pch", "malibu half", "half marathon"],
    "bbt":                 ["backbone", "latigo", "kanan", "etz meloy", "encinal",
                            "yerba buena", "circle x", "danielson", "la jolla valley",
                            "ray miller", "point mugu", "corral canyon", "castro"],
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((lat2 - lat1) * math.pi / 360) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin((lon2 - lon1) * math.pi / 360) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def seg_len_m(coords):
    return sum(haversine_m(coords[i][0], coords[i][1], coords[i+1][0], coords[i+1][1])
               for i in range(len(coords) - 1))


def load_gpx(path):
    ns = {"g": "http://www.topografix.com/GPX/1/1"}
    root = ET.parse(path).getroot()
    pts = [(float(p.get("lat")), float(p.get("lon")))
           for p in root.findall(".//g:trkpt", ns)]
    name_el = root.find(".//g:name", ns)
    name = name_el.text.strip() if name_el is not None else path.stem
    time_el = root.find(".//g:time", ns)
    date = time_el.text[:10] if time_el is not None else "unknown"
    return pts, name, date


def gpx_stats(pts):
    """Returns (miles, elev_gain_ft)."""
    dist_m = seg_len_m(pts)
    elevs = []
    # Re-parse for elevation (not in pts tuple)
    return dist_m / 1609.344, None  # elevation handled separately


def load_gpx_full(path):
    ns = {"g": "http://www.topografix.com/GPX/1/1"}
    root = ET.parse(path).getroot()
    trkpts = root.findall(".//g:trkpt", ns)
    pts = [(float(p.get("lat")), float(p.get("lon"))) for p in trkpts]
    elevs = []
    for p in trkpts:
        el = p.find("g:ele", ns)
        if el is not None:
            elevs.append(float(el.text))

    name_el = root.find(".//g:name", ns)
    name = name_el.text.strip() if name_el is not None else path.stem
    time_el = root.find(".//g:time", ns)
    date = time_el.text[:10] if time_el is not None else "unknown"

    dist_mi = seg_len_m(pts) / 1609.344
    # 11m threshold matches Garmin Connect's smoothed elevation (filters GPS noise)
    gain_m = loss_m = 0.0
    last = elevs[0] if elevs else 0.0
    for e in elevs[1:]:
        d = e - last
        if d > 11:
            gain_m += d; last = e
        elif d < -11:
            loss_m += abs(d); last = e

    return pts, name, date, round(dist_mi, 1), int(round(gain_m * 3.28084)), int(round(loss_m * 3.28084))


def classify_area(name):
    lower = name.lower()
    for area, keywords in AREA_KEYWORDS.items():
        if any(kw in lower for kw in keywords):
            return area, True  # (area, is_auto)
    return "other", False


def garmin_id_from_path(path):
    stem = path.stem  # e.g. "activity_12345678"
    parts = stem.split("_")
    return parts[-1] if len(parts) >= 2 else stem


# ---------------------------------------------------------------------------
# BBT route (cached via requests-cache)
# ---------------------------------------------------------------------------

def build_bbt_route():
    print("Loading BBT route from OSM (cached)...")
    query = f"[out:json][timeout:120];relation({BBT_RELATION_ID});way(r);out geom;"
    r = requests.get(OVERPASS_URL, params={"data": query}, timeout=120)
    r.raise_for_status()
    ways = sorted(
        [e for e in r.json()["elements"] if e["type"] == "way"
         and "School Trail" not in e.get("tags", {}).get("name", "")
         and e.get("id") not in EXCLUDED_WAY_IDS],
        key=lambda w: sum(pt["lon"] for pt in w["geometry"]) / len(w["geometry"])
                     if w.get("geometry") else 0,
        reverse=True,
    )
    bbt = []
    for w in ways:
        pts = [(pt["lat"], pt["lon"]) for pt in w.get("geometry", [])]
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


def bbt_touched_by_gpx(bbt, gpx_pts):
    """Returns list of slugs where a single GPX track passes within threshold."""
    split_idxs = sorted([closest_idx(bbt, lat, lon) for _, lat, lon in SEGMENT_SPLITS], reverse=True)
    seg_ranges = [set(range(split_idxs[i + 1], split_idxs[i] + 1)) for i in range(len(SEGMENT_SLUGS))]
    covered = {i for i, bp in enumerate(bbt)
               if min(haversine_m(bp[0], bp[1], gp[0], gp[1]) for gp in gpx_pts) <= BBT_THRESH_M}
    return [slug for seg_i, slug in enumerate(SEGMENT_SLUGS) if covered & seg_ranges[seg_i]]


def recompute_all_segment_coverage(bbt, all_bbt_runs):
    """
    Process all BBT runs chronologically, computing per-run-per-segment coverage.
    Returns dict: slug -> {miles_covered, runs: [{garmin_id, date, miles_this_seg, miles_new}]}
    """
    split_idxs = sorted([closest_idx(bbt, lat, lon) for _, lat, lon in SEGMENT_SPLITS], reverse=True)
    seg_ranges = [set(range(split_idxs[i + 1], split_idxs[i] + 1)) for i in range(len(SEGMENT_SLUGS))]

    seg_already_covered = [set() for _ in SEGMENT_SLUGS]
    seg_run_entries = [[] for _ in SEGMENT_SLUGS]

    ns = {"g": "http://www.topografix.com/GPX/1/1"}
    for run in sorted(all_bbt_runs, key=lambda r: str(r.get("date", ""))):
        gid = str(run.get("garmin_id", ""))
        candidates = list(GPX_DIR.glob(f"activity_{gid}.gpx"))
        if not candidates:
            continue
        gpx_pts = [(float(p.get("lat")), float(p.get("lon")))
                   for p in ET.parse(candidates[0]).getroot().findall(".//g:trkpt", ns)]
        covered_by_run = {
            i for i, bp in enumerate(bbt)
            if min(haversine_m(bp[0], bp[1], gp[0], gp[1]) for gp in gpx_pts) <= BBT_THRESH_M
        }
        for seg_i, slug in enumerate(SEGMENT_SLUGS):
            in_seg = covered_by_run & seg_ranges[seg_i]
            if not in_seg:
                continue
            new_in_seg = in_seg - seg_already_covered[seg_i]
            miles_this_seg = miles_from_index_set(in_seg, bbt)
            miles_overlap = miles_from_index_set(in_seg & seg_already_covered[seg_i], bbt)
            seg_run_entries[seg_i].append({
                "garmin_id": run["garmin_id"],
                "date": run["date"],
                "miles_this_seg": miles_this_seg,
                "miles_new": round(miles_this_seg - miles_overlap, 2),
            })
            seg_already_covered[seg_i] |= in_seg

    return {
        slug: {
            "miles_covered": miles_from_index_set(seg_already_covered[seg_i], bbt),
            "runs": seg_run_entries[seg_i],
        }
        for seg_i, slug in enumerate(SEGMENT_SLUGS)
    }


# ---------------------------------------------------------------------------
# Markdown / YAML I/O
# ---------------------------------------------------------------------------

def load_page():
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


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    requests_cache.install_cache(
        str(DATA_DIR / "http_cache"), backend="sqlite", expire_after=-1
    )

    # --- Load current page state ---
    data, body = load_page()
    existing_ids = {str(run.get("garmin_id", "")) for run in data.get("runs", [])}

    # --- Find new GPX files ---
    gpx_files = sorted(GPX_DIR.glob("activity_*.gpx"))
    new_files = [f for f in gpx_files if garmin_id_from_path(f) not in existing_ids]

    if not new_files:
        print("No new GPX files found. Nothing to do.")
        return

    print(f"Found {len(new_files)} new GPX file(s):")

    bbt = None  # lazy-load
    any_bbt = False
    new_runs = []

    for gpx_path in new_files:
        gid = garmin_id_from_path(gpx_path)
        pts, name, date, miles, elev_gain_ft, elev_loss_ft = load_gpx_full(gpx_path)
        area, is_auto = classify_area(name)

        auto_tag = " (auto)" if is_auto else " (needs review)"
        print(f"\n  {gpx_path.name}")
        print(f"    {date}  \"{name}\"  {miles} mi  +{elev_gain_ft:,} ft / -{elev_loss_ft:,} ft")
        print(f"    area: {area}{auto_tag}")

        # BBT check — always run proximity test regardless of area classification
        if bbt is None:
            bbt = build_bbt_route()
        touched_slugs = bbt_touched_by_gpx(bbt, pts)
        bbt_flag = bool(touched_slugs)
        if bbt_flag:
            any_bbt = True
            if area not in ("bbt",):
                area = area  # keep original area; bbt: true flag is sufficient
            print(f"    BBT: YES — touches {', '.join(touched_slugs)}")
        else:
            print(f"    BBT: no overlap detected")

        run_entry = {
            "date": date,
            "name": name,
            "area": area,
            "miles": miles,
            "elev_gain_ft": elev_gain_ft,
            "elev_loss_ft": elev_loss_ft,
            "garmin_id": int(gid) if gid.isdigit() else gid,
            "bbt": bbt_flag,
            "notes": "",
        }
        new_runs.append(run_entry)

    # --- Apply run entries to data ---
    runs = list(data.get("runs", []))
    for run_entry in new_runs:
        runs.append(run_entry)

    # --- Recompute segment coverage from scratch using ALL BBT tracks ---
    if any_bbt:
        if bbt is None:
            bbt = build_bbt_route()
        all_bbt_runs = [r for r in runs if r.get("bbt")]
        print(f"\nRecomputing coverage from {len(all_bbt_runs)} BBT track(s)...")
        coverage = recompute_all_segment_coverage(bbt, all_bbt_runs)

        for seg in data.get("bbt_segments", []):
            slug = seg.get("slug")
            if slug not in coverage:
                continue
            result = coverage[slug]
            new_mi = result["miles_covered"]
            old_mi = seg.get("miles_covered", 0)
            seg["miles_covered"] = new_mi
            seg["touched"] = new_mi > 0
            seg.pop("date", None)
            seg.pop("garmin_id", None)
            seg["runs"] = result["runs"]
            if new_mi != old_mi:
                print(f"  {seg['name']}: {old_mi} -> {new_mi} mi ({len(result['runs'])} run(s))")

    # Sort runs chronologically
    runs.sort(key=lambda r: str(r.get("date", "")))
    data["runs"] = runs

    # --- Save ---
    save_page(data, body)
    print(f"\nUpdated: {PAGE_PATH.relative_to(REPO_ROOT)}")
    print(f"  {len(new_runs)} run(s) added")

    # --- Regenerate maps if any BBT runs ---
    if any_bbt:
        print("\nRegenerating BBT maps...")
        result = subprocess.run(
            ["uv", "run", str(REPO_ROOT / "tools" / "bbt" / "generate_maps.py")],
            cwd=REPO_ROOT,
        )
        if result.returncode != 0:
            print("  Warning: map generation failed.")
        else:
            print("  Maps updated.")

    print("\nDone. Review area/notes fields, then git commit.")


if __name__ == "__main__":
    main()
