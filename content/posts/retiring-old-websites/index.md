---
title: 'Retiring Old Websites'
date: 2010-05-16T20:30:00.008+10:00
draft: false
url: /2010/05/retiring-old-websites_2251.html
tags: 
- retire
- apache
- redirect
- howtos
---

Sometimes all good things [come to an end](http://www.kelvinism.com/tech-blog/rip-old-sites/). There aren't too many links going into either of these sites, but I'd like to redirect all of them to a page on my blog saying the website doesn't exist anymore. I've already created simple screendumps for nostalgic purposes with the Firefox plugin Screengrab!, so the remaining simple server-side steps are:

*   1) Edit the DNS records from the live server to the server with the notice page is on.
*   2) Create a new vhost on the server the notice exists on, add old websites as ServerAlias.
*   3) Add a redirect in the vhost to the notice about the retired sites.
*   4) Reload apache config.

  
  

The below vhost entry will redirect any link to the retired sites to the notice page.

```
 ServerName ducktracker.com
ServerAlias www.ducktracker.com blogmozaic.com www.blogmozaic.com

RedirectMatch permanent (.\*)$ http://www.kelvinism.com/tech-blog/rip-old-sites/ 


```