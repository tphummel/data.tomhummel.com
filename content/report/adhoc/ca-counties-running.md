---
title: "California Counties Running"
date: 2026-07-05T00:00:00-08:00
tags: ["running", "checklist", "travel", "meta"]
by_county:
  - county: Alameda
    completed: false
    date: 
    notes: 

  - county: Alpine
    completed: false
    date: 
    notes: 

  - county: Amador
    completed: false
    date: 
    notes: 

  - county: Butte
    completed: false
    date: 
    notes: 

  - county: Calaveras
    completed: false
    date: 
    notes: 

  - county: Colusa
    completed: false
    date: 
    notes: 

  - county: Contra Costa
    completed: false
    date: 
    notes: 

  - county: Del Norte
    completed: false
    date: 
    notes: 

  - county: El Dorado
    completed: false
    date: 
    notes: 

  - county: Fresno
    completed: false
    date: 
    notes: 

  - county: Glenn
    completed: false
    date: 
    notes: 

  - county: Humboldt
    completed: false
    date: 
    notes: 

  - county: Imperial
    completed: false
    date: 
    notes: 

  - county: Inyo
    completed: false
    date: 
    notes: 

  - county: Kern
    completed: false
    date: 
    notes: 

  - county: Kings
    completed: false
    date: 
    notes: 

  - county: Lake
    completed: false
    date: 
    notes: 

  - county: Lassen
    completed: false
    date: 
    notes: 

  - county: Los Angeles
    completed: false
    date: 
    notes: 

  - county: Madera
    completed: false
    date: 
    notes: 

  - county: Marin
    completed: false
    date: 
    notes: 

  - county: Mariposa
    completed: false
    date: 
    notes: 

  - county: Mendocino
    completed: false
    date: 
    notes: 

  - county: Merced
    completed: false
    date: 
    notes: 

  - county: Modoc
    completed: false
    date: 
    notes: 

  - county: Mono
    completed: false
    date: 
    notes: 

  - county: Monterey
    completed: false
    date: 
    notes: 

  - county: Napa
    completed: false
    date: 
    notes: 

  - county: Nevada
    completed: false
    date: 
    notes: 

  - county: Orange
    completed: false
    date: 
    notes: 

  - county: Placer
    completed: false
    date: 
    notes: 

  - county: Plumas
    completed: false
    date: 
    notes: 

  - county: Riverside
    completed: false
    date: 
    notes: 

  - county: Sacramento
    completed: false
    date: 
    notes: 

  - county: San Benito
    completed: false
    date: 
    notes: 

  - county: San Bernardino
    completed: false
    date: 
    notes: 

  - county: San Diego
    completed: false
    date: 
    notes: 

  - county: San Francisco
    completed: false
    date: 
    notes: 

  - county: San Joaquin
    completed: false
    date: 
    notes: 

  - county: San Luis Obispo
    completed: false
    date: 
    notes: 

  - county: San Mateo
    completed: false
    date: 
    notes: 

  - county: Santa Barbara
    completed: false
    date: 
    notes: 

  - county: Santa Clara
    completed: false
    date: 
    notes: 

  - county: Santa Cruz
    completed: false
    date: 
    notes: 

  - county: Shasta
    completed: false
    date: 
    notes: 

  - county: Sierra
    completed: false
    date: 
    notes: 

  - county: Siskiyou
    completed: false
    date: 
    notes: 

  - county: Solano
    completed: false
    date: 
    notes: 

  - county: Sonoma
    completed: false
    date: 
    notes: 

  - county: Stanislaus
    completed: false
    date: 
    notes: 

  - county: Sutter
    completed: false
    date: 
    notes: 

  - county: Tehama
    completed: false
    date: 
    notes: 

  - county: Trinity
    completed: false
    date: 
    notes: 

  - county: Tulare
    completed: false
    date: 
    notes: 

  - county: Tuolumne
    completed: false
    date: 
    notes: 

  - county: Ventura
    completed: false
    date: 
    notes: 

  - county: Yolo
    completed: false
    date: 
    notes: 

  - county: Yuba
    completed: false
    date: 
    notes: 

---
{{< ca-counties-map >}}

{{< summary.inline >}}
<p>Counties Completed: {{ len (where .Page.Params.by_county "completed" true) }}/58</p>
{{< /summary.inline >}}

<!--more-->

{{< detail.inline >}}

<table>
  <tr>
    <th>County</th>
    <th>Completed</th>
    <th>Date</th>
    <th>Note</th>
  </tr>
  {{ range $i, $county := .Page.Params.by_county }}
    <tr>
      <td>{{ $county.county }}</td>
      <td>{{ cond $county.completed "✅" "❌" }}</td>
      <td>{{ $county.date }}</td>
      <td>{{ $county.notes | default "-" }}</td>
    </tr>
  {{ end }}


</table>
{{< /detail.inline >}}
