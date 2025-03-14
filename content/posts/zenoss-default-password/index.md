---
title: 'Zenoss Default Password'
date: 2008-12-20T21:30:00.002+11:00
draft: false
url: /2008/12/zenoss-default-password_1357.html
tags: 
- nms
- zenoss
- python
- howtos
---

I've evaluated Zenoss before, but forgot the default password, and searching for it didn't come up with anything quickly. I tried everything under the sun: password, 1234, admin, God, Sex, but alas, grep to the rescue:

```bash
kelvin@monitor:/usr/local/zenoss/zenoss/etc$ grep admin *
hubpasswd:admin:zenoss

```  
  

Update: it is listed on page 4 of the Admin PDF :)