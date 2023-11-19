---
title: "2023 Running"
date: 2023-01-04T16:30:00-08:00
tags: ["running", "running-annual"]
total_miles_run: 472.92
total_runs: 88
total_minutes: 4231
total_ascent_feet: 42189
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
  - start: 2023-02-19
    end: 2023-02-25
    miles: 9.01
  - start: 2023-02-26
    end: 2023-03-04
    miles: 9.36
  - start: 2023-03-05
    end: 2023-03-12
    miles: 9.96
  - start: 2023-03-12
    end: 2023-03-18
    miles: 9.08
  - start: 2023-03-19
    end: 2023-03-25
    miles: 9.31
  - start: 2023-03-26
    end: 2023-04-01
    miles: 9.43
  - start: 2023-04-02
    end: 2023-04-08
    miles: 9.34
  - start: 2023-04-09
    end: 2023-04-15
    miles: 10.25
  - start: 2023-04-16
    end: 2023-04-22
    miles: 14.02
  - start: 2023-04-23
    end: 2023-04-29
    miles: 3.30
  - start: 2023-04-30
    end: 2023-05-06
    miles: 9.16
  - start: 2023-05-07
    end: 2023-05-13
    miles: 9.37
  - start: 2023-05-14
    end: 2023-05-20
    miles: 10.34
  - start: 2023-05-21
    end: 2023-05-27
    miles: 6.01
  - start: 2023-05-28
    end: 2023-06-03
    miles: 9.92
  - start: 2023-06-04
    end: 2023-06-10
    miles: 12.81
  - start: 2023-06-11
    end: 2023-06-17
    miles: 10.48
  - start: 2023-06-18
    end: 2023-06-24
    miles: 14.14
  - start: 2023-06-25
    end: 2023-07-01
    miles: 8.85
  - start: 2023-07-02
    end: 2023-07-08
    miles: 9.07
  - start: 2023-07-09
    end: 2023-07-15
    miles: 17.45
  - start: 2023-07-16
    end: 2023-07-22
    miles: 9.79
  - start: 2023-07-23
    end: 2023-07-29
    miles: 15.21
  - start: 2023-07-30
    end: 2023-08-05
    miles: 9.29
  - start: 2023-08-06
    end: 2023-08-12
    miles: 9.14
  - start: 2023-08-13
    end: 2023-08-19
    miles: 9.16
  - start: 2023-08-20
    end: 2023-08-26
    miles: 10.08
  - start: 2023-08-27
    end: 2023-09-02
    miles: 9.84
  - start: 2023-09-03
    end: 2023-09-09
    miles: 10.50
  - start: 2023-09-10
    end: 2023-09-16
    miles: 16.06
  - start: 2023-09-17
    end: 2023-09-23
    miles: 10.81
  - start: 2023-09-24
    end: 2023-09-30
    miles: 9.05
  - start: 2023-10-01
    end: 2023-10-07
    miles: 17.77
  - start: 2023-10-08
    end: 2023-10-14
    miles: 9.15
  - start: 2023-10-15
    end: 2023-10-21
    miles: 12.91
  - start: 2023-10-22
    end: 2023-10-28
    miles: 9.32
  - start: 2023-10-29
    end: 2023-11-04
    miles: 6.71
  - start: 2023-11-05
    end: 2023-11-11
    miles: 14.72
  - start: 2023-11-12
    end: 2023-11-18
    miles: 3.01
    note: recovery from double inguinal hernia repair surgery
  - start: 2023-11-19
    end: 2023-11-25
    miles: 
  - start: 2023-11-26
    end: 2023-12-02
    miles: 
  - start: 2023-12-03
    end: 2023-12-09
    miles: 
  - start: 2023-12-10
    end: 2023-12-16
    miles: 
  - start: 2023-12-17
    end: 2023-12-23
    miles: 
  - start: 2023-12-24
    end: 2023-12-30
    miles: 


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

