#!/usr/bin/env python3
"""
Calculate minutes spent in each region per day from OwnTracks transition events.
Days are calculated in Pacific time, from midnight to midnight.

Usage:
    python region_time.py <data_dir> [start_date] [end_date]

Examples:
    python region_time.py ./2026-01-19/data
    python region_time.py ./2026-01-19/data 2025-12-01
    python region_time.py ./2026-01-19/data 2025-12-01 2026-01-19
"""

import argparse
import json
import math
import os
import re
import sys
from datetime import datetime, date, timedelta
from collections import defaultdict
from zoneinfo import ZoneInfo
import csv

PACIFIC = ZoneInfo("America/Los_Angeles")
UTC = ZoneInfo("UTC")


def parse_rec_files(data_dir):
    """Parse all .rec files and extract transition events."""
    events = []
    rec_pattern = re.compile(r'\.rec$')

    for root, dirs, files in os.walk(data_dir):
        for filename in files:
            if rec_pattern.search(filename):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                        for line in f:
                            if '"_type":"transition"' in line:
                                parts = line.strip().split('\t', 2)
                                if len(parts) >= 3:
                                    try:
                                        data = json.loads(parts[2])
                                        if data.get('_type') == 'transition':
                                            events.append({
                                                'timestamp': data['tst'],
                                                'region': data['desc'],
                                                'event': data['event'],
                                            })
                                    except (json.JSONDecodeError, KeyError):
                                        pass
                except Exception as e:
                    print(f"Error reading {filepath}: {e}", file=sys.stderr)

    events.sort(key=lambda x: x['timestamp'])
    return events


def parse_location_events(data_dir):
    """Parse all .rec files and extract location events."""
    locations = []
    rec_pattern = re.compile(r'\.rec$')

    for root, dirs, files in os.walk(data_dir):
        for filename in files:
            if rec_pattern.search(filename):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                        for line in f:
                            if '"_type":"location"' in line:
                                parts = line.strip().split('\t', 2)
                                if len(parts) >= 3:
                                    try:
                                        data = json.loads(parts[2])
                                        if data.get('_type') == 'location':
                                            locations.append({
                                                'timestamp': data['tst'],
                                                'lat': data['lat'],
                                                'lon': data['lon'],
                                                'acc': data.get('acc', 0),
                                            })
                                    except (json.JSONDecodeError, KeyError):
                                        pass
                except Exception as e:
                    print(f"Error reading {filepath}: {e}", file=sys.stderr)

    locations.sort(key=lambda x: x['timestamp'])
    return locations


def load_waypoints(data_dir):
    """Load region definitions from the waypoints directory.

    Walks the waypoints/ directory (sibling to rec/) and parses JSON files.
    For each region description, keeps the most recent definition (by tst).
    Returns a dict of region_name -> {lat, lon, rad, desc}.
    """
    # waypoints/ is a sibling of rec/ inside data_dir
    waypoints_dir = os.path.join(data_dir, 'waypoints')
    if not os.path.isdir(waypoints_dir):
        return {}

    regions = {}
    for root, dirs, files in os.walk(waypoints_dir):
        for filename in files:
            if filename.endswith('.json'):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    if data.get('_type') == 'waypoint':
                        desc = data.get('desc', '')
                        tst = data.get('tst', 0)
                        if desc not in regions or tst > regions[desc]['tst']:
                            regions[desc] = {
                                'desc': desc,
                                'lat': data['lat'],
                                'lon': data['lon'],
                                'rad': data['rad'],
                                'tst': tst,
                            }
                except (json.JSONDecodeError, KeyError, OSError):
                    pass

    # Remove the tst field used for dedup
    for r in regions.values():
        del r['tst']

    return regions


def haversine_distance(lat1, lon1, lat2, lon2):
    """Return distance in meters between two lat/lon points."""
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def is_in_region(lat, lon, region):
    """Return True if the point (lat, lon) is within the region's radius."""
    dist = haversine_distance(lat, lon, region['lat'], region['lon'])
    return dist <= region['rad']


