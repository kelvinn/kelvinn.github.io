---
title: 'An Upgrade in China'
date: 2006-06-02T20:30:00.003+10:00
draft: false
url: /2006/06/an-upgrade-in-china_4087.html
tags: 
- projects
---

Status:  ✅ 
  

Time has come to bring another network on the VPN, and perform some more upgrades. The usual by now, I guess.

- Get China on VPN  
- Limit access to other locations  
- Update all systems  
- Perform security audits  
- Upgrade wifi  
- Setup video conferencing  
  
  

Ian and I set off for our China office out of Hong Kong, and the next day started working. Total preparation was around a month, maybe a little large, mainly due to red tape. We first acquired assistance of IBM China, who were of a great help aiding us in finding our desired Cisco. One of the most important factors, which we couldn't resolve by purchasing the Cisco in the States, is support/warranty contracts (if the Cisco totally dies, what then). Through our contact we were also able to find some local vendors that would support Wifi and the Cisco, in case of an emergency.

Before leaving I prepared the necessary configurations for the Cisco, or at least a good guide to start from. The technician who came out tried to get things going through the built in GUI, however wasn't have so much luck. I took over using my pre-built configuration and soon (we swapped out the old router with the Cisco during lunch) everything, including overloaded NAT, was working fine. By the time employees came back from lunch, they couldn't notice any difference.

While the Cisco tech (who I believe is a good guy, even though I did the Cisco install) was waiting for some paper work went through and upgraded the way obsolete wifi point from WEP (which wasn't even turned on anyways) to WPA. The reasons for this, especially connected to the VPN, are very obvious. Technically the AP wasn't supposed to support WPA, but he found the correct Chinese firmware and it worked. This is good, as the new AP wouldn't be coming for a little while.

Next on the list was video conferencing. The solution was the path of least resistance: Skype on a laptop. Ian took this one, setup the laptop, and tested conferencing back to the States.

On the agenda for that night was VPN. The problem with bringing the China office on the VPN is one of security. Virus' were quite prevalent (e.g. my shared drive on my Linux laptop, to use as a sandbox, had a couple .exe files dropped into it. All with rather odd names...) -- so we first ran some security audits. Nessus was a great help, as always, and we tracked down over [an UNFATHOMABLE amount of] _critical_ holes. Picking the biggest culprits we started patching computers, removing spyware and running anti-virus. Slowly (a few days) we got the number knocked down significantly.

Lastly I hooked China up to the VPN. In order to do this safely I created some very strict access lists, to only allow outgoing communication over ports 80 and 443 (since that is all they needed at that point). Previously setup we had a webshare website (auth linked to the PDC), so no need to open any other ports.

Overall we completed what we set out to do. We made a few good contacts, achieved our goals, and once again learned more about doing I.T. overseas.