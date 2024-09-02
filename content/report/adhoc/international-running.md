---
title: "International Running"
date: 2023-06-11T05:30:00-08:00
tags: ["running", "checklist", "travel", "meta"]
by_country:
  - name: France
    date: 2023-01-29
    notes: Paris
  - name: Italy
    date: 2016-05-21
    notes: Rome
  - name: Ireland
    date: 2016-12-29
    notes: Doolin, County Clare
  - name: Thailand
    date: 2014-04-30
    notes: Koh Samui
  - name: Hong Kong
    date: 2014-04-26
    notes: HK Island central coastline
  - name: Canada
    date: 2018-07-20
    notes: Edmonton, Alberta
  - name: Mexico
    date: 2017-11-10
    notes: Todos Santos, Baja California Sur
  - name: Spain
    date: 2019-03-13
    notes: Getaria, Gipuzkoa
  - name: Belize
    date: 2014-11-13
    notes: San Pedro, Ambergris Caye
  - name: England
    date: 2024-07-29
    notes: London
  - name: Denmark
    date: 2024-08-03
    notes: Copenhagen
  - name: Sweden
    date: 2024-08-08
    notes: Stockholm

---
{{< summary.inline >}}
<p>Countries Completed: {{ len .Page.Params.by_country }}</p>
{{< /summary.inline >}}
<!--more-->

{{< detail.inline >}}

<table>
  <tr>
    <th>Country</th>
    <th>Date</th>
    <th>Note</th>
  </tr>
  {{ range $i, $country := .Page.Params.by_country }}
    <tr>
      <td>{{ $country.name }}</td>
      <td>{{ $country.date }}</td>
      <td>{{ $country.notes | default "" }}</td>
    </tr>
  {{ end }}

</table>
{{< /detail.inline >}}