def synthesize_missing_events(events, locations, regions):
    """Fill gaps in transition events using location data.

    Handles missing transitions in three cases:
    1. Missing "enter": leave→leave gap (or leave with no subsequent enter) —
       search for the first location inside the region and synthesize an "enter".
    2. Missing "leave": enter→enter gap (or enter with no subsequent leave) —
       search for the first location outside the region and synthesize a "leave".
    3. Excursions within enter→leave pairs: if the phone left and returned
       within a valid pair (>2h span), synthesize both a "leave" and "enter"
       using the first outside and first subsequent inside location points.

    Returns a new list of events (original + synthetic), sorted by timestamp.
    """
    if not locations or not regions:
        return events

    import bisect

    synthetic = []

    loc_timestamps = [loc['timestamp'] for loc in locations]

    # Build per-region event sequences for analysis
    region_events = defaultdict(list)
    for i, event in enumerate(events):
        region_events[event['region']].append((i, event))

    for region_name, revents in region_events.items():
        if region_name not in regions:
            continue

        region_def = regions[region_name]

        for ri, (idx, event) in enumerate(revents):
            if event['event'] != 'leave':
                continue

            leave_ts = event['timestamp']

            # Find the next event for this same region
            next_event = revents[ri + 1] if ri + 1 < len(revents) else None

            if next_event is not None:
                _, next_ev = next_event
                if next_ev['event'] == 'enter':
                    # leave → enter: normal, no gap
                    continue
                # leave → leave: missing enter between the two leaves
                search_end_ts = next_ev['timestamp']
            else:
                # leave with no further events for this region
                # Search up to end of location data
                search_end_ts = loc_timestamps[-1] + 1 if loc_timestamps else leave_ts

            # Search location events between leave and the search end.
            # Find the first location that's inside the region.
            loc_idx = bisect.bisect_left(loc_timestamps, leave_ts)

            for k in range(loc_idx, len(locations)):
                loc = locations[k]
                if loc['timestamp'] >= search_end_ts:
                    break
                if loc['acc'] > 100:
                    continue
                if is_in_region(loc['lat'], loc['lon'], region_def):
                    synthetic.append({
                        'timestamp': loc['timestamp'],
                        'region': region_name,
                        'event': 'enter',
                        'synthetic': True,
                    })
                    break

    # Second pass: find missing "leave" events (enter→enter gaps)
    for region_name, revents in region_events.items():
        if region_name not in regions:
            continue

        region_def = regions[region_name]

        for ri, (idx, event) in enumerate(revents):
            if event['event'] != 'enter':
                continue

            enter_ts = event['timestamp']

            # Find the next event for this same region
            next_event = revents[ri + 1] if ri + 1 < len(revents) else None

            if next_event is not None:
                _, next_ev = next_event
                if next_ev['event'] == 'leave':
                    # enter → leave: normal, no gap
                    continue
                # enter → enter: missing leave between the two enters
                search_end_ts = next_ev['timestamp']
            else:
                # enter with no further events for this region
                # Search up to end of location data
                search_end_ts = loc_timestamps[-1] + 1 if loc_timestamps else enter_ts

            # Search location events between enter and the search end.
            # Find the first location that's outside the region.
            loc_idx = bisect.bisect_left(loc_timestamps, enter_ts)

            for k in range(loc_idx, len(locations)):
                loc = locations[k]
                if loc['timestamp'] >= search_end_ts:
                    break
                if loc['acc'] > 100:
                    continue
                if not is_in_region(loc['lat'], loc['lon'], region_def):
                    synthetic.append({
                        'timestamp': loc['timestamp'],
                        'region': region_name,
                        'event': 'leave',
                        'synthetic': True,
                    })
                    break

    # Third pass: find excursions within enter→leave pairs.
    # If the phone left and returned within a valid enter→leave span,
    # both the leave and re-enter events were dropped. Detect this by
    # scanning location data for points outside the region, then finding
    # the return point.
    for region_name, revents in region_events.items():
        if region_name not in regions:
            continue

        region_def = regions[region_name]

        for ri, (idx, event) in enumerate(revents):
            if event['event'] != 'enter':
                continue

            enter_ts = event['timestamp']

            next_event = revents[ri + 1] if ri + 1 < len(revents) else None
            if next_event is None:
                continue
            _, next_ev = next_event
            if next_ev['event'] != 'leave':
                continue

            leave_ts = next_ev['timestamp']

            # Only check spans longer than 2 hours — short spans are normal
            if leave_ts - enter_ts < 7200:
                continue

            # Find first location outside the region (= missing leave)
            loc_idx = bisect.bisect_left(loc_timestamps, enter_ts)
            excursion_leave_ts = None

            for k in range(loc_idx, len(locations)):
                loc = locations[k]
                if loc['timestamp'] >= leave_ts:
                    break
                if loc['acc'] > 100:
                    continue
                if not is_in_region(loc['lat'], loc['lon'], region_def):
                    excursion_leave_ts = loc['timestamp']
                    excursion_leave_k = k
                    break

            if excursion_leave_ts is None:
                continue

            # Find first location back inside the region (= missing enter)
            for k in range(excursion_leave_k + 1, len(locations)):
                loc = locations[k]
                if loc['timestamp'] >= leave_ts:
                    break
                if loc['acc'] > 100:
                    continue
                if is_in_region(loc['lat'], loc['lon'], region_def):
                    synthetic.append({
                        'timestamp': excursion_leave_ts,
                        'region': region_name,
                        'event': 'leave',
                        'synthetic': True,
                    })
                    synthetic.append({
                        'timestamp': loc['timestamp'],
                        'region': region_name,
                        'event': 'enter',
                        'synthetic': True,
                    })
                    break

    if not synthetic:
        return events

    combined = events + synthetic
    combined.sort(key=lambda x: x['timestamp'])
    return combined


