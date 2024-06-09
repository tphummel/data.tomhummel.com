---
title: Pushups
date: 2024-06-09T09:00:00Z
tags: ["meta"]
---

{{< om.inline >}}
  {{ $pushupAnnualReports := where (index .Site.Taxonomies.tags "pushups-annual").Pages "Section" "report" }}

  {{ $allTimepushups := 0 }}
  {{ $minYear := 10000 }}
  {{ $maxYear := 0 }}

  {{ range $pushupAnnualReports }}
    {{ $allTimepushups = add $allTimepushups .Params.total_pushups }}
    {{ if lt .Params.year $minYear }}
      {{ $minYear = .Params.year }}
    {{ end }}

    {{ if gt .Params.year $maxYear }}
      {{ $maxYear = .Params.year }}
    {{ end }}
  {{ end }}


  <p>All Time: <strong>{{ $allTimepushups | lang.FormatNumber 0 }}</strong> pushups</p>
  <p>Years: {{ $minYear }} - {{ $maxYear }}</p>
  <table>
    <tr>
      <th>Year</th>
      <th>pushups</th>
    </tr>
  {{ range $pushupAnnualReports.Reverse }}
    <tr>
      <td>{{ .Params.year }}</td>
      <td>{{ .Params.total_pushups | lang.FormatNumber 0 }}{{ cond (.Params.partial_data | default false) "*" "" }}</td>
    </tr>
  {{ end }}
  </table>

  <p>* Partial Data</p>
{{< /om.inline >}}
