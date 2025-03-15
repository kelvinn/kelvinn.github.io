---
title: 'Where the heck is my Diskspace'
date: 2006-04-05T20:30:00.005+10:00
draft: false
url: /2006/04/where-is-my-diskspace_4579.html
tags: 
- linux
- articles
- tips and tricks
---

Logs spiraling crazy, we run out of disk space all the time. A nifty trick to find where the disk went is to issue: 

```bash
du -cks * |sort -rn |head -11
```

This returns where the disk usage is, and makes finding the bloated log a lot easier.