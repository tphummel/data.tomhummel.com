---
title: "workspace"
date: 2018-04-24T16:08:56-07:00
tags: []
---

<!--more-->

### union multiple files
```
q -d "," "select * from "<(q -d "," "select c1,c2,c3,c4 from ./body-via-do-2017.csv UNION select c1,c2,c3,c4 from ./body-via-do-2018-partial.csv")""
```

### add header row, enrich date format, trimmed time window, trimmed event type. save to intermediate file.

```
echo "timestamp,type,lat,lon" > year-one-sneezes.csv && q -d "," "select substr(ltrim(substr(c1, instr(c1, ' '))),5,4)||'-'||substr('00' || CASE substr(c1, 0, instr(c1, ' ')) WHEN 'January' THEN 01 WHEN 'February' THEN 02 WHEN 'March' THEN 03 WHEN 'April' THEN 04 WHEN 'May' THEN 05 WHEN 'June' THEN 06 WHEN 'July' THEN 07 WHEN 'August' THEN 08 WHEN 'September' THEN 09 WHEN 'October' THEN 10 WHEN 'November' THEN 11 WHEN 'December' THEN 12 END, -2)||'-'||substr('00'||substr(ltrim(substr(c1, instr(c1, ' '))),1,2),-2)||'T'||substr('00' || CASE WHEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) = 12 and substr(substr(ltrim(substr(c1, instr(c1, ' '))),13),-2) = 'AM' THEN 0 WHEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) = 12 and substr(substr(ltrim(substr(c1, instr(c1, ' '))),13),-2) = 'PM' THEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) WHEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) >= 1 and cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) < 12 and substr(substr(ltrim(substr(c1, instr(c1, ' '))),13),-2) = 'AM' THEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) WHEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) >= 1 and cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) < 12 and substr(substr(ltrim(substr(c1, instr(c1, ' '))),13),-2) = 'PM' THEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER)+12 END, -2)||':'||substr('00'||substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':')+1, 2),-2) as timestamp, c2, c3, c4 from "<(q -d "," "select c1,c2,c3,c4 from ./body-via-do-2017.csv UNION select c1,c2,c3,c4 from ./body-via-do-2018-partial.csv")" where c2 = 'sneeze' and timestamp >= '2017-04-22' and timestamp <= '2018-04-23' order by timestamp" >> year-one-sneezes.csv
```

### all rows via column names

```
q -H -d "," "select timestamp,type,lat,lon from ./year-one-sneezes.csv"
```

### total sneezes

```
q -H -d "," "select count(*) from ./year-one-sneezes.csv"
```

### sneezes by year, month

```
q -H -d "," "select strftime('%Y', timestamp) as year, strftime('%m', timestamp) as month, count(*) from ./year-one-sneezes.csv group by year, month"
```

### sneezes by year, week

```
q -H -d "," "select strftime('%Y', timestamp) as year, strftime('%W', timestamp) as week, count(*) from ./year-one-sneezes.csv group by year, week"
```

### sneezes by day. save to intermediate file

```
echo "date,count" > year-one-sneezes-daily.csv && q -H -d "," "select date(timestamp) as day, count(*) from ./year-one-sneezes.csv group by day" >> year-one-sneezes-daily.csv
```

### sneezes summed by day of week (with day count for averaging)

```
q -H -d "," "select strftime('%w', date) as dow, count(date) as days, sum(count) as sneezes from ./year-one-sneezes-daily.csv group by dow"
```

### most sneezes in one day

```
q -H -d "," "select date, count from ./year-one-sneezes-daily.csv order by count desc limit 10"
```

### most sneezes in one day (by day of week, 0-6: sun-sat)

```
# sunday
q -H -d "," "select date, count from ./year-one-sneezes-daily.csv where strftime('%w', date) = '0' order by count desc limit 5"
```

### most sneezes in one day (by month of year, 01-12)

```
# january
q -H -d "," "select date, count from ./year-one-sneezes-daily.csv where strftime('%m', date) = '01' order by count desc limit 5"
```

### most consecutive days with 1+ sneeze

```
# generate reference date range
date-range 2017-04-22 2018-04-23 | jq -r '.[]'

# query daily sneezes
q -H -d "," "select date, count from ./year-one-sneezes-daily.csv order by date asc"
```

### most consecutive days with 0 sneezes

### most sneezes in a 5 day span
