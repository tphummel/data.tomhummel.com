#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["ruamel.yaml"]
# ///
"""
One-time migration: rename elev_ft -> elev_gain_ft and add elev_loss_ft
by re-parsing GPX files where available.
"""

import io
import math
import xml.etree.ElementTree as ET
from pathlib import Path

from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).parent.parent.parent
PAGE_PATH = REPO_ROOT / "content" / "report" / "adhoc" / "santa-monica-mountains-running.md"
GPX_DIR = Path.home() / "Documents" / "santa monica mountains running"


def compute_elev(gpx_path):
    ns = {"g": "http://www.topografix.com/GPX/1/1"}
    root = ET.parse(gpx_path).getroot()
    elevs = [float(p.find("g:ele", ns).text)
             for p in root.findall(".//g:trkpt", ns)
             if p.find("g:ele", ns) is not None]
    gain = loss = 0.0
    last = elevs[0] if elevs else 0.0
    for e in elevs[1:]:
        d = e - last
        if d > 11:
            gain += d; last = e
        elif d < -11:
            loss += abs(d); last = e
    return int(round(gain * 3.28084)), int(round(loss * 3.28084))


def main():
    text = PAGE_PATH.read_text()
    _, fm_text, body = text.split("---", 2)
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    data = yaml.load(fm_text)

    for run in data.get("runs", []):
        old_gain = run.pop("elev_ft", run.get("elev_gain_ft", 0))
        gid = str(run.get("garmin_id", ""))
        candidates = list(GPX_DIR.glob(f"activity_{gid}.gpx"))
        if candidates:
            gain, loss = compute_elev(candidates[0])
            run["elev_gain_ft"] = gain
            run["elev_loss_ft"] = loss
            print(f"  {run['date']} {run['name'][:40]}: +{gain} / -{loss} ft (from GPX)")
        else:
            run["elev_gain_ft"] = old_gain
            run["elev_loss_ft"] = None
            print(f"  {run['date']} {run['name'][:40]}: +{old_gain} ft (no GPX, loss unknown)")

    yaml2 = YAML()
    yaml2.preserve_quotes = True
    yaml2.width = 4096
    yaml2.default_flow_style = False
    stream = io.StringIO()
    yaml2.dump(data, stream)
    PAGE_PATH.write_text(f"---\n{stream.getvalue()}---{body}")
    print("\nDone.")


if __name__ == "__main__":
    main()
