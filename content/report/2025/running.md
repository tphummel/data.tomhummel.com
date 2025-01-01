---
title: "2025 Running"
date: 2025-01-01
tags: ["running", "running-annual"]
total_miles_run: 0
total_runs: 0
total_minutes: 0
total_ascent_feet: 0
partial_data: false
weekly_goal_miles: 4.0
by_week:

---

<!--more-->

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
    <th>Net Pace</th>
  </tr>
  {{ $running_total_miles := 0 }}
  {{ range $i, $week := .Page.Params.by_week }}
    {{ $week_num := add $i 1 }}
    {{ $running_total_miles = add $running_total_miles ($week.miles | default 0) }}
    {{ $goal_through_week_miles := mul $.Page.Params.weekly_goal_miles $week_num }}
    <tr>
      <td>{{ $week_num }}</td>
      <td>{{ time $week.start | time.Format "Mon Jan 2" }}</td>
      <td>{{ time $week.end | time.Format "Mon Jan 2" }}</td>
      <td>{{ $week.miles }}</td>
      <td>{{ cond (gt $week.miles $.Page.Params.weekly_goal_miles) "✅" "❌" }}</td>
      <td>{{ (sub $running_total_miles $goal_through_week_miles ) | lang.FormatNumber 1 }}</td>
    </tr>
  {{ end }}


</table>
{{< /om.inline >}}
