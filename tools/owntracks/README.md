# OwnTracks Region Time Analysis

Calculate minutes spent in each region per day from OwnTracks Recorder data exports.

## Overview

This tool parses OwnTracks transition events (region enter/leave) and calculates how many minutes per day you spent in each defined region. It produces a CSV with:
- One row per day
- One column per region (minutes spent in that region)
- A `not_in_region` column (minutes not in any defined region)
- A `total` column (always 1440 = 24 hours)

## Requirements

- Python 3.9+ (uses `zoneinfo` module)
- OwnTracks Recorder data export

## Workflow

```bash
# 1. Pull data from OwnTracks Recorder
mkdir -p /mnt/nas1/me/owntracks/$(date +%Y-%m-%d)/
scp -r root@owntracks-recorder.hummel.casa:/etc/owntracks-recorder/data/ \
    /mnt/nas1/me/owntracks/$(date +%Y-%m-%d)/

# 2. Run analysis
python3 region_time.py /mnt/nas1/me/owntracks/$(date +%Y-%m-%d)/data
python3 region_time.py /mnt/nas1/me/owntracks/$(date +%Y-%m-%d)/data 2026-02-05
python3 region_time.py /mnt/nas1/me/owntracks/$(date +%Y-%m-%d)/data 2026-02-05 2026-03-14
```

## Usage

```bash
python3 region_time.py <data_dir> [start_date] [end_date]
```

### Arguments

| Argument | Required | Format | Description |
|----------|----------|--------|-------------|
| `data_dir` | Yes | path | Path to OwnTracks data directory containing `.rec` files |
| `start_date` | No | YYYY-MM-DD | Start date. Default: first day of previous month |
| `end_date` | No | YYYY-MM-DD | End date. Default: today |

### Examples

```bash
# Use default date range (previous month + current month to date)
python3 region_time.py ./2026-01-19/data

# Specify start date only (runs through today)
python3 region_time.py ./2026-01-19/data 2025-12-01

# Specify both start and end dates
python3 region_time.py ./2026-01-19/data 2025-12-01 2026-01-19
```

### Full Example

```bash
# Generate the CSV
python3 region_time.py ./2026-01-19/data 2025-12-01 2026-01-19

# Pretty print the output
column -t -s, region_time_20260208T153042Z.csv
```

```
date        Home    Office  Gym   not_in_region  total
2025-12-01  1397.0  0       0.5   42.5           1440
2025-12-02  932.9   0       0     507.1          1440
2025-12-22  0       0       0     1440.0         1440
2025-12-23  987.9   452.1   0     0              1440
2025-12-25  1433.8  0       0     6.2            1440
```

## Output

The script writes a timestamped CSV file (e.g. `region_time_20260208T153042Z.csv`) to the current working directory.

### Sample Output

```csv
date,Gym,Home,Office,not_in_region,total
2025-12-01,0.5,1397.0,0,42.5,1440
2025-12-02,0,932.9,0,507.1,1440
2025-12-22,0,0,0,1440.0,1440
2025-12-23,0,987.9,452.1,0,1440
2025-12-25,0,1433.8,0,6.2,1440
```

### Column Descriptions

- **date**: ISO format date (YYYY-MM-DD)
- **[region columns]**: Minutes spent in each region (can overlap if regions overlap geographically)
- **not_in_region**: Minutes when not inside any defined region
- **total**: Always 1440 (24 hours × 60 minutes)

## Implementation Details

### Time Zone

All calculations use **Pacific Time** (America/Los_Angeles). Days run from midnight to midnight Pacific.

### Initial State Detection

The script replays all transition events before the start date to determine which regions you were in at the start of the analysis period. This ensures accurate time calculations even when the first event in the date range is a "leave" event.

### Location-Based Gap Filling

OwnTracks transition events sometimes have gaps — the phone drops `enter` or `leave` events, causing inaccurate time calculations. The script detects and fills these gaps using location data (periodic lat/lon reports with accuracy) and region definitions from the `waypoints/` directory (center lat/lon and radius in meters). Location events with poor accuracy (>100m) are ignored.

Three cases are handled:

1. **Missing enter** (leave→leave gap): After a "leave" for region R, if the next event for that region is another "leave" with no intervening "enter", searches location data in the gap for the first point **inside** the region and synthesizes an "enter" event.
2. **Missing leave** (enter→enter gap): After an "enter" for region R, if the next event for that region is another "enter" with no intervening "leave", searches location data in the gap for the first point **outside** the region and synthesizes a "leave" event.
3. **Excursions within enter→leave pairs**: For enter→leave pairs spanning more than 2 hours, checks if location data shows the phone left and returned mid-span. If the first location outside the region is followed by a later location back inside, synthesizes both a "leave" and "enter" to split the pair.

### Overlapping Regions

If regions overlap geographically, time spent in the overlap counts toward both regions. In this case, the sum of region columns may exceed 1440, but `not_in_region + time_in_at_least_one_region` will always equal 1440.

### Data Format

The script reads OwnTracks Recorder `.rec` files, which contain tab-separated records with JSON payloads. It looks for two event types:

- **`transition`** events: region enter/leave records
- **`location`** events: periodic lat/lon position reports (used for gap filling)

```
2025-12-23T15:30:00Z	event	{"_type":"transition","desc":"Home","event":"enter",...}
2025-12-23T15:33:00Z	*	{"_type":"location","lat":34.021,"lon":-118.420,"acc":5,...}
```

## Data Directory Structure

OwnTracks Recorder exports have this structure:

```
data/
├── rec/
│   └── username/
│       └── device-id/
│           ├── 2025-12.rec
│           └── 2026-01.rec
├── waypoints/
│   └── username/
│       └── device-id/
│           ├── 2024-09-14T18:51:14Z.json
│           └── ...
└── ...
```

The script recursively searches for all `.rec` files under the provided data directory, and loads region definitions from `waypoints/` JSON files (keeping the most recent definition for each region name).
