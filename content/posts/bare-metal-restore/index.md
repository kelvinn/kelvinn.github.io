---
title: 'Bare-metal Restore'
date: 2007-05-25T20:30:00.004+10:00
draft: false
url: /2007/05/bare-metal-restore_7646.html
tags: 
- disaster recovery
- articles
---

As you can see by my previous post, my question to squeeze more req/sec from the server, I decided to try out Gentoo (again, last time was four years ago). Now, I like Gentoo, there is no doubt about that. However, I realized things took just **too** long to get set up. I guess that is the disadvantage of a source based package management tool. Back to Debian I go.

Two hours later everything was up and running -- and I guess I can't complain about a two hour bare-metal restore from one distro to another. And let me iterate, this isn't just a typical LAMP boxen. It's got:

  
*   apache/mod\_php/ssl with ~10 domains
  
*   apache/mod\_python/ssl with ~4 domains
  
*   lighttpd with ~5 domains (static files)
  
*   about 8 gigs of web data/images
  
*   svn repos + web\_dav access
  
*   mysql restored
  
*   postfix(chroot)/dovecot/sasl + mysql auth
  
*   home dirs restored
  
*   chrooted users again
  

  
  

I'm sure I missed something on this list, I was typing pretty quick. Well, that's the update. I'm gonna go tinker with mod\_cache some.