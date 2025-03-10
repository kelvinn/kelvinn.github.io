---
title: 'Operation Cold House'
date: 2009-06-14T20:30:00.009+10:00
draft: false
url: /2009/06/operation-cold-house_7266.html
tags: 
- home
- mysql
- google charts
- temperature
- pachube
- projects
- arduino
---

Status:  
  
  
  

My house is cold. I want to start playing with simple electronics before starting [Operation Field](http://www.kelvinism.com/projects/operation-field/), so have created Operation Cold House.

This is just simply sticking a temperature sensor onto an Arduino, linking that up to my little home "[server](http://www.kelvinism.com/tech-blog/true-consolidation/)", and uploading that to my website. I'll display some nifty graphs, too, and link it to [Pachube](http://www.pachube.com/). Stay tuned.

**Update**: Complete! The proof is [in the](http://www.kelvinism.com/howtos/simple-arduino-led-tutorial/) [pudding](http://www.kelvinism.com/tech-blog/arduino-101/). I now have a personal website from home (sorry, not public) that displays the daily and weekly temperature at home. The process is basically like this: my little Arduino gathers the temperature, and is polled every minute with a python script via cron. This script then sticks the time and temperature into MySQL. It also exports the temperature to Pachube. Every 30m I have a script that queries MySQL and uses Google's Chart's API to graph the temperature. Looks great, I'll post a graph soon.