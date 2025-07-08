#!/usr/bin/env zx

const day = argv._[1]
if (!day) {
  console.error('Usage: mkdirp-journal-day.mjs YYYY-MM-DD')
  process.exit(1)
}

const [y, m, d] = day.split('-')
const dayPath = `./content/j/${y}/${m}/${d}`
await $`mkdir -p ${dayPath}`

const indexContent = `---
title: "${day}"
date: ${day}T00:00:00Z
tags: []
---

<!--more-->
`
await $`echo ${indexContent} > ${dayPath}/index.md`

// create placeholder JSON data files
await $`echo '{}' > ${dayPath}/run.json`
await $`echo '{}' > ${dayPath}/nomie.json`
await $`echo '{}' > ${dayPath}/swarm.json`
