---
title: 'GUI to Plot Driving Speed'
date: 2008-05-27T20:30:00.002+10:00
draft: false
url: /2008/05/gui-to-plot-driving-speed_6997.html
tags: 
- pycha
- articles
- python
- glade
---

I needed another Python fix, and I need one pretty badly. I spent the weekend wondering why it appears to be impossible to edit the GUIDs inside an Exchange mailbox store (read: NOT the GUIDs stored in AD for Exchange). Anyways, I digress.

My goals were simple. I wanted to use Python, wanted something to do with traffic, and wanted to play around with Glade/PyGTK and graphing stuff. My end result was a little app that allows you to specify a GPX file, and it plots the waypoints (and calculates the moving average!). Pretty simple, pretty useless, but pretty fun. I really do like pretty pictures.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgbsbQ8Cni_yPDyZ4MPoq2GXKP-XOFmq9aEpdc3acy9aMR5QemSj4UXMS1rGJ0IUSF3yc3unogl13DXYQM9z3wD_PmGreclmzDvmaqzJlSEuHJnq-sysd-r34mpNlI1gLOFwuWuyIWfRFp8/s400/SpeedPlotrX.jpg)](http://picasaweb.google.com/lh/photo/qv9V1YGpNjeYA0oywW8BGA?feat=embedwebsite)  
  

I ended up using matplotlab for the graphing part, but I don't really like how the graphs look. I will likely use Pycha (which dips into Cairo) for my future projects -- but we'll see when that point comes. (If data sensitivity wasn't an issue, I would totally use Google Charts, since I'm a sucker for APIs).