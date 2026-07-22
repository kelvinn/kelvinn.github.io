---
title: "Six Simplifications in 2012"
date: 2013-01-09T23:07:00.001Z
url: /2013/01/seven-simplifications-in-2012.html
tags:
- travel
blogger_id: "tag:blogger.com,1999:blog-1700991654357243752.post-7442777766087359713"
blogger_post_id: "7442777766087359713"
blogger_status: "LIVE"
blogger_updated: 2013-01-10T04:06:20.025Z
---

1. Stopped hosting websites for people.

I cancelled almost all the domains I was hosting for other people and removed their websites from my server. Hosting websites generally does not take much time, but I still needed to manage backups, monitor them, and make sure everything worked. This was fun when I was younger: "Neat, I can host websites virtually for free!" Over time, however, the appeal faded. I now help with only two websites.

2. Stopped hosting my own websites.

I moved the remaining websites to either shared hosting or Red Hat's OpenShift. I still manage backups and monitoring, but I worry about them less. Most of the VPS providers I used started out fast but eventually became over-allocated and slow.

3. Moved my website to Blogger.

For years, I wrote the code that supported my website, but I realised I was spending more time adding small features than writing stories. Hosting the site on Google's App Engine meant I did not worry about uptime, but I still spent too much time on the code. Coding is relaxing for me; however, I would rather work on things that add more value.

4. Automated my backups.

For several years, especially while I was running Linux, I wrote the code to manage my own backups. I have now switched my backup system to CrashPlan and Dropbox. It is cheaper than running the backups myself, and I no longer worry about it.

5. Automated Price Watch Alerts

Instead of visiting several websites every day to look for things I want, I configured alerts for products whose prices fall below my threshold. OzBargain and Gumtree both let you save a search as an RSS feed, which you can open in Google Reader or configure IFTTT to email to you. I set up similar Amazon alerts with CamelCamelCamel.

6. Hosted Monitoring

For years, I ran my own monitoring with open-source tools. This usually worked well, but it meant one more system to support. I now monitor my small number of servers, one in the US and one in the UK, with hosted services. The best I have found are PaperTrail App for logs, RobotUptime for HTTP/ICMP, and New Relic for system resources.
