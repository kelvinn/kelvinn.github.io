---
title: 'Convert VMWare Movie to FLV'
date: 2006-09-30T20:30:00.002+10:00
draft: false
url: /2006/09/convert-vmware-movie-to-flv_2236.html
tags: 
- howtos
---

This little process, a total of two lines, took way to long to figure out.

First, we convert the VMware avi (VMnc format) to the Microsoft avi format.

  
  
```bash
 mencoder -of avi -ovc lavc movie.avi -o movie2.avi 
```  
  

Next, we convert the Microsoft avi format to FLV format.

  
  
```bash
 ffmpeg -i movie2.avi -r 12  -b 100 movie.flv 
```  
  

You can play around with the -r switch (rate per second) and the -b switch (bitrate). But, if those get larger, so does your FLV file.