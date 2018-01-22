---
title: "Face Time-lapse"
date: 2018-01-06T13:11:23-08:00
tags: ["analysis-recipe"]
---

Make a time-lapse video out of daily pictures of your face.

<!--more-->

#### ifttt recipe
ifttt camera widget -> google drive

#### solution
1. get all the images from google drive onto your laptop, stored in a directory named `2017/`
1. use `ffmpeg` to stitch the images together into a video:

```
ffmpeg \
  -framerate 12 \
  -pattern_type glob \
  -i '2017/*.jpg' \
  -c:v libx264 \
  -vf "transpose=1" \
  -pix_fmt yuv420p \
  2017.mp4
```

#### notes
- a framerate of 10, 12, or 15 frames/second seems like a good setting with 365 images.
