---
title: 'Very Remote Backups'
date: 2006-06-22T20:30:00.003+10:00
draft: false
url: /2006/06/very-remote-backups_5452.html
tags: 
- projects
---

Status:  
  

Backing up across the states has worked decently well, but due to several changes a more dedicated backup solution is in order. Desiring something quick, simple and inexpensive, research revealed a company that would perfectly fit the requirements. [iBackup](http://www.ibackup.com) was a perfect substitute - instead of SSH+rsync to another office, iBackup provides rsync over ssl to their data center. A few simple changes to the cron job, and backup location is thus changed.