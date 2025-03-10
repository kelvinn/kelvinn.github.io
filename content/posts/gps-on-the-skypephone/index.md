---
title: 'GPS on the SkypePhone'
date: 2008-02-03T21:30:00.002+11:00
draft: false
url: /2008/02/gps-on-skypephone_9589.html
tags: 
- phone
- gps
- articles
---

Yesterday I was sort of curious if I could use my 3 Skypephone in a pinch if I got lost, which here in Sydney, happens quite often. Luckily 3's Skypephone has both Bluetooth, and supports j2me apps. Mobile GPS unit, here I come.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjExWMS7zKJdGCG_1MHdpb900yTseLCrbHerf2PlfzwSouqfnmJHr5V1jiIcDcbMrEul2OZUFlCYOQhTgrq_3C-cYDWmxkx-yDOr6NNwokX8P-gUikt3DSjxRi11qJrMuP4_aSRLpjhLPax/s288/DSC03368.jpg)](http://picasaweb.google.com/lh/photo/3AY6h-qKwGk9NpnB9hrwsw?feat=embedwebsite)  
  

The recipe to get maps on your Skypephone is pretty darn easy. You'll need one dash bluetooth GPS receiver (I have the [Qstarz BT-Q1000](http://www.qstarz.com/Products/GPS%20Products/BT-Q1000.html)), [TrekBuddy](http://linuxtechs.net/kruch/tb/forum/index.php), a TrekBuddy acceptable map ([easily downloadable](http://osm.bandnet.org/browse/?1,1,1,0)), and one dab computer -- but since you're reading this, I figure you've got that part taken care of.

My process is as follows (on Linux): plug in your Skypephone and select "usb storage" on your phone. Drag the TrekBuddy.jar file onto your new mounted drive (mine comes up as KINGSTON). Drag a relevent map downloaded from bandnet.org onto your phone as well. Unplug your phone from the USB, and it will scan for new media. Hit Menu -> My Stuff -> Others and scroll down to treckbuddy.jar -- hit Run. Go to your Connectivity settings and turn on bluetooth. Next go to Games and Apps and downloaded apps, start TrekBuddy. Press the key above MENU and select Load Map, and choose the map you uploaded to your phone. Now hit Start. Select the GPS device, and you're in business!

There are more instructions [here](http://linuxtechs.net/kruch/tb/forum/viewtopic.php?t=91) and also [here](http://linuxtechs.net/kruch/tb/forum/viewtopic.php?t=22).