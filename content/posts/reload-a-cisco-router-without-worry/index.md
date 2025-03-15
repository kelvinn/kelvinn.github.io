---
title: 'Reload a Cisco Router WIthout Worry'
date: 2011-06-08T14:15:00.000+10:00
draft: false
url: /2011/06/reload-cisco-router-without-worry.html
tags: 
- tips and tricks
- cisco
- howtos
---

Recently I tried editing my Cisco's ACL at home on the train. It went something like this:  

*   I logged in
*   I started updating the ACL
*   I hit a blackspot in my 3g coverage
*   My command stops at "router(config)#access-"
*   I get an alert saying my home internet was down

Although it is simple enough to just ask her to "flip the switch on the black box", I still don't like doing it. Plus, if she's not home, I'm stuck. This accident immediately reminded me of one of a trait of the 'reload' command: it can be scheduled.  
  
In the case of updating a device remotely, it is as easy as:  
  
```plain
router# reload in 2
router# conf t
router(config)# [type in desired commands]
router(config)# exit
router# reload cancel

```  
If the commands are entered in fine, then cancel the reload. If there is a problem, then the router will reboot and resort to the startup config.