# OwnTracks Region Time Analysis

Parses OwnTracks transition events (region enter/leave) and calculates minutes per day spent in each region. Outputs a timestamped CSV with one row per day, one column per region, a `not_in_region` column, and a `total` column (always 1440).

## Usage

```bash
python3 region_time.py <data_dir> [start_date] [end_date]
```

`start_date` defaults to the first day of the previous month. `end_date` defaults to today.

```bash
# Pull data from OwnTracks Recorder
scp -r root@owntracks-recorder.hummel.casa:/etc/owntracks-recorder/data/ \
    /mnt/nas1/me/owntracks/$(date +%Y-%m-%d)/

# Run
python3 region_time.py /mnt/nas1/me/owntracks/$(date +%Y-%m-%d)/data
python3 region_time.py /mnt/nas1/me/owntracks/$(date +%Y-%m-%d)/data 2026-02-05
python3 region_time.py /mnt/nas1/me/owntracks/$(date +%Y-%m-%d)/data 2026-02-05 2026-03-14
```

## Implementation notes

All calculations use **Pacific Time** (America/Los_Angeles).

The script replays all transition events before the start date to determine which regions you were in at the analysis start, so a "leave" as the first event in the date range is handled correctly.

**Gap filling:** OwnTracks sometimes drops enter/leave events. The script detects and fills three cases using location data from the `waypoints/` directory:

1. **Missing enter** (leave→leave): finds the first location point inside the region and synthesizes an enter event.
2. **Missing leave** (enter→enter): finds the first location point outside the region and synthesizes a leave event.
3. **Excursion within enter→leave**: for pairs spanning >2 hours, checks if location data shows the phone left and returned; synthesizes the missing leave+enter.

Location events with accuracy >100m are ignored.

**Overlapping regions:** time in an overlap counts toward both regions. Region column sums may exceed 1440, but `not_in_region + time_in_at_least_one_region` always equals 1440.

## Data directory structure

```
data/
├── rec/
│   └── username/
│       └── device-id/
│           ├── 2025-12.rec
│           └── 2026-01.rec
└── waypoints/
    └── username/
        └── device-id/
            └── 2024-09-14T18:51:14Z.json
```

Reads all `.rec` files recursively. Region definitions are loaded from `waypoints/` JSON files; the most recent definition per region name is used.
