---
title: Sneezes
date: 2022-04-13T09:00:00Z
tags: ["meta"]
---

{{< om.inline >}}
  {{ $sneezeAnnualReports := where (index .Site.Taxonomies.tags "sneezes-annual").Pages "Section" "report" }}

  {{ $allTimeSneezes := 0 }}
  {{ $minYear := 10000 }}
  {{ $maxYear := 0 }}

  {{ range $sneezeAnnualReports }}
    {{ $allTimeSneezes = add $allTimeSneezes .Params.totalSneezes }}
    {{ if lt .Params.year $minYear }}
      {{ $minYear = .Params.year }}
    {{ end }}

    {{ if gt .Params.year $maxYear }}
      {{ $maxYear = .Params.year }}
    {{ end }}
  {{ end }}


  <p>All Time: <strong>{{ $allTimeSneezes | lang.FormatNumber 0 }}</strong> Sneezes</p>
  <p>Years: {{ $minYear }} - {{ $maxYear }}</p>
  <table>
    <tr>
      <th>Year</th>
      <th>Sneezes</th>
    </tr>
  {{ range $sneezeAnnualReports.Reverse }}
    <tr>
      <td>{{ .Params.year }}</td>
      <td>{{ .Params.totalSneezes | lang.FormatNumber 0 }}{{ cond (.Params.partialData | default false) "*" "" }}</td>
    </tr>
  {{ end }}
  </table>

  <p>* Partial Data</p>
{{< /om.inline >}}
