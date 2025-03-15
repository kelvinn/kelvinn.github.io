---
title: 'LDAP Backend'
date: 2006-07-07T20:30:00.003+10:00
draft: false
url: /2006/07/ldap-backend_5061.html
tags: 
- projects
---

Status:  ✅ 
  

Users don't like to remember passwords, heck, I don't like to remember to use passwords. I decided to upgrade all the webapps to authenticate off the domain, welcome a start to SSO. To do this I implemented the [adldap php class](http://adldap.sourceforge.net/) to control authentication to each webapp. Thus, a simple GPO can control who has access to the app or not. A simple solution to a rather simple problem.