def get_pacific_day(unix_ts):
    """Get the date in Pacific time for a unix timestamp."""
    dt = datetime.fromtimestamp(unix_ts, tz=UTC).astimezone(PACIFIC)
    return dt.date()


def get_day_boundaries(date_obj):
    """Get start and end unix timestamps for a Pacific day."""
    start_dt = datetime(date_obj.year, date_obj.month, date_obj.day, 0, 0, 0, tzinfo=PACIFIC)
    end_dt = start_dt + timedelta(days=1)
    return int(start_dt.timestamp()), int(end_dt.timestamp())


def add_time_to_daily(daily_dict, key, start_ts, end_ts):
    """Add time to a daily dictionary, splitting across day boundaries."""
    if end_ts <= start_ts:
        return

    start_date = get_pacific_day(start_ts)
    end_date = get_pacific_day(end_ts)

    current_date = start_date
    current_ts = start_ts

    while current_date <= end_date:
        day_start, day_end = get_day_boundaries(current_date)
        segment_start = max(current_ts, day_start)
        segment_end = min(end_ts, day_end)

        if segment_end > segment_start:
            minutes = (segment_end - segment_start) / 60.0
            daily_dict[current_date][key] += minutes

        current_date += timedelta(days=1)
        current_ts = day_end


def calculate_daily_region_time(events, first_date, last_date, initial_regions=None):
    """
    Calculate minutes spent in each region per day.

    Args:
    - events: list of transition events
    - first_date: start date for output
    - last_date: end date for output
    - initial_regions: dict of region -> True for regions we're in at start

    Returns:
    - daily_minutes: dict[date][region] = minutes
    - daily_not_in_region: dict[date] = minutes when not in any region
    """
    all_regions = set(e['region'] for e in events)
    if initial_regions:
        all_regions.update(initial_regions.keys())

    daily_minutes = defaultdict(lambda: defaultdict(float))
    daily_not_in_region = defaultdict(lambda: defaultdict(float))

    day_start_ts, _ = get_day_boundaries(first_date)
    _, day_end_ts = get_day_boundaries(last_date)

    current_regions = {}
    if initial_regions:
        for region in initial_regions:
            current_regions[region] = day_start_ts

    last_state_change_ts = day_start_ts

    for event in events:
        ts = event['timestamp']
        region = event['region']
        action = event['event']

        is_currently_in_any = len(current_regions) > 0

        if action == 'enter':
            if region not in current_regions:
                if not is_currently_in_any:
                    add_time_to_daily(daily_not_in_region, 'not_in_region', last_state_change_ts, ts)
                    last_state_change_ts = ts
                current_regions[region] = ts
        elif action == 'leave':
            if region in current_regions:
                enter_ts = current_regions.pop(region)
                add_time_to_daily(daily_minutes, region, enter_ts, ts)
                if len(current_regions) == 0:
                    last_state_change_ts = ts

    for region, enter_ts in current_regions.items():
        add_time_to_daily(daily_minutes, region, enter_ts, day_end_ts)

    if len(current_regions) == 0:
        add_time_to_daily(daily_not_in_region, 'not_in_region', last_state_change_ts, day_end_ts)

    return daily_minutes, daily_not_in_region, all_regions


