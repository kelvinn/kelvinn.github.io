---
title: 'Another Baby Step'
date: 2008-04-29T20:30:00.006+10:00
draft: false
url: /2008/04/another-baby-step_1340.html
tags: 
- openstreetmap
- graphing
- articles
- python
---

I showed a few of my co-workers my graph and one replied -- oh! that's really cool. (I think only two of my co-workers are actually interested in my geekyness). He then emailed me tonight a .kmz file containing a colorized file of his speed. I looked at the kml and noticed it appeared to be dynamically allocated judging by the top speed. Well, as you could guess, I surely had to modify my code to include colors.

Within an hour I had a semi-working example, and within two hours will easily be done with this blog post. The code might not be perfect, but it first parses the xml and returns the max speed for the trip. Next, it colorizes the speeds based on a scale of 0-255, with 0 being blue for fast and 255 for being yellow, or slow. I was going to study for the CCNA tonight, but it looks like writing Python is just too much fun.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhHE0LrPY3qk6xEJfwkyjpNu6wcJtGv9vtho2gi7W9NCTbViKUXsImuIoNjcoZGTiSTTrGkRCOzb_WP8RE7wTweah7WkOwdp1x6b2b7teDvMvGcf2u-Ou9jYkfyKTDXpWY8N8J_GYEDYKkI/s288/gpstracks1.jpg)](http://picasaweb.google.com/lh/photo/vQ_v3bb0f6QLHiOEEShN1Q?feat=embedwebsite)  
  
[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhySCFquf2IZDhKtK0aJNzlga4jA04ye11unofmz42J5_UB1AdyLDrsuxfZCwVUuj-9HBPcs04l3vkke-S3aMfbdI_2i6iwM4pmL4WFrCpD6YmSUJ9T8I6ixMDzhnuX7-I62nPs8VsP8gXx/s288/gpstracks2.jpg)](http://picasaweb.google.com/lh/photo/L7745TDqLkWkkftff8bV8g?feat=embedwebsite)  
  

So what, you might ask, are those dips? Good question. They are huge speed bumps (and the tall blue mound in the middle is a really steep hill).