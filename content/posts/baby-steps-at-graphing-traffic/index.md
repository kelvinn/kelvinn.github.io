---
title: 'Baby Steps at Graphing Traffic'
date: 2008-04-27T20:30:00.006+10:00
draft: false
url: /2008/04/baby-steps-at-graphing-traffic_522.html
tags: 
- openstreetmap
- gis
- articles
- google
- projects
---

Status:  
You can likely tell that I've been having some fun with graphing and mapping recently. I was reading a few articles about GIS and stumbled upon a pretty darn cool project at [Webopticon](http://www.webopticon.com/projects/neighborhood_nets), which included cool pictures. I showed it to my girlfriend thinking she would find it interesting, and then realized: oh! KML has an altitude attribute. That could be interesting.  
One of my projects is to create [maps of Sydney's traffic](http://www.kelvinism.com/2007/12/sydneys-driving-habits.html)[](http://www.blogger.com/), so I have been experimenting heavily with Mapnik and OSM. I figured I could have some fun and finally parse some gps tracks and display the data.  
[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi8Ju2Qv3TAIupmzBjORZ5wUBGjxIlwZ_0mrPb0Mku5Yob6_ldYEmtRO0GP_kQ62-aZDZ3fP8_vh6nfXv9NpP5X98oneS25YXXf9Tr-pD1RMkp7l_jbDBWBsqxrA5hIDhH8KvfVjZI0TvGc/s288/gpstracks3.jpg)](http://picasaweb.google.com/lh/photo/bkhs8KqkZyS7yIoA6AeNnA?feat=embedwebsite)  
  
I first started off trying to play around with the KML files my gps logger natively stores. After a while I realized it shouldn't be this hard to parse the XML, and realized it also stores data in gpx format. I opened up one of the gpx files and immediately saw how much easier it would be to work with. I quickly created a parser for the xml in Python (using the dom method, yet I think I'm going to rewrite it using sax), and then with the aid of [an article](http://zcologia.com/news/584/better-python-practices-for-the-geoweb/) by Sean Gillies, converted the needed objects into KML. I used the speed attribute (with some magnification) as the altitude, and voila, a pretty picture.  
This picture is as Victoria Road crosses James Rouse Drive -- a spot that is always congested in the morning.  
I'll likely post some code shortly, I would like to rewrite the parsing section to use something event-driven -- hopefully it will be a little faster.