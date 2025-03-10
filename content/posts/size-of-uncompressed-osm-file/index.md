---
title: 'Size of Uncompressed OSM File'
date: 2008-01-08T21:30:00.002+11:00
draft: false
url: /2008/01/size-of-uncompressed-osm-file_95.html
tags: 
- openstreetmap
- vps
- articles
---

I've been playing around with [OSM](http://www.openstreetmap.com) a little lately, and have been meaning to construct my own slippy map. At first I wanted to do it on my VPS -- but with rather limited storage, and even more limited memory, there just isn't a way. Three problems exists: the first occurs when trying to use osm2pgsql to import the OSM file into the database. Current records state that this typically uses 650+ MB, something my 512MB VPS just doesn't have (although I'm writing some code that might make this possible in the future).

The second problem exists with CPU usage. Processes on my VPS don't really utilize the CPU much, which means renicing the process doesn't do a thing. The CPU pegs at 100%, as it is supposed to do, except that the VPS auto-kills processes that stay at 100% for any length of time. Luckily somebody wrote a program called "cpulimit" (apt-get install cpulimit) that will cap the CPU usage for a process.

The last problem that I thought about is _what if_ I could uncompress the file. Would that use less memory to stick it in the database? I searched and searched but couldn't find an answer to how big the actual .osm file is. I ultimately broke down and decided to spend the 50c it would take to get this all done with EC2, and write some scripts to automate it in the future.

However, since I've finally uncompressed the .osm, I can tell you that as of about January 1st, 2008, the uncompressed OSM size is 67GB.