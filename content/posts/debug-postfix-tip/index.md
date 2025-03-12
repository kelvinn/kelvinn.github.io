---
title: 'Debug Postfix Tip'
date: 2010-05-20T20:30:00.002+10:00
draft: false
url: /2010/05/debug-postfix-tip_7051.html
tags: 
- debug
- error
- howtos
- postfix
---

One thing I love about open source stuff is that the developers usually take great care to allow awesome debug messages. There's a catch-22, however: how much logging to enable? Today I was creating a Postfix/Dovecot/Postgresql install and I kept getting an error message in mail.log, but it wasn't very helpful.

Luckily you can turn up the verbosity in Postfix for error messages. You'll need to find out what component is in error, e.g. "postfix/virtual[4467]: warning:", and then open master.cf. Add a -v to the end of the daemon that's faulting, and you'll get more logging than you know what to do with.

```bash
virtual   unix  -       n       n       -       -       virtual -v

```  
  

I hope this helps somebody. You can read more debugging tips on the Postfix [DEBUG readme](http://www.postfix.org/DEBUG_README.html).