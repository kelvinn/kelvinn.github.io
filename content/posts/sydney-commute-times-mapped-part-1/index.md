---
title: 'Sydney Commute Times Mapped Part 1'
date: 2013-07-21T10:06:00.002+10:00
draft: false
url: /2013/07/sydney-commute-times-mapped-part-1.html
tags: 
- postgis
- gis
- articles
- transport
- gtfs
---

I quite like open data. I like data based on open standards (or mostly open standards) even better. Many transport operators around the world have started releasing their timetable data using (mostly) open standards, e.g. [GTFS](http://en.wikipedia.org/wiki/General_Transit_Feed_Specification). One of the nice things about using a standard is that clever people have created tools to work with the timetable data, and those tools can now be used to manipulate timetable data from hundreds of agencies. The magnificent OpenTripPlanner is one such tool, and it works well with [131500](http://131500.info/)'s GTFS data.

  

New South Wales Planning & Infrastructure have released a draft [plan](http://strategies.planning.nsw.gov.au/MetropolitanStrategyforSydney.aspx) for how they hope to shape Sydney's growth, which is where they detail the idea of a "city of cities". I thought it would be interesting to mash these smaller "cities" with 131500's transport data, and then display a map with the shortest commute to the nearest city. Various cities, I believe including Melbourne, have goals of re-achieving a "20-minute" city, or something similar (i.e. X% of the population can reach X% of the city within X minutes).

  

This map is the first stage. It only displays the commute time to St Leonards from every Mesh Block in the greater Sydney area. I used the open source tool OpenTripPlanner to computer the commute times, with OpenStreetMaps to support walking distances. The next map I release will probably have all the regional cities, and a similar styled map depicting time to nearest "centre".

  

  
  
[View Full Screen](http://maps.kelvinism.com/st_leonards_commute.html)