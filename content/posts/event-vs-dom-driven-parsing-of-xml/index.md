---
title: 'Event vs. DOM Driven Parsing of XML'
date: 2008-04-29T20:30:00.007+10:00
draft: false
url: /2008/04/event-vs-dom-driven-parsing-of-xml_6678.html
tags: 
- graphing
- articles
- xml
- gpx
---

I recently have been [playing](http://www.kelvinism.com/tech-blog/baby-steps-graphing-traffic/) with parsing GPX files and spitting out the results into a special KML file. I initially wrote a parser using minidom, yet after running this the first time -- and my Core2Duo laptop reaching 100% utilization for 10 seconds -- I realized I needed to re-write it using something else.

I spent a little time reading the different parsers for XML and eventually read more about [cElementTree](http://effbot.org/zone/celementtree.htm). And it is included with Python2.5, sweet.

I quickly rewrote the code and did some tests. First, the two bits of code for parsing my GPX file:

**minidom-speed.py**

```
#!/usr/bin/python

from xml.dom import minidom
from genshi.template import TemplateLoader

def collect\_info():
dom = minidom.parse('airport.gpx')
for node in dom.getElementsByTagName('trkpt'):
lat = node.getAttribute('lat')
lon = node.getAttribute('lon')
speed = node.getElementsByTagName('speed')\[0\].firstChild.data
speed = float(speed) \* 10
coords = '%s,%s' % (lon, lat)
coords\_speed = '%s,%s' % (coords, speed)
yield {
'coordinates': coords\_speed
}

loader = TemplateLoader(\['.'\])
template = loader.load('template-speed.kml')
stream = template.generate(collection=collect\_info())

f = open('minidom.kml', 'w')
f.write(stream.render())

```  
  

**cet-speed.py**

```
#!/usr/bin/python

import sys,os
import xml.etree.cElementTree as ET
import string
from genshi.template import TemplateLoader

def collect\_info():
mainNS=string.Template("{http://www.topografix.com/GPX/1/0}$tag")

wptTag=mainNS.substitute(tag="trkpt")
nameTag=mainNS.substitute(tag="speed")

et=ET.parse(open("airport.gpx"))
for wpt in et.findall("//"+wptTag):
wptinfo=\[\]
wptinfo.append(wpt.get("lon"))
wptinfo.append(wpt.get("lat"))
wptinfo.append(str(float(wpt.findtext(nameTag)) \* 10))
coords\_speed = ",".join(wptinfo)
yield {
'coordinates': coords\_speed,
}

loader = TemplateLoader(\['.'\])
template = loader.load('template-speed.kml')
stream = template.generate(collection=collect\_info())

f = open('cet.kml', 'w')
f.write(stream.render())

```  
  

The speed difference is not just noticeable, but **very** noticeable.

**minidom-speed.py**

```
$ python -m cProfile minidom-speed.py
4405376 function calls (3787047 primitive calls) in 32.142 CPU seconds

```  
  

**cet-speed.py**

```
$ python -m cProfile cet-speed.py
1082061 function calls (904167 primitive calls) in 6.736 CPU seconds

```  
  

A quarter as many calls and almost 5x faster -- at least that's how I interpret the results. Much better!