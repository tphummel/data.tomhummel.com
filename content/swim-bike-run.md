---
title: Swim Bike Run
date: 2022-12-25T06:35:00Z
tags: ["meta"]
---

{{< om.inline >}}
  {{ $annualTemplate := dict "swimMinutes" 0 "bikeMinutes" 0 "runMinutes" 0 }}



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

  {{ $minYear := 10000 }}
  {{ $maxYear := 0 }}
  {{ $totalRunMinutes := 0 }}
  {{ $totalSwimMinutes := 0 }}

  {{ range $runningAnnualReports }}
    {{ $totalRunMinutes = add $totalRunMinutes (.Params.total_minutes | default 0) }}
    {{ $totalSwimMinutes = add $totalSwimMinutes ((index $swimMinutesByYear (string .Params.year)) | default 0) }}
    {{ if lt .Params.year $minYear }}
      {{ $minYear = .Params.year }}
    {{ end }}

    {{ if gt .Params.year $maxYear }}
      {{ $maxYear = .Params.year }}
    {{ end }}
  {{ end }}

  <p>Years: {{ $minYear }} - {{ $maxYear }}</p>
  <table>
    <tr>
      <th>Year</th>
      <th>Swim Minutes</th>
      <th>Bike Minutes</th>
      <th>Run Minutes</th>
    </tr>
  {{ range ($runningAnnualReports.ByParam "year").Reverse }}
    <tr>
      <td>{{ .Params.year }}</td>
      <td>{{ ((index $swimMinutesByYear (string .Params.year)) | default 0) | lang.FormatNumber 0 }}</td>
      <td> - </td>
      <td>{{ (.Params.total_minutes | default 0) | lang.FormatNumber 0 }}{{ cond (.Params.partial_data | default false) "*" "" }}</td>
    </tr>
  {{ end }}
  </table>

  <p>* Partial Data</p>
{{< /om.inline >}}
