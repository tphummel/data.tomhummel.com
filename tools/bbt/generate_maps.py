#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["staticmap", "requests", "requests-cache", "Pillow", "ruamel.yaml"]
# ///
"""
Generate static map images for each BBT segment plus an overview.
Outputs PNGs to static/images/bbt/ in the repo root.

BBT runs are read from the page front matter (runs where bbt: true).
Covered BBT sections render orange; uncovered render blue.

Usage:
    uv run tools/bbt/generate_maps.py
"""

import math
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
import requests_cache
from ruamel.yaml import YAML
from staticmap import StaticMap, Line, CircleMarker

REPO_ROOT = Path(__file__).parent.parent.parent
OUT_DIR = REPO_ROOT / "static" / "images" / "bbt"
GPX_DIR = Path.home() / "Documents" / "santa monica mountains running"
PAGE_PATH = REPO_ROOT / "content" / "report" / "adhoc" / "santa-monica-mountains-running.md"
DATA_DIR = REPO_ROOT / "tools" / "bbt" / "data"

OVERPASS_URL = "https://maps.mail.ru/osm/tools/overpass/api/interpreter"
BBT_RELATION_ID = 2748910
BBT_THRESH_M = 50  # metres — within this distance = on the BBT

# Duplicate/redundant road-crossing ways near the Trippet Ranch (Old Topanga Canyon
# Blvd / Greenleaf Canyon Rd) junction. The two "Backbone Trail"-named ways bookending
# this crossing already come within ~40m of each other directly; these extra relation
# members (a stub road spur plus a ~200m there-and-back down Topanga Canyon Blvd)
# make the naive longitude-sorted stitcher zigzag, showing as a stray line on maps.
EXCLUDED_WAY_IDS = {13340743, 122087883, 204589613, 1216972055}

TILE_URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
COLOR_COVERED = "#ff6600"   # orange — miles you've run on the BBT
COLOR_UNCOVERED = "#0066cc" # blue   — miles remaining

# Official NPS segment boundaries, west to east (Ray Miller = Seg 1, Will Rogers = Seg 8).
# Segments 1-2 share Danielson Ranch; 2-3 share Mishe Mokwa; 5-6 share Piuma; 6-7 share Saddle Peak.
# We use a single linear split for map purposes, treating each shared trailhead once.
SEGMENT_SPLITS = [
    ("Ray Miller TH",        34.0788, -119.0255),  # west terminus
    ("Danielson Ranch",      34.0753, -118.9200),
    ("Mishe Mokwa TH",       34.0805, -118.8505),
    ("Encinal Canyon Rd",    34.0815, -118.8200),
    ("Latigo Canyon Rd",     34.0820, -118.7910),
    ("Piuma TH",             34.0799, -118.7037),
    ("Saddle Peak",          34.0819, -118.6441),
    ("Trippet Ranch",        34.0934, -118.5878),
    ("Will Rogers SHP",      34.0540, -118.5245),  # east terminus
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
    # placeholder so len(SLUGS) == len(SPLITS)-1
]

DATA_DIR.mkdir(parents=True, exist_ok=True)
requests_cache.install_cache(
    str(DATA_DIR / "http_cache"), backend="sqlite", expire_after=-1
)


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((lat2 - lat1) * math.pi / 360) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin((lon2 - lon1) * math.pi / 360) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def closest_idx(coords, lat, lon):
    return min(range(len(coords)), key=lambda i: haversine_m(coords[i][0], coords[i][1], lat, lon))


