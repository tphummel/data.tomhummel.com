---
title: "iOS Location"
date: 2019-10-26T13:11:23-08:00
tags: ["analysis-recipe"]
---

Set up a geofence around your common locations (home, work) and automatically get enter and exit events written to a google sheet. Allows you to passively build a report of where you spend your time.

<!--more-->

## ifttt recipes

### geofences

Allow IFTTT on your iPhone to use location even when not using the app. Create an applet for each key location you want to track. For me, I have two applets: home and work.

**If This**: you enter or exit an area (a geo fence around a map location)

drop a pin on the location and set the zoom to determine the radius of the geofence.

**Then That**: add a row to a spreadsheet.

Spreadsheet name: `ifttt-location-activity`

Formatted row:
```
{{OccurredAt}} ||| {{EnteredOrExited}} ||| =IMAGE("{{LocationMapImageUrl}}";1) ||| {{LocationMapUrl}} ||| home
```

use a different literal value for the final cell in each recipe as a convenience to distinguish the location of each row.

Drive folder path: `IFTTT/iOS Location`

### nightly marker

Every night at 11:45PM, write a marker row to your spreadsheet. This allows for clean divisions of days when summing.

**If This**: every day at 11:45PM Pacific

**Then That**: add a row to a spreadsheet.

Formatted row:

```
{{CheckTime}}|||=INDIRECT(ADDRESS(ROW()-1,COLUMN()))|||=INDIRECT(ADDRESS(ROW()-1,COLUMN()))|||=INDIRECT(ADDRESS(ROW()-1,COLUMN()))|||=INDIRECT(ADDRESS(ROW()-1,COLUMN()))
```

This will insert a sheet every night with formulas to duplicate the row above it. This a convenience to make daily sums tidy.

## spreadsheet enrichment

With these three applets writing to a single google sheet into the first sheet/tab, you'll have all your raw data in one place.

Add a second tab to the workbook. Reference the raw values from the first tab. You can either do this with cell references you drag the cross cursor down to bottom of the page (ex: `={Sheet1!A3:E}`), or you can do an [importrange](https://support.google.com/docs/answer/3093340?hl=en).

Columns A through E will come from the raw inputs on sheet 1. I leave a blank column F as a visual delimiter. Use the following labels for row 1 of columns G through P.

```
datetime	date	year	dow	moy	woy	time diff	prev type	prev name	prev
```

For row 2 of columns G through P, use:

- Column G: `=replace(A2,find(" at ",A2),4," ")`
- Column H: `=to_date(datevalue(G2))`
- Column I: `=year(H2)`
- Column J: `=WEEKDAY(H2)&"-"&TEXT(H2,"ddd")`
- Column K: `=text(H2,"mm-mmm")`
- Column L: `=weeknum(H2)`
- Column M: `=G2-G1`
- Column O: `=if(E1="123-main-st","home",if(E1="456-wall-st", "work", "other))"))`
- Column P: `=if(N2="entered", "at " & O2, "out")`

Column O can handle any mapping based on the literal string value you provided in the final cell of the ifttt geofence applets. If you set up that value as you want it to appear in your reports, you can use `=E1` instead (the raw value of `location` which came directly from ifttt). The else case for `other` can also help you catch any weird values that come in from ifttt or your formulas.

Select Row 2, columns G through P. Click and hold the bottom right corner of P2 when the cursor turns into a cross. Then drag downward to the bottom of the sheet.

Clear the contents of columns M through P in row 2. These are delta/relative rows which only make sense in row 3 and below.

The really neat part about the enrichment, particular columns M through P, is you wind up with time deltas between events and automatic attribution for where that time was spent. From here, the data is teed up to build reports using pivot tables.

## pivot tables

## notes

- Sometimes rows get written out of order by ifttt. This is the most common reason for odd looking sums. Reorder the rows to correct this.
- When reordering incorrectly written rows or adding missing rows, it can be helpful to consult other data sources such as Automatic of Swarm.
