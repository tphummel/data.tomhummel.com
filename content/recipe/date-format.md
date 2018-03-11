---
title: "SQLite / IFTTT Date Formatting"
date: 2018-03-11T12:22:54-07:00
tags: ["analysis-recipe", "ifttt", "sqlite"]
---

Convert `January 01, 2018 at 01:50PM` to `2018-01-01T13:50`

<!--more-->

### Overview

1. [Intro](#intro)
1. [Problem](#problem)
1. [Data](#data)
1. [Solution](#solution)
1. [Walkthrough](#walkthrough)
  - [Year](#walkthrough-year)
  - [Month](#walkthrough-month)
  - [Day](#walkthrough-day)
  - [Time](#walkthrough-time)
  - [Zero-padding](#walkthrough-zero-padding)
  - [ISO 8601](#walkthrough-iso8601)
1. [Conclusion](#conclusion)


## Intro {#intro}

Tools like [harelba/q](http://harelba.github.io/q/) and [SQLite](https://www.sqlite.org/index.html) are powerful for doing local analysis on personal datasets and [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) is a fine standard for storing date and time data. SQLite expects date strings to be formatted this way. [Unfortunately](https://xkcd.com/1179/), not every service creates dates in this format. [IFTTT](https://ifttt.com) in particular creates timestamps in a very odd format - likely aimed at consumption by humans. You can reformat these strings using a tool of your choosing prior to loading into SQLite or you can format them within your queries. This is a guide to formatting date strings using SQLite-flavored SQL.

## Problem {#problem}

When you use the "Add Row to Spreadsheet" action in IFTTT (which the majority of my Applets use), you have access to an `OccurredAt` ingredient which you will use to attach the timestamp to each row. However, when you look at your spreadsheet the timestamp will look something like: `January 06, 2017 at 06:27PM` (as of 2018-03-11). This string is not ISO 8601 compliant. And there isn't a way to customize the date format via IFTTT (as of 2018-03-11).

If you intend to download this sheet as csv and do local analysis, you'll need to reformat these values in order to use [sqlite date functions](https://www.sqlite.org/lang_datefunc.html) like `strftime`. This is important because it unlocks the ability to use date modifiers and extract individual fragments from a date such as the week of year or day of week.

## Data {#data}

In this example we'll use a dataset that looks like one you would export from an IFTTT created google sheet.
```
 head -n 5 ./my-sheet.csv

"January 01, 2018 at 10:31AM",run,34.02130458,-118.4203004,https://ifttt.com/share/DSmnc9Dc9wM,,"https://maps.google.com/?q=34.0213045822793,-118.420300388416&z=16"
"January 01, 2018 at 10:49AM",run,34.02132238,-118.420358,https://ifttt.com/share/8hwhWk2B9wM,,"https://maps.google.com/?q=34.0213223817022,-118.420357970281&z=16"
"January 01, 2018 at 12:32PM",run,34.02138991,-118.4205079,https://ifttt.com/share/qmHTzhvMcwM,,"https://maps.google.com/?q=34.021389908732,-118.420507914225&z=16"
"January 01, 2018 at 01:22PM",run,34.02694743,-118.4133058,https://ifttt.com/share/knZxfTQPdwM,,"https://maps.google.com/?q=34.0269474311501,-118.413305830858&z=16"
"January 01, 2018 at 01:50PM",run,34.02128426,-118.420437,https://ifttt.com/share/g77ZC6JqfwM,,"https://maps.google.com/?q=34.0212842588202,-118.42043704072&z=16"
```

Note there is no header row. Column 1 contains the IFTTT formatted date string.

```
q -d "," "SELECT c1 FROM ./my-sheet.csv"

"January 01, 2018 at 10:31AM"
"January 01, 2018 at 10:49AM"
"January 01, 2018 at 12:32PM"
"January 01, 2018 at 01:22PM"
"January 01, 2018 at 01:50PM"
```

We'll need to craft a query that will convert dates like this:
```

```

## Solution {#solution}

```
q -d "," "select substr(ltrim(substr(c1, instr(c1, ' '))),5,4)||'-'||substr('00' || CASE substr(c1, 0, instr(c1, ' ')) WHEN 'January' THEN 01 WHEN 'February' THEN 02 WHEN 'March' THEN 03 WHEN 'April' THEN 04 WHEN 'May' THEN 05 WHEN 'June' THEN 06 WHEN 'July' THEN 07 WHEN 'August' THEN 08 WHEN 'September' THEN 09 WHEN 'October' THEN 10 WHEN 'November' THEN 11 WHEN 'December' THEN 12 END, -2)||'-'||substr('00'||substr(ltrim(substr(c1, instr(c1, ' '))),1,2),-2)||'T'||substr('00' || CASE WHEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) = 12 and substr(substr(ltrim(substr(c1, instr(c1, ' '))),13),-2) = 'AM' THEN 0 WHEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) = 12 and substr(substr(ltrim(substr(c1, instr(c1, ' '))),13),-2) = 'PM' THEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) WHEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) >= 1 and cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) < 12 and substr(substr(ltrim(substr(c1, instr(c1, ' '))),13),-2) = 'AM' THEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) WHEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) >= 1 and cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) < 12 and substr(substr(ltrim(substr(c1, instr(c1, ' '))),13),-2) = 'PM' THEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER)+12 END, -2)||':'||substr('00'||substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':')+1, 2),-2) as timestamp from ./my-sheet.csv"
```

## Walkthrough {#walkthrough}

The solution above works but it is incomprehensible. Here are the steps this query performs in order to convert `January 01, 2018 at 01:50PM` to `2018-01-01T13:50`:

- Extract the month string. Convert it from string to integer. Pad to two digits.
- Extract the time string. Then split into separate hour, minute, and AM/PM values.
- Handle inconsistent hour formats: `1:50`, `01:50`
- Handle inconsistent AM/PM: `1:50PM`, `1:50 PM`
- Convert 12-hour clock to 24-hour clock. Pad to two digits.
- Extract day of the month. Pad to two digits.
- Extract four-digit year.

#### Year {#walkthrough-year}

```
substr(ltrim(substr(c1, instr(c1, ' '))),5,4)
```

#### Month {#walkthrough-month}

Extract everything up to the first space in the string:
```
SELECT SUBSTR(c1, 0, INSTR(c1, ' ')) AS month
```

Convert the month string to a two-digit integer:
```
CASE substr(c1, 0, instr(c1, ' ')) WHEN 'January' THEN 01 WHEN 'February' THEN
02 WHEN 'March' THEN 03 WHEN 'April' THEN 04 WHEN 'May' THEN 05 WHEN 'June' THEN
06 WHEN 'July' THEN 07 WHEN 'August' THEN 08 WHEN 'September' THEN 09 WHEN
'October' THEN 10 WHEN 'November' THEN 11 WHEN 'December' THEN 12 END AS month
```

#### Day {#walkthrough-day}

```
substr(ltrim(substr(c1, instr(c1, ' '))),1,2)
```

#### Time {#walkthrough-time}

Extract Minute:
```
substr(substr(ltrim(substr(c1, instr(c1, ' '))),13,7),4,2) AS minute
```

Extract AM/PM:
```
substr(substr(ltrim(substr(c1, instr(c1, ' '))),13),-2) as ampm
```

Extract original hour value:
```
cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) as hour12
```
We have to coerce/cast the original hour value string into an integer before converting it so we can do integer comparisons on it during the conversion.

Pseudocode algorithm to convert the hour value from 12-hour clock to 24-hour clock:
```
CASE
  WHEN hour12 = 12 and ampm = 'AM'
    THEN 00
  WHEN hour12 = 12 and ampm = 'PM'
    THEN hour12
  WHEN hour12 >= 1 and hour12 < 12 and ampm = 'AM'
    THEN hour12
  WHEN hour12 >= 1 and hour12 < 12 and ampm = 'PM'
    THEN hour12+12
END
```
When you substitute the actual query for `hour12` and `ampm` it gets much longer, but it is still the same as above in structure:
```
CASE
  WHEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) = 12 and substr(substr(ltrim(substr(c1, instr(c1, ' '))),13),-2) = 'AM'
    THEN 0
  WHEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) = 12 and substr(substr(ltrim(substr(c1, instr(c1, ' '))),13),-2) = 'PM'
    THEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER)
  WHEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) >= 1 and cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) < 12 and substr(substr(ltrim(substr(c1, instr(c1, ' '))),13),-2) = 'AM'
    THEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER)
  WHEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) >= 1 and cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) < 12 and substr(substr(ltrim(substr(c1, instr(c1, ' '))),13),-2) = 'PM'
    THEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER)+12
END as hour24
```

#### Zero padding {#walkthrough-zero-padding}

There is no direct function to zero-pad the string representations of integers in sqlite. However, there is a handy trick [I found on stackoverflow](https://stackoverflow.com/questions/4899832/sqlite-function-to-format-numbers-with-leading-zeroes)


```
-- left-pad with zeroes a field called `month` to two digits
substr('00' || month, -2)
```

#### ISO 8601 {#walkthrough-iso8601}

Put it all together and the pseudo code looks like:
```
year||'-'||substr('00' || month, -2)||'-'||substr('00'||dom,-2)||'T'||substr('00' || hour24, -2)||':'||substr('00'||minutes,-2) as iso8601
```

## Conclusion {#conclusion}

This is a specific problem and solution, but the techniques here can be used to format other non-standard date formats.
