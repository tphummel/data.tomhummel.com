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

  <h2>By Decade</h2>
  {{ $decades := dict "1990s" (slice) "2000s" (slice) "2010s" (slice) "2020s" (slice) }}
  {{ range $runningAnnualReports }}
    {{ $year := .Params.year }}
    {{ if and (ge $year 1990) (lt $year 2000) }}
      {{ $decades = merge $decades (dict "1990s" (index $decades "1990s" | append .)) }}
    {{ else if and (ge $year 2000) (lt $year 2010) }}
      {{ $decades = merge $decades (dict "2000s" (index $decades "2000s" | append .)) }}
    {{ else if and (ge $year 2010) (lt $year 2020) }}
      {{ $decades = merge $decades (dict "2010s" (index $decades "2010s" | append .)) }}
    {{ else if and (ge $year 2020) (lt $year 2030) }}
      {{ $decades = merge $decades (dict "2020s" (index $decades "2020s" | append .)) }}
    {{ end }}
  {{ end }}

  <table>
    <tr>
      <th>Decade</th>
      <th>Run Count</th>
      <th>Mileage</th>
      <th>Minutes</th>
      <th>Ascent (Feet)</th>
    </tr>
  {{ range slice "1990s" "2000s" "2010s" "2020s" }}
    {{ $decade := . }}
    {{ $reports := index $decades $decade }}
    {{ if $reports }}
      {{ $decadeRuns := 0 }}
      {{ $decadeMiles := 0 }}
      {{ $decadeMinutes := 0 }}
      {{ $decadeAscent := 0 }}
      {{ range $reports }}
        {{ $decadeRuns = add $decadeRuns (.Params.total_runs | default 0) }}
        {{ $decadeMiles = add $decadeMiles (.Params.total_miles_run | default 0) }}
        {{ $decadeMinutes = add $decadeMinutes (.Params.total_minutes | default 0) }}
        {{ $decadeAscent = add $decadeAscent (.Params.total_ascent_feet | default 0) }}
      {{ end }}
      <tr>
        <td>{{ $decade }}</td>
        <td>{{ $decadeRuns | lang.FormatNumber 0 }}</td>
        <td>{{ $decadeMiles | lang.FormatNumber 0 }}</td>
        <td>{{ $decadeMinutes | lang.FormatNumber 0 }}</td>
        <td>{{ $decadeAscent | lang.FormatNumber 0 }}</td>
      </tr>
    {{ end }}
  {{ end }}
  </table>

  <h2>By Age</h2>
  {{ $ages := dict "Teens" (slice) "20s" (slice) "30s" (slice) "40s" (slice) }}
  {{ range $runningAnnualReports }}
    {{ $year := .Params.year }}
    {{ if and (ge $year 1998) (lt $year 2005) }}
      {{ $ages = merge $ages (dict "Teens" (index $ages "Teens" | append .)) }}
    {{ else if and (ge $year 2005) (lt $year 2015) }}
      {{ $ages = merge $ages (dict "20s" (index $ages "20s" | append .)) }}
    {{ else if and (ge $year 2015) (lt $year 2025) }}
      {{ $ages = merge $ages (dict "30s" (index $ages "30s" | append .)) }}
    {{ else if ge $year 2025 }}
      {{ $ages = merge $ages (dict "40s" (index $ages "40s" | append .)) }}
    {{ end }}
  {{ end }}

  <table>
    <tr>
      <th>Age Range</th>
      <th>Run Count</th>
      <th>Mileage</th>
      <th>Minutes</th>
      <th>Ascent (Feet)</th>
    </tr>
  {{ range slice "Teens" "20s" "30s" "40s" }}
    {{ $ageRange := . }}
    {{ $reports := index $ages $ageRange }}
    {{ if $reports }}
      {{ $ageRuns := 0 }}
      {{ $ageMiles := 0 }}
      {{ $ageMinutes := 0 }}
      {{ $ageAscent := 0 }}
      {{ range $reports }}
        {{ $ageRuns = add $ageRuns (.Params.total_runs | default 0) }}
        {{ $ageMiles = add $ageMiles (.Params.total_miles_run | default 0) }}
        {{ $ageMinutes = add $ageMinutes (.Params.total_minutes | default 0) }}
        {{ $ageAscent = add $ageAscent (.Params.total_ascent_feet | default 0) }}
      {{ end }}
      <tr>
        <td>{{ $ageRange }}</td>
        <td>{{ $ageRuns | lang.FormatNumber 0 }}</td>
        <td>{{ $ageMiles | lang.FormatNumber 0 }}</td>
        <td>{{ $ageMinutes | lang.FormatNumber 0 }}</td>
        <td>{{ $ageAscent | lang.FormatNumber 0 }}</td>
      </tr>
    {{ end }}
  {{ end }}
  </table>

  <h2>By Year</h2>
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
