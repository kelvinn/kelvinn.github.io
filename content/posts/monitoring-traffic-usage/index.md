---
title: 'Monitoring Traffic Usage'
date: 2006-08-29T20:30:00.004+10:00
draft: false
url: /2006/08/monitoring-traffic-usage_3593.html
tags: 
- nfsen
- projects
- netflow
---

Status:  ✅ 
  

One of the greatest benefits, in my opinion, of Cisco routers is the ability to generate netflows. In a lot of ways, I would prefer to do this than implement some appliance (say, using ntop). The ability to analyse the amount of traffic becomes extremely valuable. Not only can one measure the amount of traffic, but the type of traffic that is being generated through the network.

  

Using a similar configuration, I setup all four Ciscos to export netflows that stream back to a server in the States. I decided to use [nfdump](http://nfdump.sourceforge.net) as a collector. After the dumps are collected, it is simple to setup [nfsen](http://nfsen.sourceforge.net) to parse and analyse the received flows. It even allows you to generate [really pretty graphs](http://nfsen.sourceforge.net/details-graphs.png).

So, why do this? For starters, collecting netflows allows the basic analysis of data, which can tell you several things. You can know instantly how saturated your connection is, if there are any anomalies, if there is any file sharing going on or when heavy traffic usage is. For instance, if the connection becomes slow during the end of the day, you can analyse what protocol is used the most during that time. Or, as was my case, hunting down virus infected computers that were fully saturating a 10mbit pipe.

  
  

**A week in the life of NFSEN:**

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEivEGoFqSfZAEI3gQLtho98ejnUaGACDCELHII6McP4zOscQvHaE4dHRT40tBAM_CPiFZSV5ajMWYC9cN_K0G6gLO_qROJahVJYNvr2Y3arC3wH1n0gZX-WGoEPtnABzwggUEgRrr4zBqBy/s800/monitorbw.jpg)](http://picasaweb.google.com/lh/photo/NiYBlgwbHY8Xa2vA0j1asw?feat=embedwebsite)