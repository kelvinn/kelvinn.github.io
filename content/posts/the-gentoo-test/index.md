---
title: 'The Gentoo test'
date: 2007-05-24T20:30:00.004+10:00
draft: false
url: /2007/05/the-gentoo-test_1297.html
tags: 
- linux
- articles
---

I have a love-hate relationship with Linux. I love it because if there is a problem, I can actually tinker and find the problem and fix it. But I hate it because I like to tinker.

Recently I've been doing a fair amount of Django programming -- enjoying every minute of it. After completing several of my projects I decided to do some benchmarks, and the results are in! Generally I can server cached/semi-cached pages at about 200req/sec. 200req! Considering this is 5,000,000 or so requests a day, and a number I am never going to reach, I still began to wonder: why isn't it higher? I mean, serving a static html page is at like 1000+ req/sec, so why would a cached page be significantly different? I started exploring and noticed that Apache would spike the CPU. Ok, time to be thorough, and as I said, I like to tinker.

I tried lighttpd as a fastcgi to python -- not a significant different, basically the same. Next I tried several versions of python -- one from 2.4 and one from 2.5, one as a package and one from source -- same results. High cpu usage. Thinking it could be something related to my VPS (or some odd limit within Debian) I decided, ok, I'll reinstall.

I reinstalled and got things working pretty quickly. The only slight hiccup was postfix/dovecot, cause postfix insists on being in a jail (and my configs are all setup for that). Also, Chinese support in Apache isn't working. Regardless, I re-ran the benchmarks and the results were the same -- so, it isn't related to my previous install after all. Doh.

I'll evaluate Gentoo as a server setup for a little while, but I'm thinking I'll do a quick reinstall of Debian.