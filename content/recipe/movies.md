---
title: "Movies"
date: 2018-07-31T19:11:24-08:00
tags: ["movies", "analysis-recipe"]
---

Track the movies I watch and associated metadata.

<!--more-->

### plan

IFTTT recipe: IMDB page, Pocket w/ tag `video-checkin` -> google sheet

Other pocket tags:

- venue: `hbo`, `netflix`, `amazon`, `theater`, `cable`, `airplane`, `hotel`...
- cost: `free`, `$` (rent), `$$` (buy)
- first-watch vs. re-watch

### enrichment in google sheets

- the year of the movie is in the title of each html doc.
- where `D2` is the html title, extract the date: `=value(REGEXEXTRACT(D2,"[0-9]{4}"))`
- where `H2` is the year, extract the decade: `=concatenate(floor(H2/10),"0")`
- where `C2` is the list of pocket tags, extract spend: `=if(K2<datevalue("2016-08-28"),"unknown",if(iferror(find("$$",C2),-1)>=0,"buy", if(iferror(find("$",C2), -1)>=0,"rent", "free")))`
- where `C2` is the list of pocket tags, extract venue: `=if(iferror(search("amazon",C2),-1)>=0,"amazon", if(iferror(search("netflix",C2),-1)>=0,"netflix", if(iferror(search("hbo",C2),-1)>=0,"hbo", if(iferror(search("itunes",C2),-1)>=0,"itunes", if(iferror(search("theatre",C2),-1)>=0,"theatre", if(iferror(search("dvd",C2),-1)>=0,"dvd", if(iferror(search("airplane",C2),-1)>=0,"airplane",if(iferror(search("hotel",C2),-1)>=0,"hotel","other"))))))))`

### queries
- how many movies did i watch this year?
- which venues do I use most?
- Do I pay for movies?
- Of the movies I watched last year, which decades did I frequent the most?
