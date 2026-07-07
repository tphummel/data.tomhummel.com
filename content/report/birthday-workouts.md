---
title: "Birthday Workouts"
date: 2019-07-20T00:17:09-08:00
tags: ["meta", "running", "birthday"]
workouts:
- year: 2026
  location: Beverlywood, Los Angeles, CA
  miles: 7.28
  duration: "58:04"
  climb_ft: 495
  garmin_id: 23511129601
- year: 2025
  note: "No workout. Push-ups only; see nomie"
- year: 2024
  location: Griffith Park, Los Angeles, CA
  miles: 10.35
  duration: "1:37:12"
  climb_ft: 1829
  garmin_id: 16291458055
- year: 2023
  location: Westridge Canyon, Los Angeles, CA
  miles: 6.27
  duration: "1:01:54"
  climb_ft: 1483
  garmin_id: 11508446457
- year: 2022
  location: Los Angeles, CA
  miles: 6.22
  duration: "53:01"
  garmin_id: 9158446101
- year: 2021
  note: "No workout"
- year: 2020
  note: "Peloton ride"
  links:
  - label: 45 minute intervals and arms
    url: https://members.onepeloton.com/profile/workouts/268de23c48c840adbf64bb1eba03ccc6
  - label: 5 minute cool down
    url: https://members.onepeloton.com/profile/workouts/e74cc54760a54d79b9fd275d40484894
- year: 2019
  note: "no workout"
- year: 2018
  location: Los Angeles, CA
  miles: 4.0
  duration: "36:30"
  garmin_id: 2832933782
- year: 2017
  location: Occidental, CA
  miles: 5.0
  duration: "43:44"
  garmin_id: 1840565277
- year: 2016
  note: "no run"
- year: 2015
  note: "no run"
- year: 2014
  location: Marina Del Rey, CA
  miles: 4.0
  duration: "41:00"
  garmin_id: 543552603
- year: 2013
  note: "no run"
- year: 2012
  location: Marina Del Rey, CA
  miles: 6.0
  duration: "58:00"
  garmin_id: 203353913
- year: 2011
  location: Sherman Oaks, CA
  miles: 3.0
  duration: "25:57"
  garmin_id: 97458436
- year: 2010
  location: Santa Monica, CA
  note: gretna green
  miles: 3.01
  duration: "26:43"
  garmin_id: 39809657
- year: 2009
  location: Sherman Oaks, CA
  miles: 5.0
  duration: "35:02"
- year: 2008
  location: Sherman Oaks, CA
  note: 50 min 2500 yds swim
- year: 2007
  location: Montclair, CA
  note: swim 30:02
- year: 2006
  note: "bike to school. Lift arms. Bike home. Stretch roll. Ice left leg."
- year: 2005
  note: "AM - Run 20:31 meeks bay desolation trail. PM - Core 3x100-20-100 + 15 extra pushups."
- year: 2004
  note: open water swim in lake tahoe
- year: 2003
  note: double. Meeks bay trail Tahoe. 64 min 7am. 30 minute 3pm
- year: 2002
  note: "no run"
- year: 2001
  note: "no run, traveling to sf marathon relay on July 8."
- year: 2000
  note: "?"
- year: 1999
  note: "?"
---

{{< summary.inline >}}
<p>Count: {{ len .Page.Params.workouts }}</p>
{{< /summary.inline >}}

<!--more-->

{{< detail.inline >}}

<ul>
{{ range .Page.Params.workouts }}
  {{ $line := printf "%d" .year }}
  {{ if .location }}{{ $line = printf "%s - %s" $line .location }}{{ end }}
  {{ if .note }}{{ $line = printf "%s - %s" $line .note }}{{ end }}
  {{ if .miles }}{{ $line = printf "%s - %v mi" $line .miles }}{{ end }}
  {{ if .duration }}
    {{ if .climb_ft }}
      {{ $line = printf "%s - %s (%s ft climb)" $line .duration (lang.FormatNumber 0 .climb_ft) }}
    {{ else }}
      {{ $line = printf "%s - %s" $line .duration }}
    {{ end }}
  {{ end }}
  {{ if .garmin_id }}
    {{ $line = printf `%s - <a href="https://connect.garmin.com/modern/activity/%v">garmin</a>` $line .garmin_id }}
  {{ end }}
  {{ if .links }}
    {{ $linkHtml := "" }}
    {{ range $i, $l := .links }}
      {{ if $i }}{{ $linkHtml = printf "%s, " $linkHtml }}{{ end }}
      {{ $linkHtml = printf `%s<a href="%s">%s</a>` $linkHtml $l.url $l.label }}
    {{ end }}
    {{ $line = printf "%s - %s" $line $linkHtml }}
  {{ end }}
  <li>{{ $line | safeHTML }}</li>
{{ end }}
</ul>

{{< /detail.inline >}}
