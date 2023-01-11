---
title: "2023 Running"
date: 2023-01-04T16:30:00-08:00
tags: ["running", "running-annual"]
total_miles_run: 21.61
total_runs: 4
total_minutes: 180.5
partial_data: true
weekly_goal_miles: 9.0
by_week:
  - start: 2023-01-01
    end: 2023-01-07
    miles: 12.11
  - start: 2023-01-08
    end: 2023-01-15
    miles: 9.5
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

