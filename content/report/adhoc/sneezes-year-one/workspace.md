---
title: "workspace"
date: 2018-04-24T16:08:56-07:00
tags: []
draft: true
---

<!--more-->

### input prep

the 2018 file was in progress, I copied the current year file from: `My Drive/IFTTT/body-functions/body-via-do`

downloads from google drive as csv (sheet 1):

- `My Drive/Annual Data Files/2017/2017-body-via-do`
- `My Drive/Annual Data Files/2018/2018-body-via-do`

```
# pwd my clone of data.tomhummel.com repo
git checkout first-year-of-sneezes
cd content/report/adhoc/sneezes-year-one
mv ~/Downloads/2018-body-via-do\ -\ Sheet1.csv ./2018-body-via-do.csv
mv ~/Downloads/2017-body-via-do\ -\ Sheet1.csv ./2017-body-via-do.csv
```

### add header row, enrich date format, filtered time window, filtered event type. save to intermediate file.

```
echo "timestamp,type,lat,lon" > year-one-sneezes.csv && q -d "," "select substr(ltrim(substr(c1, instr(c1, ' '))),5,4)||'-'||substr('00' || CASE substr(c1, 0, instr(c1, ' ')) WHEN 'January' THEN 01 WHEN 'February' THEN 02 WHEN 'March' THEN 03 WHEN 'April' THEN 04 WHEN 'May' THEN 05 WHEN 'June' THEN 06 WHEN 'July' THEN 07 WHEN 'August' THEN 08 WHEN 'September' THEN 09 WHEN 'October' THEN 10 WHEN 'November' THEN 11 WHEN 'December' THEN 12 END, -2)||'-'||substr('00'||substr(ltrim(substr(c1, instr(c1, ' '))),1,2),-2)||'T'||substr('00' || CASE WHEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) = 12 and substr(substr(ltrim(substr(c1, instr(c1, ' '))),13),-2) = 'AM' THEN 0 WHEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) = 12 and substr(substr(ltrim(substr(c1, instr(c1, ' '))),13),-2) = 'PM' THEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) WHEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) >= 1 and cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) < 12 and substr(substr(ltrim(substr(c1, instr(c1, ' '))),13),-2) = 'AM' THEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) WHEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) >= 1 and cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER) < 12 and substr(substr(ltrim(substr(c1, instr(c1, ' '))),13),-2) = 'PM' THEN cast(substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':'), -2) as INTEGER)+12 END, -2)||':'||substr('00'||substr(substr(ltrim(substr(c1, instr(c1, ' '))),13), instr(substr(ltrim(substr(c1, instr(c1, ' '))),13), ':')+1, 2),-2) as timestamp, c2, c3, c4 from "<(q -d "," "select c1,c2,c3,c4 from ./2017-body-via-do.csv UNION select c1,c2,c3,c4 from ./2018-body-via-do.csv")" where c2 = 'sneeze' and timestamp >= '2017-04-23' and timestamp <= '2018-04-22' order by timestamp" >> year-one-sneezes.csv
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
q -H -d "," "select strftime('%Y', timestamp) as year, strftime('%m', timestamp) as month, count(*) from ./year-one-sneezes.csv group by year, month order by year, month" | (echo 'year,month,count' && cat) | csvlook
```

### sneezes by year, week

```
q -H -d "," "select strftime('%Y', timestamp) as year, strftime('%W', timestamp) as week, count(*) from ./year-one-sneezes.csv group by year, week" | (echo 'year,week,count' && cat) | csvlook
```

### sneezes by day. save to intermediate file

```
echo "date,count" > year-one-sneezes-daily.csv && q -H -d "," "select date(timestamp) as day, count(*) from ./year-one-sneezes.csv group by day" >> year-one-sneezes-daily.csv
```

### sneezes summed by day of week (with day count for averaging)

```
q -H -d "," "select strftime('%w', date) as dow, round(avg(count),2) as sneezes_per_day, sum(count) as sneezes, count(date) as days from ./year-one-sneezes-daily.csv group by dow" | (echo 'day,avg,sneezes,days' && cat) | csvlook
```

### most sneezes in one day

```
q -H -d "," "select date, count from ./year-one-sneezes-daily.csv order by count desc limit 10" | (echo 'date,count' && cat) | csvlook
```

### most sneezes in one day (by day of week, 0-6: sun-sat)

```
# sunday
q -H -d "," "select date, count from ./year-one-sneezes-daily.csv where strftime('%w', date) = '0' order by count desc limit 5" | (echo 'date,count' && cat) | csvlook
```

### most sneezes in one day (by month of year, 01-12)

```
# january
q -H -d "," "select date, count from ./year-one-sneezes-daily.csv where strftime('%m', date) = '01' order by count desc limit 5" | (echo 'date,count' && cat) | csvlook
```

### most sneezes in a single hour

```
q -H -d "," "select date(timestamp) as date, strftime('%H', timestamp) as hour, count(*) as count from ./year-one-sneezes.csv group by date, hour order by count desc limit 15" | (echo 'date,hour,count' && cat) | csvlook
```

### most consecutive days with 1+ sneeze

```
date-range 2017-04-23 2018-04-22 | jq -r '.[]' | (echo "date" && cat) | csvjoin -c "1" --outer ./year-one-sneezes-daily.csv - 2>/dev/null | csvcut -c 3,2 | csvsort -c 1 | q -H -d "," "select date2, ifnull(count, 0) from -"| csvjson -H 2>/dev/null | jq ".[] | [.a, .b]" | jq --slurp . | streak --label 0 --column 1 --min 1 | jq -r ".[] | [.start, .end, .value] | @csv" | csvsort -H -c 3 -r 2>/dev/null | sed '1 s/.*/start,end,streak/' | csvlook | head -n 10
```

### most consecutive days with 0 sneezes

```
date-range 2017-04-23 2018-04-22 | jq -r '.[]' | (echo "date" && cat) | csvjoin -c "1" --outer ./year-one-sneezes-daily.csv - 2>/dev/null | csvcut -c 3,2 | csvsort -c 1 | q -H -d "," "select date2, ifnull(count, 0) from -"| csvjson -H 2>/dev/null | jq ".[] | [.a, .b]" | jq --slurp . | streak --label 0 --column 1 --max 0 | jq -r ".[] | [.start, .end, .value] | @csv" | csvsort -H -c 3 -r 2>/dev/null | sed '1 s/.*/start,end,streak/' | csvlook | head -n 10
```

### most sneezes in a 5-day span

```
q -H -d "," "select min(b.date), max(b.date), sum(b.count) as sneezes from ./year-one-sneezes-daily.csv a JOIN ./year-one-sneezes-daily.csv b ON (b.date < date(a.date, '+5 day') and b.date >= a.date) group by a.date order by sneezes desc"  | (echo 'start,end,count' && cat) | csvlook | head -n 10
```


### appendix

prepend a header row: `| (echo "year,month,count" && cat)`
overwrite the header row: `| sed '1 s/.*/start,end,streak/'`
