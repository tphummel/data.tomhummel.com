---
title: Running
date: 2022-12-10T06:35:00Z
---

{{< om.inline >}}
  {{ $runningAnnualReports := where (index .Site.Taxonomies.tags "running-annual").Pages "Section" "report" }}

  {{ $allTimeMilesRun := 0 }}
  {{ $allTimeRunCount := 0 }}
  {{ $minYear := 10000 }}
  {{ $maxYear := 0 }}

  {{ range $runningAnnualReports }}
    {{ $allTimeMilesRun = add $allTimeMilesRun (.Params.total_miles_run | default 0) }}
    {{ $allTimeRunCount = add $allTimeRunCount (.Params.total_runs | default 0) }}
    {{ if lt .Params.year $minYear }}
      {{ $minYear = .Params.year }}
    {{ end }}

    {{ if gt .Params.year $maxYear }}
      {{ $maxYear = .Params.year }}
    {{ end }}
  {{ end }}


  <p>All Time Runs: <strong>{{ $allTimeRunCount | lang.FormatNumber 0 }}</strong></p>
  <p>All Time Mileage: <strong>{{ $allTimeMilesRun | lang.FormatNumber 0 }}</strong></p>
  <p>Years: {{ $minYear }} - {{ $maxYear }}</p>
  <table>
    <tr>
      <th>Year</th>
      <th>Run Count</th>
      <th>Mileage</th>
    </tr>
  {{ range $runningAnnualReports.Reverse }}
    <tr>
      <td>{{ .Params.year }}</td>
      <td>{{ (.Params.total_runs | default 0) | lang.FormatNumber 0 }}{{ cond (.Params.partial_data | default false) "*" "" }}</td>
      <td>{{ (.Params.total_miles_run | default 0) | lang.FormatNumber 0 }}{{ cond (.Params.partial_data | default false) "*" "" }}</td>
    </tr>
  {{ end }}
  </table>

  <p>* Partial Data</p>
{{< /om.inline >}}
