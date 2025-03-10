---
title: 'Last Xenful Comments'
date: 2007-06-29T20:30:00.007+10:00
draft: false
url: /2007/06/last-xenful-comments_2649.html
tags: 
- articles
- amazon
- virtualization
- xen
---

One of the biggest things I regret is not utilizing Xen more. I've finally been admitted to Amazon's EC2 Limited Beta, just two days before I leave, so not enough time to actually do anything fun. However, I think Xen is an ideal infrastructure aid for SMEs in particular. The cost of technology is continuing to decrease, which means bigger servers cost less. This is great for the small/branch office. Let me explain.

One of the themes I noticed while studying and taking the MCSE was that the solution to the majority of the problems was to just buy more servers. Even for simple things like DHCP, buy another server. I've always operated on a limited budget, and anyways, I don't think money should be wasted on resources when it isn't needed. With a VT chipset, you aren't tied to any OS in particular.

My friend Ian and I were talking and he illustrated a great usage of Xen through his work. What he's ended up doing is installing the Small Business Edition of Server 2003 in a Xen node. The reasoning is that SBE is, apparently extremely difficult to create backups of -- mainly due to odd file locking behavior. I've had similar thoughts, but mainly taking advantage of Xen's migration feature. The idea of taking a small branch office and putting everything on a Xen server is quite appealing to me, especially considering a second server could be used to create virtual hot spare.

As you can see, I like Xen. I've found it relatively easy to install, and the fact that it is starting to come bundled with recent distributions is pretty darn, sweet.