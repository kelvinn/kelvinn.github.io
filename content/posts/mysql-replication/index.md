---
title: 'MySQL Replication'
date: 2006-01-23T21:30:00.006+11:00
draft: false
url: /2006/01/mysql-replication_5029.html
tags: 
- projects
---

Status:  ✅ 
  

The webapp server is running fine, but backups are important. Better yet, a hot computer is a great idea. To do this, I setup an older spare rackmount as a 'live' webapp server, just in case. A duplicate LAMP was setup, web apps copied over SSH via rsync on a regular basis, and the icing on the cake: mysql replication.

So, if the dedicated webapp server dies a painful death, a quick change of IP for the webapp server in the internal DNS to the backup rackmount, and nobody will know anything happened.