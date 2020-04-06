---
title: "Peloton Output Cheatsheet"
date: 2020-04-05T11:20:00-07:00
tags: ["peloton", "analysis-recipe"]
aliases: ["/recipe/peloton-cheatsheet"]
---

Quickly see the relationship between time, average wattage, and total kilojoules. Peloton computes joules using: 100 watts x 1 second = 100 joules ([reference](http://www.brygs.com/your-peloton-screen-resistance-cadence-and-output/)).

<!--more-->

## Avg Wattage and Duration to Total kj

If you average the wattage in a row for the duration in a column, you'll get the kilojoule total in the intersecting cell.

| watts/minutes | 10     | 20     | 30     | 45     | 60      |
|---------------|--------|--------|--------|--------|---------|
| 100           | 60.00  | 120.00 | 180.00 | 270.00 | 360.00  |
| 125           | 75.00  | 150.00 | 225.00 | 337.50 | 450.00  |
| 150           | 90.00  | 180.00 | 270.00 | 405.00 | 540.00  |
| 175           | 105.00 | 210.00 | 315.00 | 472.50 | 630.00  |
| 200           | 120.00 | 240.00 | 360.00 | 540.00 | 720.00  |
| 225           | 135.00 | 270.00 | 405.00 | 607.50 | 810.00  |
| 250           | 150.00 | 300.00 | 450.00 | 675.00 | 900.00  |
| 275           | 165.00 | 330.00 | 495.00 | 742.50 | 990.00  |
| 300           | 180.00 | 360.00 | 540.00 | 810.00 | 1080.00 |
| 325           | 195.00 | 390.00 | 585.00 | 877.50 | 1170.00 |
| 350           | 210.00 | 420.00 | 630.00 | 945.00 | 1260.00 |

## Total kj and Duration to Avg Wattage

To achieve a kilojoule total (rows) in a workout of a duration (columns), you need to average the wattage in the intersecting cell.

| kj/minutes | 10      | 20     | 30     | 45     | 60     |
|-----------------|---------|--------|--------|--------|--------|
| 100             | 166.67  | 83.33  | 55.56  | 37.04  | 27.78  |
| 200             | 333.33  | 166.67 | 111.11 | 74.07  | 55.56  |
| 300             | 500.00  | 250.00 | 166.67 | 111.11 | 83.33  |
| 400             | 666.67  | 333.33 | 222.22 | 148.15 | 111.11 |
| 500             | 833.33  | 416.67 | 277.78 | 185.19 | 138.89 |
| 600             | 1000.00 | 500.00 | 333.33 | 222.22 | 166.67 |
| 700             | 1166.67 | 583.33 | 388.89 | 259.26 | 194.44 |
| 800             | 1333.33 | 666.67 | 444.44 | 296.30 | 222.22 |
| 900             | 1500.00 | 750.00 | 500.00 | 333.33 | 250.00 |
| 1000            | 1666.67 | 833.33 | 555.56 | 370.37 | 277.78 |

## Seconds to Produce 1 kj by Wattage

| watts | seconds to 1 kj |
|-------|----------------|
| 50    | 20.00          |
| 75    | 13.33          |
| 100   | 10.00          |
| 125   | 8.00           |
| 150   | 6.67           |
| 175   | 5.71           |
| 200   | 5.00           |
| 225   | 4.44           |
| 250   | 4.00           |
| 275   | 3.64           |
| 300   | 3.33           |
| 325   | 3.08           |
| 350   | 2.86           |
| 375   | 2.67           |
| 400   | 2.50           |
| 425   | 2.35           |
| 450   | 2.22           |
| 475   | 2.11           |
| 500   | 2.00           |
