---
title: "Lahaina Pali Trail Running"
date: '2026-07-27T00:00:00Z'
tags: ["running", "trail", "maui", "hawaii"]
trail:
  name: Lahaina Pali Trail
  system: "Nā Ala Hele — Hawaiʻi Trail & Access System"
  length_mi: 4.8
  elev_gain_ft: 1630
  elev_loss_ft: 1407
  trailheads:
  - key: east
    name: "Māʻalaea (East) Trailhead"
    address: "Dirt road off Hwy 30, just south of the Hwy 30 / Hwy 380 junction, ~2.5 mi south of Wailuku"
  - key: west
    name: "Ukumehame (West) Trailhead"
    address: "Highway 30 pullout ~0.25 mi north of the Lāhainā Pali Tunnel, ~3 mi west of Māʻalaea Harbor"
runs:
- date: '2026-07-25'
  garmin_id: 23729568728
  name: Lahaina Pali Trail from Māʻalaea (East) Trailhead
  trailhead: east
  miles: 4.02
  elev_gain_ft: 1401
  elev_loss_ft: 1395
  elev_min_ft: 207
  elev_max_ft: 1585
  duration: 1:07:55
  avg_pace: 16:54/mi
  avg_hr: 137
  max_hr: 170
  calories: 754
  start_lat: 20.80737
  start_lon: -156.51289
  turnaround_lat: 20.80041
  turnaround_lon: -156.53671
  laps:
  - mile: 1
    distance_mi: 1.0
    time: 21:15
    pace: 21:15/mi
    avg_hr: 147
    max_hr: 170
    calories: 310
  - mile: 2
    distance_mi: 1.0
    time: 13:38
    pace: 13:38/mi
    avg_hr: 162
    max_hr: 170
    calories: 224
  - mile: 3
    distance_mi: 1.0
    time: 13:06
    pace: 13:06/mi
    avg_hr: 127
    max_hr: 153
    calories: 116
  - mile: 4
    distance_mi: 1.0
    time: 19:41
    pace: 19:41/mi
    avg_hr: 114
    max_hr: 133
    calories: 102
  - mile: 5
    distance_mi: 0.02
    time: 0:15
    pace:
    avg_hr: 121
    max_hr: 121
    calories: 2
  notes: ''
- date: '2026-07-27'
  garmin_id: 23753377382
  name: Lahaina Pali Trail from Ukumehame (West) Trailhead
  trailhead: west
  miles: 5.32
  elev_gain_ft: 1789
  elev_loss_ft: 1793
  elev_min_ft: 38
  elev_max_ft: 1607
  duration: 1:30:04
  avg_pace: 16:56/mi
  avg_hr: 133
  max_hr: 167
  calories: 946
  start_lat: 20.79196
  start_lon: -156.5638
  turnaround_lat: 20.79947
  turnaround_lon: -156.53791
  laps:
  - mile: 1
    distance_mi: 1.0
    time: 18:32
    pace: 18:32/mi
    avg_hr: 147
    max_hr: 163
    calories: 271
  - mile: 2
    distance_mi: 1.0
    time: 17:50
    pace: 17:50/mi
    avg_hr: 152
    max_hr: 165
    calories: 257
  - mile: 3
    distance_mi: 1.0
    time: 13:52
    pace: 13:52/mi
    avg_hr: 143
    max_hr: 167
    calories: 175
  - mile: 4
    distance_mi: 1.0
    time: 14:54
    pace: 14:54/mi
    avg_hr: 119
    max_hr: 149
    calories: 113
  - mile: 5
    distance_mi: 1.0
    time: 19:46
    pace: 19:46/mi
    avg_hr: 112
    max_hr: 127
    calories: 99
  - mile: 6
    distance_mi: 0.32
    time: 5:10
    pace: 16:12/mi
    avg_hr: 113
    max_hr: 125
    calories: 31
  notes: ''
---

{{< summary.inline >}}
{{ $runs := .Page.Params.runs }}
{{ $miles := 0.0 }}{{ range $runs }}{{ $miles = add $miles .miles }}{{ end }}
<p>Lahaina Pali Trail (Maui): <strong>complete</strong> — {{ len $runs }} runs, {{ $miles | lang.FormatNumber 1 }} mi, one from each trailhead, meeting near the mid-trail high point.</p>
{{< /summary.inline >}}

