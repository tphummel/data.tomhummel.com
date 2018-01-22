---
title: "Github Stars"
date: 2018-01-05T19:09:59-08:00
tags: ["data-exfil", "analysis-recipe"]
---

Gather data on which Github repos you starred.

<!--more-->

#### Download Data for user: tphummel

```
for i in {1..20}
do
  curl -H "Accept: application/vnd.github.v3.star+json" "https://api.github.com/users/tphummel/starred?page=$i" > "p$i.json"
done

```

#### gather raw stars by year (optional)

```
cat *.json | jq --slurp '. | flatten | .[] | select((.starred_at >= "2016-01-01") and (.starred_at <= "2016-12-31"))' | jq --slurp '.' > 2016-github-stars.json
```

#### question

> what languages did I star most frequently in 2016?

```
cat *.json \
  | jq --slurp '. | flatten | .[] | select((.starred_at >= "2016-01-01") and (.starred_at <= "2016-12-31"))' \
  | jq --slurp '.[] .repo.language' \
  | awk '{ FS="\n" count[$1]++}END{for(j in count) print j","count[j]}' \
  | sort -t "," -k2 -nr  
```

#### answer

```
"JavaScript",63
"Python",34
"Go",34
"Shell",20
"Ruby",13
null,12
"C",7
"Java",5
"HCL",4
"PHP",3
"Objective-C",3
"HTML",3
"Perl",2
"CSS",2
"TeX",1
"Roff",1
"Jupyter Notebook",1
"Hack",1
"C++",1
```


#### Links

(source gist)[https://gist.github.com/tphummel/efdfc6737187e9927f72dac7465cadab]