def generate_csv(daily_minutes, daily_not_in_region, all_regions, first_date, last_date):
    """Generate CSV output with one row per day."""
    regions = sorted(all_regions)
    header = ['date'] + regions + ['not_in_region', 'total']

    rows = []
    current_date = first_date
    total_day_minutes = 24 * 60

    while current_date <= last_date:
        row = {'date': current_date.isoformat()}

        for region in regions:
            minutes = daily_minutes[current_date].get(region, 0)
            row[region] = round(minutes, 1)

        not_in_region = daily_not_in_region[current_date].get('not_in_region', 0)
        row['not_in_region'] = round(not_in_region, 1)
        row['total'] = total_day_minutes

        rows.append(row)
        current_date += timedelta(days=1)

    return header, rows


def get_default_date_range():
    """Get default date range: first day of previous month to today."""
    today = datetime.now(PACIFIC).date()

    # First day of current month
    first_of_current = date(today.year, today.month, 1)

    # First day of previous month
    if today.month == 1:
        first_of_previous = date(today.year - 1, 12, 1)
    else:
        first_of_previous = date(today.year, today.month - 1, 1)

    return first_of_previous, today


def parse_date(date_str):
    """Parse a YYYY-MM-DD date string."""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: {date_str}. Use YYYY-MM-DD.")


def main():
    parser = argparse.ArgumentParser(
        description='Calculate minutes spent in each region per day from OwnTracks data.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ./2026-01-19/data
  %(prog)s ./2026-01-19/data 2025-12-01
  %(prog)s ./2026-01-19/data 2025-12-01 2026-01-19

Output is written to region_time.csv in the current directory.
Days are calculated in Pacific time (midnight to midnight).
        """
    )
    parser.add_argument('data_dir', help='Path to OwnTracks data directory')
    parser.add_argument('start_date', nargs='?', type=parse_date,
                        help='Start date (YYYY-MM-DD). Default: first of previous month')
    parser.add_argument('end_date', nargs='?', type=parse_date,
                        help='End date (YYYY-MM-DD). Default: today')

    args = parser.parse_args()

    # Set default dates if not provided
    default_start, default_end = get_default_date_range()
    start_date = args.start_date or default_start
    end_date = args.end_date or default_end

    if start_date > end_date:
        print(f"Error: start_date ({start_date}) is after end_date ({end_date})", file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(args.data_dir):
        print(f"Error: {args.data_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    print(f"Data directory: {args.data_dir}")
    print(f"Date range: {start_date} to {end_date}")

    print("Parsing transition events...")
    events = parse_rec_files(args.data_dir)
    print(f"Found {len(events)} total transition events")

    if not events:
        print("No events found!")
        sys.exit(1)

    # Load location events and waypoints for gap-filling
    print("Parsing location events...")
    locations = parse_location_events(args.data_dir)
    print(f"Found {len(locations)} location events")

    print("Loading waypoint definitions...")
    waypoint_regions = load_waypoints(args.data_dir)
    print(f"Loaded {len(waypoint_regions)} region definitions: {sorted(waypoint_regions.keys())}")

    start_ts, _ = get_day_boundaries(start_date)
    _, end_ts = get_day_boundaries(end_date)

    # Determine initial state from original events before start date
    initial_regions = {}
    for e in events:
        if e['timestamp'] >= start_ts:
            break
        if e['event'] == 'enter':
            initial_regions[e['region']] = True
        elif e['event'] == 'leave':
            initial_regions.pop(e['region'], None)

    print(f"Initial state at {start_date}: in regions {list(initial_regions.keys()) or 'none'}")

    range_events = [e for e in events if start_ts <= e['timestamp'] < end_ts]
    print(f"Filtered to {len(range_events)} events in date range")

    # Synthesize missing transition events from location data (within date range only)
    range_locations = [l for l in locations if start_ts <= l['timestamp'] < end_ts]
    num_before = len(range_events)
    range_events = synthesize_missing_events(range_events, range_locations, waypoint_regions)
    num_synthetic = len(range_events) - num_before
    print(f"Synthesized {num_synthetic} missing transition events from location data")

    print("Calculating daily region time...")
    daily_minutes, daily_not_in_region, all_regions = calculate_daily_region_time(
        range_events, start_date, end_date, initial_regions
    )

    print(f"Regions: {sorted(all_regions)}")

    header, rows = generate_csv(daily_minutes, daily_not_in_region, all_regions, start_date, end_date)

    output_file = f"region_time_{datetime.now(tz=UTC).strftime('%Y%m%dT%H%M%SZ')}.csv"
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Output written to {output_file}")

    print("\nFirst 10 rows:")
    print(','.join(header))
    for row in rows[:10]:
        print(','.join(str(row.get(h, '')) for h in header))


if __name__ == '__main__':
    main()
