#!/usr/bin/env zx

const days = JSON.parse(argv._[1])

for (let day of days) {
  const [y, m, d] = day.split('-')

  const dayPath = path.join('./content/log', y, m, d)
  await $`mkdir -p ${dayPath}`

  const indexContent = `---
  title: "${day}"
  date: ${day}T23:59:59-00:00
  tags: []
  ---

  <!--more-->
  `

  await $`echo ${indexContent} > ${dayPath}/_index.md`
}
