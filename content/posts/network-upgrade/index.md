---
title: 'Network Upgrade'
date: 2005-11-14T21:30:00.003+11:00
draft: false
url: /2005/11/network-upgrade_1831.html
tags: 
- projects
---

Status:  ✅ 
  

A network upgrade is in order, since we are depending more and more on our internet connectivity. Historically we have been using D-Link "Business Grade" equipment over DSL lines (decent bandwidth, but not 100% reliable, plus latency that is a little high). Time for an upgrade.

Since FiOS isn't offered yet where our office is located, we had to settle on a T1. However, since both locations in the States will have T1s through the same company, the quality should be decent. Since I'm telecommuting now, my colleague organized what company to order the T1 through, and had the line installed. Since our offices are both quite small, there isn't a need for any huge routers, we aren't moving a tremendous amount of traffic. Then again, we do need a certain amount of features. Initially the T1 company almost required us to use their equipment (which was luckily discounted highly), and after we gave them our set of requirements, they gave us a pair of Cisco 1723s, which I was a little skeptical about. A Cisco technician came out and sort of set them up (enough for me to gain remote access at least). However, a slew of issues surrounded the 1723s. The routing wasn't setup up quite properly, and the IOS was a little outdated.

Ultimately it turns out the routers weren't right, and wouldn't support our requirements (which was my guess in the first place). Oh well. A quick call to [CDW](http://www.cdw.com) and we had a pair of Cisco 1841s sent to Portland. After some widgetry magic (my knowledge of the Cisco CLI, to some degree at least) I got them both configured for their respective networks to run over the T1, then quickly setup NAT and then IPSec. Overall they run very smooth, and after installation they just have kept working.

So, there you have it. A quick network upgrade in two sites. Go Cisco.