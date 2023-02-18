---
title: "2023 Running"
date: 2023-01-04T16:30:00-08:00
tags: ["running", "running-annual"]
total_miles_run: 68.0
total_runs: 13
total_minutes: 575
partial_data: true
weekly_goal_miles: 9.0
by_week:
  - start: 2023-01-01
    end: 2023-01-07
    miles: 12.11
  - start: 2023-01-08
    end: 2023-01-14
    miles: 9.5
  - start: 2023-01-15
    end: 2023-01-21
    miles: 10.20
  - start: 2023-01-22
    end: 2023-01-28
    miles: 9.03
  - start: 2023-01-29
    end: 2023-02-04
    miles: 9.01
  - start: 2023-02-05
    end: 2023-02-11
    miles: 9.12
  - start: 2023-02-12
    end: 2023-02-18
    miles: 9.32
---

{{< om.inline >}}
<p>Total Runs: {{ .Page.Params.total_runs }}</p>
<p>Total Miles: {{ .Page.Params.total_miles_run }}</p>
<p>Total Minutes: {{ .Page.Params.total_minutes }}</p>

<table>
  <tr>
    <th>Week #</th>
    <th>Start</th>
    <th>End</th>
    <th>Miles</th>
    <th>Goal Complete</th>
  </tr>
  {{ range $i, $week := .Page.Params.by_week }}
    <tr>
      <td>{{ add $i 1 }}</td>
      <td>{{ time $week.start | time.Format "Mon Jan 2" }}</td>
      <td>{{ time $week.end | time.Format "Mon Jan 2" }}</td>
      <td>{{ $week.miles }}</td>
      <td>{{ cond (gt $week.miles $.Page.Params.weekly_goal_miles) "✅" "❌" }}</td>
    </tr>
  {{ end }}


</table>
{{< /om.inline >}}

