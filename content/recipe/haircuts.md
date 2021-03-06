---
date: 2012-11-23T19:09:59-08:00
title: Haircuts
tags: [personal-finance, data-exfil]
---

I bought a home trimmer on 2012-11-21. Of course, the next logical question is “how much money does this save me?”

To answer this question I turned to my mint.com data. I searched all transactions for “Supercuts” (it turns out I’ve been amazingly loyal over the past three years). That gave me a list of 29 haircuts with dates and prices.

![mint.com haircut transactions](https://i.imgur.com/tkg6W8r.png)

I saved the transactions as csv and loaded them into a spreadsheet.

![spreadsheet haircut transactions](https://i.imgur.com/6wICamr.png)

The next issue I saw was that my intervals between haircuts varied widely. So it wouldn’t be accurate to value each haircut at $20. A haircut after three months of growth would cut more hair and provide more value than a haircut after just a month. Nor would it be fair to start cutting my hair at home once a week and value each of those cuts at $20 each.

Ultimately I wanted a value for how much it costs to cut the hair I grow in a single day. Baldness jokes aside, I’m going to assume the hair I was able to grow in a single day in 2009 is the same as how much I can grow in a day now.

For each period, I can see how many days it has been since the previous cut. Then divide the cost of the cut by the days to get a $/day rate.

As for valuing home haircuts going forward I got an overall rate for the period 3/26/2009 through 10/26/2012 which came out to 43 cents. This means my hair grows at 43 cents per day.

Now my last paid haircut was on 10/16/2012. My first home cut was on November 22 - a span of 37 days. 37 days x $0.43 = $16.07. The value of my home haircut was $16.07.

Now factor in that the trimmer cost $35.33. I will have broken even in the next one or two home haircuts depending on the intervals. More specifically, I will have broken even in 45 days from 11/22/2012 which will be 1/6/2013.

![final spreadsheet view](https://i.imgur.com/4NUuURg.png)

EDIT: as of 7/1/2020, I'm still using the same trimmer. I've saved $1,187.66, net of the cost of the trimmer.
