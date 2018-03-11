---
title: "Tasks Wordcloud"
date: 2017-12-31T09:54:42-08:00
tags: ["analysis-recipe"]
---

Create a word cloud using the text of the tasks you completed last year.

<!--more-->

#### prerequisites
1. capture completed tasks every day. ex: [iDoneThis](https://idonethis.com)
1. export your csv of idonethis data from the year
1. have a working python/pip install


#### steps
```
cd ~/Code
virtualenv word-cloud
cd word-cloud
source bin/activate
pip install wordcloud
mv ~/Downloads/export.csv 2017-idonethis.csv
pip install csvkit

bin/wordcloud_cli.py --help

cat 2017-idonethis.csv| csvcut -c body | bin/wordcloud_cli.py --width 600 --height 600 --margin 10 > 2017.png
```

#### Links

- [Virtualenv docs](https://virtualenv.pypa.io/en/stable/userguide/#usage)
- [wordcloud cli](https://github.com/amueller/word_cloud)
- [csvkit docs](https://csvkit.readthedocs.io/en/1.0.2/)
