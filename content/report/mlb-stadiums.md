---
title: "MLB Stadiums"
date: 2024-09-01T00:17:09-08:00
tags: ["meta", "baseball", "travel", "checklist"]
stadiums:
  - team: Arizona Diamondbacks
    venue: Chase Field
    visited: false
    date: 
    note: 

  - team: Atlanta Braves
    venue: Truist Park
    visited: false
    date: 
    note: 

  - team: Baltimore Orioles
    venue: Oriole Park at Camden Yards
    visited: true
    date: 2007
    note: 

  - team: Boston Red Sox
    venue: Fenway Park
    visited: true
    date: 2007
    note: also 4/24/2013

  - team: Chicago Cubs
    venue: Wrigley Field
    visited: true
    date: 2006
    note: 

  - team: Chicago White Sox
    venue: Guaranteed Rate Field
    visited: true
    date: 2006
    note: 

  - team: Cincinnati Reds
    venue: Great American Ball Park
    visited: true
    date: 2006
    note: 

  - team: Cleveland Guardians
    venue: Progressive Field
    visited: true
    date: 2006
    note: 

  - team: Colorado Rockies
    venue: Coors Field
    visited: false
    date: 
    note: 

  - team: Detroit Tigers
    venue: Tiger Stadium
    visited: true
    date: 2006
    note: Didn't see a game. stood outside the walls while it was still standing. I was able to see into the field and grandstands through a fence. 

  - team: Detroit Tigers
    venue: Comerica Park
    visited: true
    date: 2006
    note: 

  - team: Houston Astros
    venue: Minute Maid Park
    visited: false
    date: 
    note: 

  - team: Kansas City Royals
    venue: Kauffman Stadium
    visited: false
    date: 
    note: 

  - team: Los Angeles Angels
    venue: Angel Stadium
    visited: true
    date: 2002-09-02
    note: many visits

  - team: Los Angeles Dodgers
    venue: Dodger Stadium
    visited: true
    date: 2010-09-03
    note: many visits

  - team: Miami Marlins
    venue: LoanDepot Park
    visited: false
    date: 
    note: 

  - team: Milwaukee Brewers
    venue: American Family Field
    visited: false
    date: 
    note: 

  - team: Minnesota Twins
    venue: Metrodome
    visited: false
    date: 
    note: 
  - team: Minnesota Twins
    venue: Target Field
    visited: false
    date: 
    note: 

  - team: New York Mets
    venue: Shea Stadium
    visited: true
    date: 2007
    note: I was inside the stadium but the game was rained out after we arrived
  - team: New York Mets
    venue: Citi Field
    visited: false
    date: 
    note: 

  - team: New York Yankees
    venue: Yankee Stadium I
    visited: true
    date: 2007-06-29
    note: 
  - team: New York Yankees
    venue: Yankee Stadium II
    visited: false
    date: 
    note: 

  - team: Oakland Athletics
    venue: Oakland-Alameda County Coliseum
    visited: true
    date: 1984
    note: Many

  - team: Philadelphia Phillies
    venue: Citizens Bank Park
    visited: true
    date: 2007
    note: I've been to multiple games. 2007 was the first. 

  - team: Pittsburgh Pirates
    venue: PNC Park
    visited: true
    date: 2006
    note: 

  - team: San Diego Padres
    venue: Qualcomm Stadium
    visited: false
    date: 
    note: 

  - team: San Diego Padres
    venue: Petco Park
    visited: true
    date: 2004-04-08
    note: Several. First attended in 2004 for an open house preview. 

  - team: San Francisco Giants
    venue: Candlestick Park
    visited: true
    date: 1999-06-04
    note: several

  - team: San Francisco Giants
    venue: Oracle Park
    visited: true
    date: 2000-04-11
    note: 

  - team: Seattle Mariners
    venue: Kingdome
    visited: false
    date: 
    note: 

  - team: Seattle Mariners
    venue: T-Mobile Park
    visited: true
    date: 2009-05-02
    note: Saturday 6:10pm game vs. A's. 

  - team: St. Louis Cardinals
    venue: Busch Stadium I
    visited: false
    date: 
    note: 
  - team: St. Louis Cardinals
    venue: Busch Stadium II
    visited: true
    date: 2006
    note: 

  - team: Tampa Bay Rays
    venue: Tropicana Field
    visited: false
    date: 
    note: 

  - team: Texas Rangers
    venue: Globe Life Field
    visited: false
    date: 
    note: 

  - team: Toronto Blue Jays
    venue: Rogers Centre
    visited: false
    date: 
  - team: Washington Nationals
    venue: RFK Stadium
    visited: true
    date: 2007
    note: 
  - team: Washington Nationals
    venue: Nationals Park
    visited: false
    date: 
    note: 

---
{{< summary.inline >}}
<p>Stadiums Visited: {{ len (where .Page.Params.stadiums "visited" true) }}</p>
{{< /summary.inline >}}

<!--more-->

{{< detail.inline >}}

<table>
  <tr>
    <th></th>
    <th>Team</th>
    <th>Venue</th>
    <th>Date</th>
    <th>Note</th>
  </tr>
  {{ range $i, $stadium := .Page.Params.stadiums }}
    <tr>
      <td>{{ cond $stadium.visited "✅" "❌" }}</td>
      <td>{{ $stadium.team }}</td>
      <td>{{ $stadium.venue }}</td>
      <td>{{ $stadium.date }}</td>
      <td>{{ $stadium.note | default "-" }}</td>
    </tr>
  {{ end }}


</table>
{{< /detail.inline >}}
