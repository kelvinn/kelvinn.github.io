---
title: 'Lightweight Detection'
date: 2007-01-23T21:30:00.002+11:00
draft: false
url: /2007/01/lightweight-detection_8013.html
tags: 
- articles
- IDS
- hacking
---

I love my Snort, I really do.  But sometimes, I just don't need all the extra overhead -- sometimes the resources on a server are somewhat, limited.  Looking for a solution I stumbled upon [PSAD](http://www.cipherdyne.com/psad/) , a way to detect port scans.  Since port scans are often one of the first tactics used to find vulnerabilities on a server, it is a pretty good idea to detect them.   Depending on the attack, I receive a nice little email telling me what is going on.  To test it out I first fired up nmap, and received a few emails.  Next I fired up nessus with updated plugins -- you can be the judge.  I now have 50 emails from myself telling me somebody is doing something naughty:  
```bash
\=-=-=-=-=-=-=-=-=-=-=-= Tue Jan 23 10:30:04 2007 =-=-=-=-=-=-=-=-=-=-=-=


         Danger level: [5] (out of 5) Multi-Protocol

    Scanned tcp ports: [11-41111: 337 packets]
            tcp flags: [SYN: 337 packets, Nmap: -sT or -sS]
       iptables chain: INPUT, 337 packets

               Source: 218.167.75.27
                  DNS: 218-167-75-27.dynamic.hinet.net

          Destination: 64.79.194.165
                  DNS: kelvinism.com

      Syslog hostname: kelvinism

     Current interval: Tue Jan 23 10:29:54 2007 (start)
                       Tue Jan 23 10:30:04 2007 (end)
```