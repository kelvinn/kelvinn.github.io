---
title: 'Server Virtualization'
date: 2006-01-24T21:30:00.002+11:00
draft: false
url: /2006/01/server-virtualization_5778.html
tags: 
- articles
- virtualization
---

We don't want to have a billion servers each doing their own task -- so what can we use as a solution? Server virtualization (or semi-virtualization or para-virtualization). This involves cutting down a server into mini servers that each have full customization. Our VPS at hostmysite is like this. So why would you want to do this? A few reasons actually.

\-Localize exploits. Let's say DNS gets exploited -- the access gained would only be for DNS, and not for mail and web and everything else.

\-Easy "upgrades," backups and redundancy. Let's say we start to use MySQL more and more, but the server can't handle it. To upgrade (ignoring replication for this example) we could just turn off the virtual server (in essense lock files), move it to other server, drop it into another server that is setup to do virtualization, and turn it it on. Nearly no downtime, and you know it will work.

Anyhow, worth looking at. Here are some of the most mature linux virtualization packages out there:

http://openvz.org/ -- This is the open source version of hostmysites VPS. The main difference is it isn't setup for doing mass hosting (like, 1000 VPSs on a huge mainframe).

http://www.openvps.org/

http://linux-vserver.org/ -- Very plain website, but there is news that the authors are pushing for this code to be included in the Linux kernal natively.

http://www.cl.cam.ac.uk/Research/SRG/netos/xen/ -- I've heard rumors also about this being one of the most advanced.

http://www.vmware.com/ -- The one and only. This is full virtualization so will contain the most overhead (some of the previous packages have almost no overhead, not even 1%). Oh yea, and this "costs" money.