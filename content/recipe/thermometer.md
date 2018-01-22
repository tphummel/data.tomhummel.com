---
title: "Body Temperature"
date: 2018-01-06T11:15:46-08:00
tags: ["data-exfil"]
---

Take your temperature every morning. Own the data.

<!--more-->

1. Get a [bluetooth-connected, ear thermometer](https://www.amazon.com/Koogeek-Forehead-Thermometer-Bluetooth-Non-Contact/dp/B01LMWD9SY) that feeds data to Apple Health.
1. [export](https://help.apple.com/iphone/10/#/iph27f6325b2) your apple health data
1. convert apple health xml to json for ease
1. slice out temperature data for the date range you care about

```
npm install --global xml2json-command
xml2json < ~/Downloads/apple_health_export/export.xml > apple-health.json

cat apple-health.json | \
  jq '.HealthData.Record | .[] | \
  select((.type == "HKQuantityTypeIdentifierBodyTemperature") \
    and (.creationDate > "2016-12-31") and (.creationDate < "2018-01-01")) | \
  [.creationDate, .value, .unit]' | \
  jq -r '. | @csv' > 2017-temperatures.csv
```

```
cat
...
"2017-12-04 21:29:35 -0800","98.42","degF"
"2017-12-05 07:23:07 -0800","97.16","degF"
"2017-12-06 08:39:52 -0800","96.62","degF"
...
```
