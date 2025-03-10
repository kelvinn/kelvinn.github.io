---
title: 'Slope Finder for the Missus'
date: 2008-11-02T21:30:00.008+11:00
draft: false
url: /2008/11/slope-finder-for-missus_5304.html
tags: 
- articles
- python
- glade
- sysadmin
---

Since I do sysadminy stuff all day, I don't really get a chance to do much coding (or not as much of a chance as I would like). You can imagine my joy when my girlfriend expressed a problem she needed solved: "I'm going to need to solve 100s of slope equations, i.e. where two lines intersect. Can you write a program to do it?" Sure!

I asked if she wanted to do a batch input or just a one-off type of deal, she decided on the latter. Although I've done a fair bit of PyGTK stuff, I had never actually needed to convert it to Windows. I debated using IronPython -- but needed to use a special library to help solve the equations (I'm lazy).

So, where is the power in Python? After about 15-20m I had a console based app that could solve the slopes. I added the Linux GUI part in maybe 45m, and then the Windows part in, well, not 45m!

Either way, screenshot is below. Thanks girlfriend, I had fun!

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgEAxIIJW4HIfuL3VFBYCY8aQM8pVChFP5qcxi3_Daaay5oN2OEJ4XstDByk-fOFICyJUfkp3Beerf12V4n3HmWFn_4WNd36bvDOFd0y5Grx6cgo5WpICpgFU5exuS0zwHrCNTaSHeuzMOt/s800/slopefinder.jpg)](http://picasaweb.google.com/lh/photo/z7c7K2SAI4DQi84sBKkiGA?feat=embedwebsite)