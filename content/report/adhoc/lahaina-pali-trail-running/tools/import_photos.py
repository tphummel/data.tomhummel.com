#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pillow", "pillow-heif", "ruamel.yaml"]
# ///
"""
Import geotagged photos into the Lahaina Pali Trail page: reads GPS +
DateTimeOriginal from each photo's EXIF, matches it to the run it was taken
on (by date), converts it to a web-friendly JPEG, and writes a `photos:`
entry into the page front matter.

Drop photos (HEIC or JPEG, with GPS + timestamp intact) in the source
directory, then run:
    uv run content/report/adhoc/lahaina-pali-trail-running/tools/import_photos.py

A note on GPS/timestamp survival: chat upload pipelines commonly strip EXIF
from individual image uploads. Zipping the originals first (e.g. iOS Files
app > Select > Compress, after confirming "Location" is on in the share
sheet) tends to preserve it, since the archive isn't re-encoded the way a
single image is.
"""

import sys
from datetime import datetime, timedelta, timezone
from fractions import Fraction
from pathlib import Path

import pillow_heif
from PIL import Image, ImageOps
from ruamel.yaml import YAML

pillow_heif.register_heif_opener()

sys.path.insert(0, str(Path(__file__).parent))
from lib import load_tcx  # noqa: E402

HST_OFFSET = timedelta(hours=-10)  # Hawaii Standard Time, no DST

BUNDLE_DIR = Path(__file__).parent.parent  # content/report/adhoc/lahaina-pali-trail-running/
PAGE_PATH = BUNDLE_DIR / "index.md"
OUT_DIR = BUNDLE_DIR / "images" / "photos"
SOURCE_DIR = Path.home() / "Documents" / "lahaina pali trail running" / "photos"
TCX_DIR = Path.home() / "Documents" / "lahaina pali trail running"

MAX_DIMENSION = 1600
GPS_IFD, EXIF_IFD = 0x8825, 0x8769
DATETIME_ORIGINAL_TAG = 36867


def dms_to_decimal(dms, ref):
    deg, minute, sec = (float(Fraction(v)) for v in dms)
    value = deg + minute / 60 + sec / 3600
    return -value if ref in ("S", "W") else value


def read_exif(path):
    img = Image.open(path)
    exif = img.getexif()
    gps = exif.get_ifd(GPS_IFD)
    exif_ifd = exif.get_ifd(EXIF_IFD)
    if not gps or 2 not in gps or 4 not in gps:
        return None

    lat = dms_to_decimal(gps[2], gps.get(1, "N"))
    lon = dms_to_decimal(gps[4], gps.get(3, "E"))
    elev_m = float(gps[6]) if 6 in gps else None

    dt_raw = exif_ifd.get(DATETIME_ORIGINAL_TAG)
    taken_at = datetime.strptime(dt_raw, "%Y:%m:%d %H:%M:%S") if dt_raw else None

    return img, lat, lon, elev_m, taken_at


def match_run(taken_at, runs_by_date):
    if taken_at is None:
        return None
    return runs_by_date.get(taken_at.strftime("%Y-%m-%d"))


def nearest_mile(tcx, taken_at):
    """Distance along the matched run's own track at the photo's timestamp.

    Matched by time rather than nearest GPS point: this trail is an
    out-and-back, so the start and turnaround-adjacent points can sit only
    meters apart from points recorded much later (or earlier) in the same
    run, and a spatial nearest-neighbor search can't tell those apart.
    Every trackpoint has its own timestamp, so matching on time is
    unambiguous.
    """
    taken_at_utc = taken_at.replace(tzinfo=timezone.utc) - HST_OFFSET
    pts = tcx["points"]
    idx = min(
        range(len(pts)),
        key=lambda i: abs(datetime.fromisoformat(pts[i]["time"].replace("Z", "+00:00")) - taken_at_utc),
    )
    return round(pts[idx]["dist_m"] / 1609.344, 2)


def load_page():
    text = PAGE_PATH.read_text()
    _, fm_text, body = text.split("---", 2)
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    data = yaml.load(fm_text)
    return data, body


def save_page(data, body):
    import io
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    yaml.default_flow_style = False
    stream = io.StringIO()
    yaml.dump(data, stream)
    PAGE_PATH.write_text(f"---\n{stream.getvalue()}---{body}")


def save_web_jpeg(img, out_path):
    img = ImageOps.exif_transpose(img)  # bake in orientation; we're stripping EXIF
    img.thumbnail((MAX_DIMENSION, MAX_DIMENSION))
    img.convert("RGB").save(out_path, "JPEG", quality=85)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    data, body = load_page()
    existing_files = {p["file"] for p in data.get("photos", [])}

    runs_by_date = {r["date"]: r for r in data.get("runs", [])}
    tcx_by_trailhead = {}
    for path in TCX_DIR.glob("activity_*.tcx"):
        tcx = load_tcx(path)
        tcx_by_trailhead[tcx["trailhead"]] = tcx

    source_files = sorted(
        p for p in SOURCE_DIR.iterdir()
        if p.suffix.lower() in (".heic", ".heif", ".jpg", ".jpeg")
    )
    new_files = [p for p in source_files if f"{p.stem.lower()}.jpg" not in existing_files]

    if not new_files:
        print("No new photos found. Nothing to do.")
        return

    photos = list(data.get("photos", []))
    print(f"Found {len(new_files)} new photo(s):")
    for path in new_files:
        result = read_exif(path)
        if result is None:
            print(f"  {path.name}: no GPS data, skipping")
            continue
        img, lat, lon, elev_m, taken_at = result

        run = match_run(taken_at, runs_by_date)
        trailhead = run["trailhead"] if run else None
        tcx = tcx_by_trailhead.get(trailhead)
        mile = nearest_mile(tcx, taken_at) if tcx and taken_at else None

        out_name = f"{path.stem.lower()}.jpg"
        save_web_jpeg(img, OUT_DIR / out_name)

        entry = {
            "file": out_name,
            "taken_at": taken_at.strftime("%Y-%m-%dT%H:%M:%S-10:00") if taken_at else None,
            "lat": round(lat, 5),
            "lon": round(lon, 5),
            "elev_ft": int(round(elev_m * 3.28084)) if elev_m is not None else None,
            "trailhead": trailhead,
            "mile": mile,
            "caption": "",
        }
        photos.append(entry)
        print(f"  {path.name} -> {out_name}  {entry['taken_at']}  "
              f"{lat:.5f},{lon:.5f}  {entry['elev_ft']} ft  mile {mile} ({trailhead})")

    photos.sort(key=lambda p: p.get("taken_at") or "")
    data["photos"] = photos

    save_page(data, body)
    print(f"\nUpdated: {PAGE_PATH.relative_to(BUNDLE_DIR)}")
    print(f"  {len(new_files)} photo(s) added — fill in `caption:` for each in index.md")


if __name__ == "__main__":
    main()
