#!/usr/bin/env zx

const day = argv._[1]
console.log(day)
const [y, m, d] = day.split('-')
const dayPath = `./content/log/${y}/${m}/${d}`
$`mkdir -p ${dayPath}`

const indexContent = `---
title: "${day}"
date: ${day}T23:59:59-00:00
tags: []
---

<!--more-->
`

$`echo ${indexContent} > ${dayPath}/_index.md`