<!--more-->

{{< detail.inline >}}

<h2>Lahaina Pali Trail</h2>

<p>The <a href="https://dlnr.hawaii.gov/dtoh/trails/na-ala-hele/">Nā Ala Hele</a> Lahaina Pali Trail crosses the West Maui Mountains between Māʻalaea and Ukumehame, {{ .Page.Params.trail.length_mi }} mi one-way with about {{ .Page.Params.trail.elev_gain_ft | lang.FormatNumber 0 }} ft of gain and {{ .Page.Params.trail.elev_loss_ft | lang.FormatNumber 0 }} ft of loss between trailheads, both near sea level. Ran as two out-and-back trips, one from each end, meeting near the same mid-trail high point — in aggregate, every mile of the trail covered.</p>

<img src="/images/lahaina-pali/overview.png" alt="Lahaina Pali Trail overview map" style="width:100%;max-width:900px;">

<table>
  <tr><th>Trailhead</th><th>Access</th></tr>
  {{ range .Page.Params.trail.trailheads }}
  <tr>
    <td>{{ .name }}</td>
    <td>{{ .address }}</td>
  </tr>
  {{ end }}
</table>

{{ $runs := .Page.Params.runs }}
{{ $totalMiles := 0.0 }}{{ range $runs }}{{ $totalMiles = add $totalMiles .miles }}{{ end }}
{{ $totalGain := 0 }}{{ range $runs }}{{ $totalGain = add $totalGain .elev_gain_ft }}{{ end }}
{{ $totalCal := 0 }}{{ range $runs }}{{ $totalCal = add $totalCal .calories }}{{ end }}

<h3>Combined</h3>
<table>
  <tr><th>Runs</th><th>Miles</th><th>Elev Gain</th><th>Calories</th></tr>
  <tr>
    <td>{{ len $runs }}</td>
    <td>{{ $totalMiles | lang.FormatNumber 2 }}</td>
    <td>{{ $totalGain | lang.FormatNumber 0 }} ft</td>
    <td>{{ $totalCal | lang.FormatNumber 0 }}</td>
  </tr>
</table>

{{ range $runs }}
<h3>{{ .name }} — {{ .date }}</h3>
<img src="/images/lahaina-pali/{{ .date }}-{{ .trailhead }}-elev.png" alt="Elevation profile: {{ .name }}" style="width:100%;max-width:900px;">

<table>
  <tr>
    <th>Miles</th><th>Time</th><th>Avg Pace</th><th>Elev Gain</th><th>Elev Loss</th>
    <th>Elev Range</th><th>Avg HR</th><th>Max HR</th><th>Calories</th>
  </tr>
  <tr>
    <td>{{ .miles }}</td>
    <td>{{ .duration }}</td>
    <td>{{ .avg_pace }}</td>
    <td>{{ .elev_gain_ft | lang.FormatNumber 0 }} ft</td>
    <td>{{ .elev_loss_ft | lang.FormatNumber 0 }} ft</td>
    <td>{{ .elev_min_ft | lang.FormatNumber 0 }}&ndash;{{ .elev_max_ft | lang.FormatNumber 0 }} ft</td>
    <td>{{ .avg_hr }} bpm</td>
    <td>{{ .max_hr }} bpm</td>
    <td>{{ .calories }}</td>
  </tr>
</table>

<p>Splits — <a href="https://connect.garmin.com/modern/activity/{{ .garmin_id }}">Garmin activity {{ .garmin_id }}</a>{{ with .notes }}. {{ . }}{{ end }}</p>
<table>
  <tr><th>Mile</th><th>Distance</th><th>Time</th><th>Pace</th><th>Avg HR</th><th>Max HR</th><th>Calories</th></tr>
  {{ range .laps }}
  <tr>
    <td>{{ .mile }}</td>
    <td>{{ .distance_mi }} mi</td>
    <td>{{ .time }}</td>
    <td>{{ .pace | default "—" }}</td>
    <td>{{ .avg_hr }} bpm</td>
    <td>{{ .max_hr }} bpm</td>
    <td>{{ .calories }}</td>
  </tr>
  {{ end }}
</table>
{{ end }}

{{< /detail.inline >}}