def _best_zoom(lat_min, lat_max, lon_min, lon_max, width, height):
    def lon2tile(lon, z): return (lon + 180) / 360 * 2 ** z
    def lat2tile(lat, z): return (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * 2 ** z
    for z in range(15, 7, -1):
        if (lon2tile(lon_max, z) - lon2tile(lon_min, z)) * 256 <= width and \
           (lat2tile(lat_min, z) - lat2tile(lat_max, z)) * 256 <= height:
            return z
    return 9


# ---------------------------------------------------------------------------
# BBT route from OSM
# ---------------------------------------------------------------------------

def fetch_bbt_route():
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
    print(f"  {len(bbt)} coords, lon {bbt[0][1]:.3f} to {bbt[-1][1]:.3f}")
    return bbt


def split_route(bbt):
    # SEGMENT_SPLITS is ordered west→east (Ray Miller first, Will Rogers last).
    # BBT array is indexed east→west (bbt[0] = Will Rogers, bbt[-1] = Ray Miller).
    # closest_idx therefore returns high values for western splits and low for eastern.
    # We sort descending so idxs[0] = Ray Miller (highest) and idxs[-1] = Will Rogers (lowest),
    # then slice bbt[idxs[i+1]:idxs[i]+1] to get each segment west-to-east in NPS order.
    idxs = sorted([closest_idx(bbt, lat, lon) for _, lat, lon in SEGMENT_SPLITS], reverse=True)
    return [bbt[idxs[i + 1]:idxs[i] + 1] for i in range(len(idxs) - 1)]


# ---------------------------------------------------------------------------
# GPX loading — from page front matter
# ---------------------------------------------------------------------------

def load_page_bbt_gpx_ids():
    """Return garmin_ids (as strings) for all runs marked bbt: true in the page."""
    text = PAGE_PATH.read_text()
    _, fm_text, _ = text.split("---", 2)
    yaml = YAML()
    data = yaml.load(fm_text)
    ids = []
    for run in data.get("runs", []):
        if run.get("bbt"):
            gid = run.get("garmin_id")
            if gid:
                ids.append(str(gid))
    return ids


def load_gpx_coords(gpx_path):
    ns = {"g": "http://www.topografix.com/GPX/1/1"}
    root = ET.parse(gpx_path).getroot()
    return [(float(p.get("lat")), float(p.get("lon")))
            for p in root.findall(".//g:trkpt", ns)]


def load_all_bbt_gpx():
    """Load GPX tracks for all BBT runs listed in the page."""
    ids = load_page_bbt_gpx_ids()
    tracks = []
    for gid in ids:
        candidates = list(GPX_DIR.glob(f"activity_{gid}.gpx"))
        if candidates:
            tracks.append(load_gpx_coords(candidates[0]))
        else:
            print(f"  Warning: no GPX file found for garmin_id {gid}")
    return tracks


# ---------------------------------------------------------------------------
# Coverage coloring
# ---------------------------------------------------------------------------

def coverage_lines(seg_coords, all_gpx_tracks):
    """
    Split seg_coords into contiguous runs of covered/uncovered points.
    Returns list of (coords, color) — only the BBT route points, colored
    orange where any GPX track passes within BBT_THRESH_M, blue elsewhere.
    """
    if not all_gpx_tracks:
        return [(seg_coords, COLOR_UNCOVERED)]

    covered = []
    for bp in seg_coords:
        hit = any(
            any(haversine_m(bp[0], bp[1], gp[0], gp[1]) <= BBT_THRESH_M for gp in gpx)
            for gpx in all_gpx_tracks
        )
        covered.append(hit)

    lines = []
    i = 0
    while i < len(seg_coords):
        color = COLOR_COVERED if covered[i] else COLOR_UNCOVERED
        j = i + 1
        while j < len(seg_coords) and covered[j] == covered[i]:
            j += 1
        # Include one-point overlap at boundaries to avoid gaps
        end = min(j, len(seg_coords) - 1)
        lines.append((seg_coords[i:end + 1], color))
        i = j

    return lines


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render_map(colored_lines, output_path, width=1200, height=600, padding=0.05):
    """
    colored_lines: list of (coords, color_hex)
    coords: list of (lat, lon)
    """
    all_pts = [pt for coords, _ in colored_lines for pt in coords]
    lats = [p[0] for p in all_pts]
    lons = [p[1] for p in all_pts]
    lat_pad = (max(lats) - min(lats)) * padding + 0.01
    lon_pad = (max(lons) - min(lons)) * padding + 0.01

    m = StaticMap(width, height, url_template=TILE_URL)
    for coords, color in colored_lines:
        if len(coords) >= 2:
            m.add_line(Line([(lon, lat) for lat, lon in coords], color, 3))

    # Terminus markers at the ends of the first and last line
    first_pt = colored_lines[0][0][0]
    last_pt = colored_lines[-1][0][-1]
    m.add_marker(CircleMarker((first_pt[1], first_pt[0]), "#cc0000", 8))
    m.add_marker(CircleMarker((last_pt[1], last_pt[0]), "#cc0000", 8))

    center_lat = (min(lats) + max(lats)) / 2
    center_lon = (min(lons) + max(lons)) / 2
    zoom = _best_zoom(min(lats) - lat_pad, max(lats) + lat_pad,
                      min(lons) - lon_pad, max(lons) + lon_pad, width, height)
    image = m.render(zoom=zoom, center=[center_lon, center_lat])
    image.save(str(output_path))
    print(f"  Saved: {output_path.name}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    bbt = fetch_bbt_route()
    segments = split_route(bbt)
    all_gpx = load_all_bbt_gpx()
    print(f"BBT GPX tracks loaded: {len(all_gpx)}")
    print(f"Segments: {len(segments)}")

    # --- Overview ---
    print("\nRendering overview...")
    overview_lines = coverage_lines(bbt, all_gpx)
    render_map(overview_lines, OUT_DIR / "00-overview.png", width=1300, height=500)

    # --- Per-segment ---
    for i, (seg_coords, slug) in enumerate(zip(segments, SEGMENT_SLUGS)):
        print(f"\nRendering {slug} ({len(seg_coords)} pts)")
        lines = coverage_lines(seg_coords, all_gpx)
        render_map(lines, OUT_DIR / f"{slug}.png", width=900, height=500)


if __name__ == "__main__":
    main()
