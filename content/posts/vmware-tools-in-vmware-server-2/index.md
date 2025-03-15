---
title: 'VMware Tools in VMware Server 2'
date: 2008-08-01T20:30:00.005+10:00
draft: false
url: /2008/08/vmware-tools-in-vmware-server-2_6233.html
tags: 
- vmware
- howtos
---

Installing the tools in VMware Server 2 is a little different than Workstation or the previous versions of VMware Server. Under the Summary tab of your Virtual Machine, look for a link that says "Install VMware Tools" -- click it.

Wait for 'Success' to show up on the bottom, and jump into your virtual machine. Mount the tools as so:

```bash
mount /dev/cdrom /media/cdrom

```  
  

And install as normal (copy the .tar.gz to /usr/src, extract it, install it). Easy peasy.