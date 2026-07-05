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
    completed: true
    date: 2001-09-09
    notes: Muir Woods and the Dipsea Trail

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
    completed: true
    date: 2001-07-10
    notes: First journal entry. Old ladies house.

  - county: Orange
    completed: true
    date: 2001-09-28
    notes: Brea Olinda XC Invite

  - county: Placer
    completed: true
    date: 2001-05-12
    notes: Save A Life 5k, Auburn, CA

  - county: Plumas
    completed: false
    date: 
    notes: 

  - county: Riverside
    completed: false
    date: 
    notes: 

  - county: Sacramento
    completed: true
    date: 2001-06-08
    notes: Friday Night 5k

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
    completed: true
    date: 2001-07-08
    notes: San Francisco Marathon relay

  - county: San Joaquin
    completed: false
    date: 
    notes: 

  - county: San Luis Obispo
    completed: true
    date: 1998-10-17
    notes: Cal Poly XC Invite

  - county: San Mateo
    completed: true
    date: 1998-05-17
    notes: San Carlos Hometown Days run

  - county: Santa Barbara
    completed: false
    date: 
    notes: 

  - county: Santa Clara
    completed: true
    date: 1999-07-01
    notes: Los Gatos High School all comers meet

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
