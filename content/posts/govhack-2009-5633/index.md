---
title: "GovHack 2009"
date: 2009-11-02T10:30:00.003Z
url: /2009/11/govhack-2009_5633.html
tags:
- travel
- gis
- python
- government
- govhack
- web
- osm
- lobbyclue
- australia
blogger_id: "tag:blogger.com,1999:blog-1700991654357243752.post-8998426793950386873"
blogger_post_id: "8998426793950386873"
blogger_status: "LIVE"
blogger_updated: 2013-01-08T13:31:03.810Z
---
Nearly everyone on our team stayed up the entire night; most of us didn't sleep at all.

It had been years since I last pulled an all-nighter, but they had always been for good causes. I had just completed another one and had an immense amount of fun in the process. The reason? [GovHack](http://govhack.org).

GovHack aimed to encourage the Australian government to make as much information openly available as possible. The challenge was to take the scattered pieces of information already available and turn them into useful tools or visualisations for the public.

I arrived at about 1:45 for the 2:00 registration and was a little worried about what I had gotten myself into: there were signs everywhere, but only two people in the room. Over the next 30 minutes, however, people quickly filed in, and soon the room was full. Many teams came from different organisations, but I arrived on my own. I soon began talking with [Christian](http://Twitter.com/frglps), a web developer from Melbourne, and [Doris](http://Twitter.com/DorisSpiel), a network visualiser also from Melbourne. We discussed ideas and began settling on government lobbying. After the kickoff ceremony, I walked to the car to pay for 20 more minutes of parking; we all know parking rangers will catch you in those final 20 minutes. When I came back, a few more people who had arrived alone had joined us: [Michael](http://Twitter.com/mjec) and [Alex](http://Twitter.com/maxious). Another colleague, Tim, stayed for a while but unfortunately had to work the next day.

![4059658704 66a4d8b1f5](http://farm3.static.flickr.com/2556/4059658704_66a4d8b1f5.jpg)

In retrospect, one observation stood out: over the entire 24 hours, not one member of the team said anything negative about lobbying or lobbyists. We simply wanted to visualise the relationships among the different organisations.

Christian and I mapped out the features we thought would be useful and the range we could realistically deliver. Because we didn't yet know whether the visualisation would work, we also created a straightforward category view and a geospatial view. We divided the goals and established rough areas of responsibility, although there was a fair amount of overlap, and started building.

Alex took responsibility for helping assimilate the data and creating the impressive visualisation, using a library he had never seen or worked with before. Michael assimilated the rest of the data and somehow kept adding tables with more and more information. Christian created the category view and essentially glued everything together.

![4058876335 76e72d67c3](http://farm3.static.flickr.com/2488/4058876335_76e72d67c3.jpg)

My primary role was to create the geospatial visualisation. One element I particularly wanted to display was Australia's electoral boundaries on a "slippy map." This proved difficult because the data wasn't in OpenStreetMap, and the 16 MB KML file was far too large for a web browser. I ended up writing a small script that took the ESRI file and created custom tiles for the map, all 70,000 of them. My laptop didn't appreciate the CPU load, so I launched an EC2 instance and eventually uploaded the tiles to S3. If you would like to use them, they are available at http://cdn.kelvinism.com/audivisions/. The code snippet is:

```javascript
map.addLayer(new OpenLayers.Layer.TMS("Election Boundaries", "http://cdn.kelvinism.com/audivisions/", { type: 'png', getURL: osm_getTileURL, displayOutsideMaxExtent: true, isBaseLayer: false, wrapDateLine: true }));
```

After creating the tiles, I added the lobby agency locations. Nearly everyone on our team stayed up the entire night; most of us didn't sleep at all. After finding a JSON feed containing the agency offices, I was able to map each representative to a division name and then to the division's longitude and latitude. Finally, although it remained slightly incomplete, I created a simple table showing the total value of government funds paid to each supplier. There were 7,000 suppliers, however, so displaying all of them in JavaScript wasn't practical. Even in its current form, the map was resource-intensive because it contained 200 to 300 pins.

Overall, this project was tremendous fun. The judges gave it a "Best in Show" award, which I missed because I needed to return to Sydney. Team 7 brought together people from different fields with complementary skills and solid experience. That range of backgrounds became clear when several developers compared revision control systems while our non-coder asked what the acronyms meant. Her questions helped inspire large parts of the project.

We considered entering it in the mashup contest, but a few things needed refinement. For instance, I wanted to make the map lighter and add the suppliers to it. Alex had a few ideas up his sleeve as well.

Our entry: [LobbyClue](http://team7.govhack.net.tmp.anchor.net.au/)

 Update: We received a Notable Mashing Achievement in the [MashupAustralia](http://mashupaustralia.org/) competition. Good job, team!
