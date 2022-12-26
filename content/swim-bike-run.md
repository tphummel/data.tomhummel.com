---
title: Swim Bike Run
date: 2022-12-25T06:35:00Z
tags: ["meta"]
---

I'm not a triathlete. 

{{< om.inline >}}
  {{ $runningAnnualReports := where (index .Site.Taxonomies.tags "running-annual").Pages "Section" "report" }}
  {{ $runMinutesByYear := dict }}
  {{ range $runningAnnualReports }}
    {{ $runMinutesByYear = $runMinutesByYear | merge (dict (string .Params.year) .Params.total_minutes) }}
  {{ end }}

  {{ $swimmingAnnualReports := where (index .Site.Taxonomies.tags "swimming-annual").Pages "Section" "report" }}
  {{ $swimMinutesByYear := dict }}
  {{ range $swimmingAnnualReports }}
    {{ $swimMinutesByYear = $swimMinutesByYear | merge (dict (string .Params.year) .Params.total_minutes) }}
  {{ end }}

  {{ $bikingAnnualReports := where (index .Site.Taxonomies.tags "biking-annual").Pages "Section" "report" }}
  {{ $bikeMinutesByYear := dict }}
  {{ range $bikingAnnualReports }}
    {{ $bikeMinutesByYear = $bikeMinutesByYear | merge (dict (string .Params.year) .Params.total_minutes) }}
  {{ end }}

  {{ $minYear := 10000 }}
  {{ $maxYear := 0 }}
  {{ $totalRunMinutes := 0 }}
  {{ $totalSwimMinutes := 0 }}
  {{ $totalBikeMinutes := 0 }}

  {{ range $runningAnnualReports }}
    {{ $totalRunMinutes = add $totalRunMinutes (.Params.total_minutes | default 0) }}
    {{ $totalSwimMinutes = add $totalSwimMinutes ((index $swimMinutesByYear (string .Params.year)) | default 0) }}
    {{ $totalBikeMinutes = add $totalBikeMinutes ((index $bikeMinutesByYear (string .Params.year)) | default 0) }}
    {{ if lt .Params.year $minYear }}
      {{ $minYear = .Params.year }}
    {{ end }}

    {{ if gt .Params.year $maxYear }}
      {{ $maxYear = .Params.year }}
    {{ end }}
  {{ end }}

  <p><strong>Years:</strong> {{ $minYear }} - {{ $maxYear }}</p>
  <p><strong>Swim Minutes: </strong>{{ $totalSwimMinutes | lang.FormatNumber 0 }}</p>
  <p><strong>Bike Minutes: </strong>{{ $totalBikeMinutes | lang.FormatNumber 0 }}</p>
  <p><strong>Run Minutes: </strong>{{ $totalRunMinutes | lang.FormatNumber 0 }}</p>
  <table>
    <tr>
      <th>Year</th>
      <th>Total Swim Minutes</th>
      <th>Total Bike Minutes</th>
      <th>Total Run Minutes</th>
    </tr>
  {{ range ($runningAnnualReports.ByParam "year").Reverse }}
    <tr>
      <td>{{ .Params.year }}</td>
      <td>{{ ((index $swimMinutesByYear (string .Params.year)) | default 0) | lang.FormatNumber 0 }}</td>
      <td>{{ ((index $bikeMinutesByYear (string .Params.year)) | default 0) | lang.FormatNumber 0 }}</td>
      <td>{{ (.Params.total_minutes | default 0) | lang.FormatNumber 0 }}{{ cond (.Params.partial_data | default false) "*" "" }}</td>
    </tr>
  {{ end }}
  </table>

  <p>* Partial Data</p>
{{< /om.inline >}}
