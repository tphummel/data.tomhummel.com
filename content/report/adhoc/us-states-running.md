---
title: "US States Running"
date: 2023-06-09T16:30:00-08:00
tags: ["running", "checklist"]
by_state:
  - state: Alabama
    completed: false
    date: 
    notes: 

  - state: Alaska
    completed: false
    date: 
    notes: 

  - state: Arizona
    completed: true
    date: 2007-04-22
    notes: Carefree, AZ

  - state: Arkansas
    completed: false
    date: 
    notes: 

  - state: California
    completed: true
    date: 1998-05-17
    notes: Just chose an early date from log. 99.9999% of my running is in California. 

  - state: Colorado
    completed: false
    date: 
    notes: 

  - state: Connecticut
    completed: false
    date: 
    notes: 

  - state: Delaware
    completed: false
    date: 
    notes: 

  - state: Florida
    completed: false
    date: 
    notes: 

  - state: Georgia
    completed: false
    date: 
    notes: 

  - state: Hawaii
    completed: true
    date: 2002-12-15
    notes: Maui

  - state: Idaho
    completed: true
    date: 2011-06-09
    notes: Boise. 6/11, 6/12. 

  - state: Illinois
    completed: true
    date: 2005-07-13
    notes: Caseyville, IL

  - state: Indiana
    completed: false
    date: 
    notes: 

  - state: Iowa
    completed: false
    date: 
    notes: 

  - state: Kansas
    completed: false
    date: 
    notes: 

  - state: Kentucky
    completed: false
    date: 
    notes: 

  - state: Louisiana
    completed: false
    date: 
    notes: 

  - state: Maine
    completed: true
    date: 2023-06-06
    notes: Kennibunkport. 2023-06-08

  - state: Maryland
    completed: true
    date: 2003-11-26
    notes: Silver Spring

  - state: Massachusetts
    completed: true
    date: 2013-04-24
    notes: Boston Commons. 2023-04-25 Charles River

  - state: Michigan
    completed: false
    date: 
    notes: 

  - state: Minnesota
    completed: false
    date: 
    notes: 

  - state: Mississippi
    completed: false
    date: 
    notes: 

  - state: Missouri
    completed: false
    date: 
    notes: 

  - state: Montana
    completed: false
    date: 
    notes: 

  - state: Nebraska
    completed: false
    date: 
    notes: 

  - state: Nevada
    completed: true
    date: 2002-02-16
    notes: Holiday Inn Classic, Reno. 

  - state: New Hampshire
    completed: false
    date: 
    notes: 

  - state: New Jersey
    completed: false
    date: 
    notes: 

  - state: New Mexico
    completed: true
    date: 2017-12-18
    notes: Santa Fe. 12/22, 12/23, 12/25 Taos. 

  - state: New York
    completed: false
    date: 
    notes: 

  - state: North Carolina
    completed: true
    date: 2003-11-22
    notes: Cary. 2003-11-23 New Bern. 2003-11-24 Ocracoke.

  - state: North Dakota
    completed: false
    date: 
    notes: 

  - state: Ohio
    completed: false
    date: 
    notes: 

  - state: Oklahoma
    completed: false
    date: 
    notes: 

  - state: Oregon
    completed: false
    date: 
    notes: 

  - state: Pennsylvania
    completed: false
    date: 
    notes: 

  - state: Rhode Island
    completed: false
    date: 
    notes: 

  - state: South Carolina
    completed: false
    date: 
    notes: 

  - state: South Dakota
    completed: false
    date: 
    notes: 

  - state: Tennessee
    completed: false
    date: 
    notes: 

  - state: Texas
    completed: false
    date: 
    notes: 

  - state: Utah
    completed: false
    date: 
    notes: 

  - state: Vermont
    completed: false
    date: 
    notes: 

  - state: Virginia
    completed: true
    date: 2005-07-14
    notes: Salem. Williamsburg

  - state: Washington
    completed: false
    date: 
    notes: 

  - state: West Virginia
    completed: false
    date: 
    notes: 

  - state: Wisconsin
    completed: false
    date: 
    notes: 

  - state: Wyoming
    completed: true
    date: 2005-07-12
    notes: US-80. Either exit 260 or 255.

---

<!--more-->

{{< om.inline >}}

<p>States Completed: {{ len (where .Page.Params.by_state "completed" true) }}</p>

<table>
  <tr>
    <th>State</th>
    <th>Completed</th>
    <th>Date</th>
    <th>Note</th>
  </tr>
  {{ range $i, $state := .Page.Params.by_state }}
    <tr>
      <td>{{ $state.state }}</td>
      <td>{{ cond $state.completed "✅" "❌" }}</td>
      <td>{{ $state.date }}</td>
      <td>{{ $state.notes | default "-" }}</td>
    </tr>
  {{ end }}


</table>
{{< /om.inline >}}

