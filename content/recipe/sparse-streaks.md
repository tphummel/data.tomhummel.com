---
title: "Sparse Streaks"
date: 2018-01-28T21:11:50-08:00
tags: ["analysis-recipe"]
---

Find Streaks in Daily Data with Sparse/Missing Days

<!--more-->

### Install Libraries

```
brew update
brew install tphummel/util/date-range
brew install tphummel/util/streak
brew install jq
brew install csvkit
```

### Create Input Dataset

```
cat << EOF > sparse.csv
"category 4",2018-01-01,3
"category 4",2018-01-02,1
"category 4",2018-01-04,0
"category 4",2018-01-05,1
"category 4",2018-01-08,1
"category 4",2018-01-10,5
"category 4",2018-01-11,6
"category 4",2018-01-12,5
"category 4",2018-01-13,7
"category 4",2018-01-15,1
"category 4",2018-01-19,1
"category 4",2018-01-21,5
"category 4",2018-01-22,6
"category 4",2018-01-23,5
"category 4",2018-01-24,5
"category 4",2018-01-25,7
"category 4",2018-01-27,5
"category 4",2018-01-28,9
"category 4",2018-01-30,1
"category 4",2018-01-31,2
EOF
```

### Compile List of Streaks

```
date-range 2018-01-01 2018-02-15 | \
  jq -r '.[]' | \
  csvjoin -H -c "2,1" --outer ./sparse.csv - 2>/dev/null | \
  csvcut -c 4,1,3 | \
  csvsort -c 1 | \
  csvjson | \
  jq ".[] | [.a2, .a, .c]" | \
  jq --slurp "." | \
  streak --label 0 --column 2 --min 5 | \
  jq -r ".[] | [.start, .end, .value] | @csv" | \
  csvsort -H -c 3 -r 2>/dev/null | \
  sed '1 s/.*/start,end,streak/' | \
  csvlook
```

### Result
```
|      start |        end | streak |
| ---------- | ---------- | ------ |
| 2018-01-21 | 2018-01-25 |      5 |
| 2018-01-10 | 2018-01-13 |      4 |
| 2018-01-27 | 2018-01-28 |      2 |
```

## Appendix

- [Streak CLI Tool](https://github.com/tphummel/streak)
- [Date Range CLI Tool](https://github.com/tphummel/date-range)
