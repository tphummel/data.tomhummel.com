"""Shared TCX parsing helpers for the Lahaina Pali Trail running page."""

import io
import math
import xml.etree.ElementTree as ET

from PIL import Image

NS = {"t": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"}

# Real recorded start coordinates from the first run at each end, used to
# classify which trailhead a new activity started from. The two ends of this
# point-to-point trail are ~5.5 miles apart, so a coarse proximity check is
# plenty.
TRAILHEADS = {
    "east": {
        "label": "Māʻalaea (East) Trailhead",
        "lat": 20.80737,
        "lon": -156.51289,
    },
    "west": {
        "label": "Ukumehame (West) Trailhead",
        "lat": 20.79196,
        "lon": -156.56380,
    },
}

ELEV_GAIN_LOSS_THRESHOLD_M = 3  # filters GPS/barometer noise


def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((lat2 - lat1) * math.pi / 360) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin((lon2 - lon1) * math.pi / 360) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def load_tcx(path):
    """Parse a Garmin TCX export into trackpoints + laps.

    Returns dict with keys: garmin_id, date, trailhead, points, laps
    points: list of dicts {time, lat, lon, elev_m, dist_m, hr, speed_mps}
    laps: list of dicts {start_time, distance_m, time_s, calories, avg_hr, max_hr}
    """
    root = ET.parse(path).getroot()
    act = root.find(".//t:Activity", NS)

    act_id_el = act.find("t:Id", NS)
    start_time = act_id_el.text if act_id_el is not None else None

    points = []
    for tp in act.findall(".//t:Trackpoint", NS):
        pos = tp.find("t:Position", NS)
        if pos is None:
            continue
        time_el = tp.find("t:Time", NS)
        alt_el = tp.find("t:AltitudeMeters", NS)
        dist_el = tp.find("t:DistanceMeters", NS)
        hr_el = tp.find("t:HeartRateBpm/t:Value", NS)
        speed_el = tp.find("t:Extensions/t:TPX/t:Speed", NS)
        points.append({
            "time": time_el.text if time_el is not None else None,
            "lat": float(pos.find("t:LatitudeDegrees", NS).text),
            "lon": float(pos.find("t:LongitudeDegrees", NS).text),
            "elev_m": float(alt_el.text) if alt_el is not None else None,
            "dist_m": float(dist_el.text) if dist_el is not None else None,
            "hr": int(hr_el.text) if hr_el is not None else None,
            "speed_mps": float(speed_el.text) if speed_el is not None else None,
        })

    laps = []
    for lap_el in act.findall("t:Lap", NS):
        dist_el = lap_el.find("t:DistanceMeters", NS)
        time_el = lap_el.find("t:TotalTimeSeconds", NS)
        cal_el = lap_el.find("t:Calories", NS)
        avg_hr_el = lap_el.find("t:AverageHeartRateBpm/t:Value", NS)
        max_hr_el = lap_el.find("t:MaximumHeartRateBpm/t:Value", NS)
        laps.append({
            "start_time": lap_el.get("StartTime"),
            "distance_m": float(dist_el.text) if dist_el is not None else 0.0,
            "time_s": float(time_el.text) if time_el is not None else 0.0,
            "calories": int(cal_el.text) if cal_el is not None else None,
            "avg_hr": int(avg_hr_el.text) if avg_hr_el is not None else None,
            "max_hr": int(max_hr_el.text) if max_hr_el is not None else None,
        })

    date = start_time[:10] if start_time else "unknown"
    trailhead = classify_trailhead(points[0]["lat"], points[0]["lon"]) if points else "unknown"

    return {
        "garmin_id": garmin_id_from_path(path),
        "date": date,
        "trailhead": trailhead,
        "points": points,
        "laps": laps,
    }


def garmin_id_from_path(path):
    stem = path.stem  # activity_23729568728
    parts = stem.split("_")
    gid = parts[-1] if len(parts) >= 2 else stem
    return int(gid) if gid.isdigit() else gid


def classify_trailhead(lat, lon):
    best, best_d = None, float("inf")
    for key, th in TRAILHEADS.items():
        d = haversine_m(lat, lon, th["lat"], th["lon"])
        if d < best_d:
            best, best_d = key, d
    return best


def elev_gain_loss_m(points, threshold=ELEV_GAIN_LOSS_THRESHOLD_M):
    elevs = [p["elev_m"] for p in points if p["elev_m"] is not None]
    if not elevs:
        return 0.0, 0.0
    gain = loss = 0.0
    last = elevs[0]
    for e in elevs[1:]:
        d = e - last
        if d > threshold:
            gain += d
            last = e
        elif d < -threshold:
            loss += abs(d)
            last = e
    return gain, loss


def turnaround_point(points):
    """Highest-elevation point — proxy for the out-and-back turnaround on a
    trail that climbs from the trailhead to a mid-trail high point."""
    return max((p for p in points if p["elev_m"] is not None), key=lambda p: p["elev_m"])


def format_pace(seconds_per_mile):
    m = int(seconds_per_mile // 60)
    s = int(round(seconds_per_mile % 60))
    if s == 60:
        m += 1
        s = 0
    return f"{m}:{s:02d}/mi"


def format_duration(total_seconds):
    total_seconds = int(round(total_seconds))
    h, rem = divmod(total_seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def savefig_webp(fig, out_path):
    """Save a matplotlib figure as lossless WebP instead of PNG.

    These charts are mostly flat color + text/lines, where lossless WebP
    runs consistently 2.5-3x smaller than PNG at identical quality (no
    compression artifacts on the text), so there's no tradeoff to make.
    """
    buf = io.BytesIO()
    fig.savefig(buf, format="png", facecolor=fig.get_facecolor())
    buf.seek(0)
    Image.open(buf).convert("RGB").save(out_path, "WEBP", lossless=True, method=6)
