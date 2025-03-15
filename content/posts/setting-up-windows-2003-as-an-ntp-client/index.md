---
title: 'Setting up Windows 2003 as an NTP Client'
date: 2008-04-29T20:30:00.008+10:00
draft: false
url: /2008/04/setting-up-windows-2003-as-ntp-client_4269.html
tags: 
- windows
- ntp
- howtos
---

I have had to search for the commands to setup a Windows 2003 box as an ntp client a few times now, so have decided to finally write them down here for my own good measure. Funny thing is, I'm pretty sure there are three ways to setup a 2003 box as an ntp client.

#### 1) Via the CLI

  
  

Open up the cmd prompt and type in:

```bash
w32tm /config /manualpeerlist:"0.pool.ntp.org 1.pool.ntp.org 2.pool.ntp.org 3.pool.ntp.org" 
/syncfromflags:MANUAL /reliable:YES /update

```  
  

#### 2) Via the CLI, option 2

  
  
```bash
net time setsntp: "0.pool.ntp.org 1.pool.ntp.org 2.pool.ntp.org 3.pool.ntp.org"

```  
  

#### 3) Via GUI

  
  

Type in **gpedit.msc** and your local GPO editor will pop up. Go to the folder as indicated in the below screenshot and Enable the "Enable Windows NTP Client" option. Next set the "Configure Windows NTP Client" option to whatever time servers you so choose. As always, make sure to keep the 0x1 at the end.