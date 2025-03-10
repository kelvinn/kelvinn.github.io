---
title: 'Operation Field'
date: 2009-04-13T20:30:00.005+10:00
draft: false
url: /2009/04/operation-field_8222.html
tags: 
- electronics
- OSM
- projects
- arduino
- java
---

Status:  

It is time for a new project. I've finally decided I want to do some electronics stuff - at least play around in that realm a little. However, I want to "get out and about" a little as well, so this leads me to my idea: a controllable long-range RC plane.

I've been debating whether to go the embedded Linux route, or the more simple microcontroller route. One of the first things I stumbled upon was [ArduPilot](http://diydrones.com/profiles/blog/show?id=705844%3ABlogPost%3A44814), a cheap Arduino-based board allowing for a UAV. However, after looking through the requirements I would have needed to purchase an RF transmitter, and they aren't cheap. This made me rethink the ArduPilot route and to evaluate what I really wanted to do: control the plan. My ultimate goal is to attach a joystick to my computer and be able to control the RC plane. This presents another problem with the ArduPilot, however, as there isn't an extra Rx pin available on the ArduPilot board (or so the forums say), I wouldn't be able to transmit coordinates on the fly.

After much research, I think I've determined what I'm going to do. I'm ultimately going to adopt the best parts of the ArduPilot, and fill in the gaps with my own board. I'm going to take an EasyStar, combine it with an Arduino Mini, Xbee, XY Sensor, GPS module, servos, H-bridges and a custom PCB, and hope it works.

One thing I've learned from YS is to stage our the things I buy. For instance, instead of signing up for a year at a local gym, try a month first. This project won't be any different, and while most of the equipment is very reasonably priced, I still want to make sure I enjoy this type of thing. The first stage is going to be to buy the Arduino Mini, breadboard, servos and h-bridge (and a cheap DC motor), and see if I can get it all working. If I can, I'll buy the EasyStar and see if I can control it with a joystick. If still successful, I'll acquire the Xbees and GPS module - and these represent the majority of the cost.

Another element I've considered is how to visualize the RC plane flying around. I had contemplated looking into using Google Earth, but I'd really prefer to use a free variant. I also want to strengthen my Java knowledge, so have opted to use the SDK for WorldWind. I was very excited to see that they also have support for OSM, which is just spectaculous. I plan to have a HUD that on the right displays the plane's location in WorldWind, and on the left display current altitude, tilt and RF strength. Since I've been flying through a book on Processing, this looks like a perfect real-life opportunity to use it.

I'm likely to start putting my money where my mouth is in the next two weeks.