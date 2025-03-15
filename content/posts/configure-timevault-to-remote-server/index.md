---
title: 'Configure Timevault to Remote Server'
date: 2008-11-02T21:30:00.011+11:00
draft: false
url: /2008/11/configure-timevault-to-remote-server_2418.html
tags: 
- ubuntu
- linux
- howtos
---

Using TimeVault with a shared drive as a backend is actually quite easy, but it does require a few special things setup. Note: this is gonna be a brief summary.

  

Install samba-tools, smbfs...

  
```bash
sudo apt-get install samba-tools smbfs

```  

A lot more other stuff may install as well.

  

Create a script that mounts your samba share. You could also do this in fstab, but I tend to suspend my laptop when I come home, and I like clicking buttons.

  
```bash
#!/bin/bash

mount -t cifs //192.168.44.2/kelvin /mnt/backups -o netbiosname=KELVIN-PC,iocharset=utf8,credentials=/home/kelvin/Apps/.smb-details.txt

```  
  

smb-details.txt includes:

```bash
username=DOMAIN\\kelvin
password=mypassword

```  
  

Finally, create a folder called 'timevault' or something inside your mapped share, then launch TimeVault and configure it to use the above mentioned /mnt/backups/timevault folder. Configure Timevault as normal.