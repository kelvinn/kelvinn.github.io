---
title: 'Building Custom LiveCDs'
date: 2006-01-26T21:30:00.002+11:00
draft: false
url: /2006/01/building-custom-livecds_4795.html
tags: 
- linux
- articles
- gentoo
- tips and tricks
---

I have a feeling we will shortly be deploying many Linux servers to perform certain actions. Maybe we will implement Asterisk to be used as a VoIP interchange between locations, maybe the backup servers will be Linux based, maybe the BDCs.

One thing that could speed up implementation at remote sites is to build live cds for certain purposes. For instance, on the file server in PDX to keep updated live cds for certain projects. Like, a BDC live cd or a backup live cd. Already setup with the most current packages (or scripts to fetch+install them). So when we get to the site we just put the CD in, click or type "load" and poof, the server is installed and configured.

These links (haven't read all of the process) may be helpful:

http://www.linuxjournal.com/article/7233

http://gentoo-wiki.com/HOWTO\_build\_a\_LiveCD\_from\_scratch