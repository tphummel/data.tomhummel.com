---
title: "MLB Stadiums"
date: 2024-09-01T00:17:09-08:00
tags: ["meta", "baseball", "travel", "checklist"]
stadiums:
  - team: Arizona Diamondbacks
    venue: Chase Field
    city: phoenix-az
    visited: false
    date: 
    note: 

  - team: Atlanta Braves
    venue: Truist Park
    city: atlanta-ga
    visited: false
    date: 
    note: 

  - team: Baltimore Orioles
    venue: Oriole Park at Camden Yards
    city: baltimore-md
    visited: true
    date: 2007
    note: 

  - team: Boston Red Sox
    venue: Fenway Park
    city: boston-ma
    visited: true
    date: 2007
    note: also 4/24/2013

  - team: Chicago Cubs
    venue: Wrigley Field
    city: chicago-il
    visited: true
    date: 2006
    note: 

  - team: Chicago White Sox
    venue: Guaranteed Rate Field
    city: chicago-il
    visited: true
    date: 2006
    note: 

  - team: Cincinnati Reds
    venue: Great American Ball Park
    city: cincinnati-oh
    visited: true
    date: 2006
    note: 

  - team: Cleveland Guardians
    venue: Progressive Field
    city: cleveland-oh
    visited: true
    date: 2006
    note: 

  - team: Colorado Rockies
    venue: Coors Field
    city: denver-co
    visited: false
    date: 
    note: 

  - team: Detroit Tigers
    venue: Tiger Stadium
    city: detroit-mi
    visited: true
    date: 2006
    note: Didn't see a game. stood outside the walls while it was still standing. I was able to see into the field and grandstands through a fence. 

  - team: Detroit Tigers
    venue: Comerica Park
    city: detroit-mi
    visited: true
    date: 2006
    note: 

  - team: Houston Astros
    venue: Minute Maid Park
    city: houston-tx
    visited: false
    date: 
    note: 

  - team: Kansas City Royals
    venue: Kauffman Stadium
    city: kansascity-mo
    visited: false
    date: 
    note: 

  - team: Los Angeles Angels
    venue: Angel Stadium
    city: anaheim-ca
    visited: true
    date: 2002-09-02
    note: many visits

  - team: Los Angeles Dodgers
    venue: Dodger Stadium
    city: losangeles-ca
    visited: true
    date: 2010-09-03
    note: many visits

  - team: Miami Marlins
    venue: LoanDepot Park
    city: miami-fl
    visited: false
    date: 
    note: 

  - team: Milwaukee Brewers
    venue: American Family Field
    city: milwaukee-wi
    visited: false
    date: 
    note: 

  - team: Minnesota Twins
    venue: Metrodome
    city: minneapolis-mn
    visited: false
    date: 
    note: 
  - team: Minnesota Twins
    venue: Target Field
    city: minneapolis-mn
    visited: false
    date: 
    note: 

  - team: New York Mets
    venue: Shea Stadium
    city: newyork-ny
    visited: true
    date: 2007
    note: I was inside the stadium but the game was rained out after we arrived
  - team: New York Mets
    venue: Citi Field
    city: newyork-ny
    visited: false
    date: 
    note: 

  - team: New York Yankees
    venue: Yankee Stadium I
    city: newyork-ny
    visited: true
    date: 2007-06-29
    note: 
  - team: New York Yankees
    venue: Yankee Stadium II
    city: newyork-ny
    visited: false
    date: 
    note: 

  - team: Oakland Athletics
    venue: Oakland-Alameda County Coliseum
    city: oakland-ca
    visited: true
    date: 1984
    note: Many
  
  - team: Oakland Athletics
    venue: Sutter Health Park
    city: sacramento-ca
    visited: true
    date: 2025-05-24
    note: also 7/4 and 7/5 2025

  - team: Athletics
    venue: Las Vegas Ballpark
    city: lasvegas-nv
    visited: true
    date: 2026-06-13
    note: Section 107, Row V, Seat 5 vs. Col

  - team: Philadelphia Phillies
    venue: Citizens Bank Park
    city: philadelphia-pa
    visited: true
    date: 2007
    note: I've been to multiple games. 2007 was the first. 

  - team: Pittsburgh Pirates
    venue: PNC Park
    city: pittsburgh-pa
    visited: true
    date: 2006
    note: 

  - team: San Diego Padres
    venue: Qualcomm Stadium
    city: sandiego-ca
    visited: false
    date: 
    note: 

  - team: San Diego Padres
    venue: Petco Park
    city: sandiego-ca
    visited: true
    date: 2004-04-08
    note: Several. First attended in 2004 for an open house preview. 

  - team: San Francisco Giants
    venue: Candlestick Park
    city: sanfrancisco-ca
    visited: true
    date: 1999-06-04
    note: several

  - team: San Francisco Giants
    venue: Oracle Park
    city: sanfrancisco-ca
    visited: true
    date: 2000-04-11
    note: 

  - team: Seattle Mariners
    venue: Kingdome
    city: seattle-wa
    visited: false
    date: 
    note: 

  - team: Seattle Mariners
    venue: T-Mobile Park
    city: seattle-wa
    visited: true
    date: 2009-05-02
    note: Saturday 6:10pm game vs. A's. 

  - team: St. Louis Cardinals
    venue: Busch Stadium I
    city: stlouis-mo
    visited: false
    date: 
    note: 
  - team: St. Louis Cardinals
    venue: Busch Stadium II
    city: stlouis-mo
    visited: true
    date: 2006
    note: 

  - team: Tampa Bay Rays
    venue: Tropicana Field
    city: tampabay-fl
    visited: false
    date: 
    note: 

  - team: Texas Rangers
    venue: Globe Life Field
    city: arlington-tx
    visited: false
    date: 
    note: 

  - team: Toronto Blue Jays
    venue: Rogers Centre
    city: toronto-on
    visited: true
    date: 2026-05-08
    note: 

  - team: Washington Nationals
    venue: RFK Stadium
    city: washington-dc
    visited: true
    date: 2007
    note: 
  - team: Washington Nationals
    venue: Nationals Park
    city: washington-dc
    visited: false
    date: 
    note: 

---
{{< mlb-stadiums-map >}}

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
