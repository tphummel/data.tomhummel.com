---
title: "US States Running Checklist"
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
    completed: false
    date: 
    notes: 

  - state: Arkansas
    completed: false
    date: 
    notes: 

  - state: California
    completed: true
    date: 
    notes: 

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
    completed: false
    date: 
    notes: 

  - state: Idaho
    completed: false
    date: 
    notes: 

  - state: Illinois
    completed: false
    date: 
    notes: 

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
    completed: false
    date: 
    notes: 

  - state: Maryland
    completed: false
    date: 
    notes: 

  - state: Massachusetts
    completed: false
    date: 
    notes: 

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
    completed: false
    date: 
    notes: 

  - state: New Hampshire
    completed: false
    date: 
    notes: 

  - state: New Jersey
    completed: false
    date: 
    notes: 

  - state: New Mexico
    completed: false
    date: 
    notes: 

  - state: New York
    completed: false
    date: 
    notes: 

  - state: North Carolina
    completed: false
    date: 
    notes: 

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
    completed: false
    date: 
    notes: 

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
    completed: false
    date: 
    notes: 




---

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
      <td>{{ $state.date | default "-" }}</td>
      <td>{{ $state.notes | default "-" }}</td>
    </tr>
  {{ end }}


</table>
{{< /om.inline >}}

