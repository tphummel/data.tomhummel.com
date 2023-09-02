---
title: Running
date: 2022-12-10T06:35:00Z
tags: ["meta","running"]
---

{{< om.inline >}}
  {{ $runningAnnualReports := where (index .Site.Taxonomies.tags "running-annual").Pages "Section" "report" }}

  {{ $allTimeMilesRun := 0 }}
  {{ $allTimeRunCount := 0 }}
  {{ $allTimeMinutes := 0 }}
  {{ $allTimeAscentFeet := 0 }}
  {{ $minYear := 10000 }}
  {{ $maxYear := 0 }}

  {{ range $runningAnnualReports }}
    {{ $allTimeMilesRun = add $allTimeMilesRun (.Params.total_miles_run | default 0) }}
    {{ $allTimeRunCount = add $allTimeRunCount (.Params.total_runs | default 0) }}
    {{ $allTimeMinutes = add $allTimeMinutes (.Params.total_minutes | default 0) }}
    {{ $allTimeAscentFeet = add $allTimeAscentFeet (.Params.total_ascent_feet | default 0) }}
    {{ if lt .Params.year $minYear }}
      {{ $minYear = .Params.year }}
    {{ end }}

    {{ if gt .Params.year $maxYear }}
      {{ $maxYear = .Params.year }}
    {{ end }}
  {{ end }}


  <p>Total Runs: <strong>{{ $allTimeRunCount | lang.FormatNumber 0 }}</strong></p>
  <p>Total Miles: <strong>{{ $allTimeMilesRun | lang.FormatNumber 0 }}</strong></p>
  {{ $hours := math.Floor (float (div $allTimeMinutes 60)) }}
  {{ $modMinutes := mod $allTimeMinutes 60 }}
  <p>Total Duration: <strong>{{ $hours | lang.FormatNumber 0 }} hours</strong></p>
  <p>Total Ascent: <strong>{{ $allTimeAscentFeet | lang.FormatNumber 0 }} feet (Since 2010)</strong></p>
  {{ $milesPerHour := (div $allTimeMilesRun $hours) }}
  {{ $milePace := div 60 $milesPerHour }}
  {{ $milePaceMinutes := math.Floor $milePace }}
  {{ $milePaceSeconds := math.Floor (mul (sub $milePace $milePaceMinutes) 60) }}
  <p>Mile Pace: <strong>{{ $milePaceMinutes | lang.FormatNumber 0 }}:{{ printf "%02d" (int $milePaceSeconds) }}</strong></p>
  <p>Years: {{ $minYear }} - {{ $maxYear }}</p>
  <table>
    <tr>
      <th>Year</th>
      <th>Run Count</th>
      <th>Mileage</th>
      <th>Minutes</th>
      <th>Ascent (Feet)</th>
    </tr>
  {{ range ($runningAnnualReports.ByParam "year").Reverse }}
    <tr>
      <td>{{ .Params.year }}</td>
      <td>{{ (.Params.total_runs | default 0) | lang.FormatNumber 0 }}{{ cond (.Params.partial_data | default false) "*" "" }}</td>
      <td>{{ (.Params.total_miles_run | default 0) | lang.FormatNumber 0 }}{{ cond (.Params.partial_data | default false) "*" "" }}</td>
      <td>{{ (.Params.total_minutes | default 0) | lang.FormatNumber 0 }}{{ cond (.Params.partial_data | default false) "*" "" }}</td>
      <td>{{ (.Params.total_ascent_feet | default 0) | lang.FormatNumber 0 }}{{ cond (.Params.partial_data | default false) "*" "" }}</td>
    </tr>
  {{ end }}
  </table>

  <p>* Partial Data</p>
{{< /om.inline >}}
