---
title: 'Track My Hours Please'
date: 2005-07-31T20:30:00.003+10:00
draft: false
url: /2005/07/track-my-hours-please_6190.html
tags: 
- projects
---

Status:  ✅ 
  

Initially all CSRs were hired as temps, which means they had their own timesheets. Some new people have been hired as full/part-time employees, so we need to handle their timesheets -- plus, several people (including myself) are paid on an hourly basis. Perfect time to setup a Timesheet.

Since we are still small, with no ERP, and I don't have time or desire to write a timesheet app, I decided to do some research. I found a few on SourceForge, but I wanted something uber-simple to use and uber-simple to install. I settled upon [TimesheetPHP](http://www.timesheetphp.com/). Luckily it even allowed LDAP support, which would be useful eventually for SSO. Installation was a breeze, and now everybody logs hours onto the an intraweb server.

A simple, simple solution to a simple, simple problem.