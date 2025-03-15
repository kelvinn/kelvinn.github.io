---
title: 'Quick Backups'
date: 2006-02-01T21:30:00.003+11:00
draft: false
url: /2006/02/quick-backups_2198.html
tags: 
- projects
---

Status:  ✅ 
  

All is well for some disasters, but what happens if our entire office burns down? SSH+rsync to the rescue, again.

I first setup the PDC and webapp server to backup to the file server on a regular basis (PDC: incremental every day, full on Saturday). Then the file server takes those backups (including the files stored on the file server) every night and syncs them with another server across the States. In case something drastic happens, these off-site backups should be a savior.