---
title: "2024 Running"
date: 2024-01-01T02:30:00-08:00
tags: ["running", "running-annual"]
total_miles_run: 79.49
total_runs: 18
total_minutes: 656
total_ascent_feet: 2444
partial_data: true
weekly_goal_miles: 11.0
by_week:
  - start: 2023-12-31
    end: 2024-01-06
    miles: 11.06
  - start: 2024-01-07
    end: 2024-01-13
    miles: 11.38
  - start: 2024-01-14
    end: 2024-01-20
    miles: 11.36
  - start: 2024-01-21
    end: 2024-01-27
    miles: 11.95
  - start: 2024-01-28
    end: 2024-02-03
    miles: 11.21
  - start: 2024-02-04
    end: 2024-02-10
    miles: 11.28
  - start: 2024-02-11
    end: 2024-02-17
    miles: 11.26
  - start: 2024-02-18
    end: 2024-02-24
    miles: 0
  - start: 2024-02-25
    end: 2024-03-02
    miles: 0
  - start: 2024-03-03
    end: 2024-03-09
    miles: 0
  - start: 2024-03-10
    end: 2024-03-16
    miles: 0
  - start: 2024-03-17
    end: 2024-03-23
    miles: 0
  - start: 2024-03-24
    end: 2024-03-30
    miles: 0
  - start: 2024-03-31
    end: 2024-04-06
    miles: 0
  - start: 2024-04-07
    end: 2024-04-13
    miles: 0
  - start: 2024-04-14
    end: 2024-04-20
    miles: 0
  - start: 2024-04-21
    end: 2024-04-27
    miles: 0
  - start: 2024-04-28
    end: 2024-05-04
    miles: 0
  - start: 2024-05-05
    end: 2024-05-11
    miles: 0
  - start: 2024-05-12
    end: 2024-05-18
    miles: 0
  - start: 2024-05-19
    end: 2024-05-25
    miles: 0
  - start: 2024-05-26
    end: 2024-06-01
    miles: 0
  - start: 2024-06-02
    end: 2024-06-08
    miles: 0
  - start: 2024-06-09
    end: 2024-06-15
    miles: 0
  - start: 2024-06-16
    end: 2024-06-22
    miles: 0
  - start: 2024-06-23
    end: 2024-06-29
    miles: 0
  - start: 2024-06-30
    end: 2024-07-06
    miles: 0
  - start: 2024-07-07
    end: 2024-07-13
    miles: 0
  - start: 2024-07-14
    end: 2024-07-20
    miles: 0
  - start: 2024-07-21
    end: 2024-07-27
    miles: 0
  - start: 2024-07-28
    end: 2024-08-03
    miles: 0
  - start: 2024-08-04
    end: 2024-08-10
    miles: 0
  - start: 2024-08-11
    end: 2024-08-17
    miles: 0
  - start: 2024-08-18
    end: 2024-08-24
    miles: 0
  - start: 2024-08-25
    end: 2024-08-31
    miles: 0
  - start: 2024-09-01
    end: 2024-09-07
    miles: 0
  - start: 2024-09-08
    end: 2024-09-14
    miles: 0
  - start: 2024-09-15
    end: 2024-09-21
    miles: 0
  - start: 2024-09-22
    end: 2024-09-28
    miles: 0
  - start: 2024-09-29
    end: 2024-10-05
    miles: 0
  - start: 2024-10-06
    end: 2024-10-12
    miles: 0
  - start: 2024-10-13
    end: 2024-10-19
    miles: 0
  - start: 2024-10-20
    end: 2024-10-26
    miles: 0
  - start: 2024-10-27
    end: 2024-11-02
    miles: 0
  - start: 2024-11-03
    end: 2024-11-09
    miles: 0
  - start: 2024-11-10
    end: 2024-11-16
    miles: 0
  - start: 2024-11-17
    end: 2024-11-23
    miles: 0
  - start: 2024-11-24
    end: 2024-11-30
    miles: 0
  - start: 2024-12-01
    end: 2024-12-07
    miles: 0
  - start: 2024-12-08
    end: 2024-12-14
    miles: 0
  - start: 2024-12-15
    end: 2024-12-21
    miles: 0
  - start: 2024-12-22
    end: 2024-12-28
    miles: 0
  - start: 2024-12-29
    end: 2025-01-04
    miles: 0

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
