---
title: 'New File and Webapp Server'
date: 2006-01-13T21:30:00.003+11:00
draft: false
url: /2006/01/new-file-and-webapp-server_9847.html
tags: 
- projects
---

Status:  ✅ 
  

Time has come to upgrade a few servers in the office. An older P4 2.8 was being used as a webapp server, and that needs to go. The resource utilization wasn't too much of an issue, however the computer was aging. Plus, it wasn't strictly built to host critical services, but since we grew so quickly, it is what was available. Additionally, the PDC was hosting user files and with these mounting in size, a dedicated file server is in order.

  

Oh, and Ian and I are on a strict budget, as usual.

[Our trusty CDW](http://www.cdw.com) shipped over two IBM rackmounts. Plenty of CPU and RAM to grow, the key feature that we were needing was hardware RAID1. With those shipped out, Ian screwed them into the rackmount and we started working on them. Both servers had Debian slapped on, and one then into a true LAMP server. On the LAMP server we also loaded up our ticketing system, and several IMAP based email accounts (good ol' Dovecot).

On the other server was setup as a dedicated file server. For several reasons, including the strict budget, we synced Samba up to the 2003 PDC. Thus, all profiles (through file redirection) are mapped to the Samba box, which does auth via kerberos back to the PDC. Besides user profiles, several shared folders exist, and access is based on GPO. I must admit, Samba+Windows2003 is a very handy combo.