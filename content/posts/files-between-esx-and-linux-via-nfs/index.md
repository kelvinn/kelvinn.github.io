---
title: 'Files between ESX and Linux via NFS'
date: 2009-03-02T21:30:00.002+11:00
draft: false
url: /2009/03/files-between-esx-and-linux-via-nfs_6022.html
tags: 
- esxi
- nfs
- vmware
- linux
- howtos
---

I like ESX. I like Linux. It is absurdly easy to configure Linux as an NFS server and mount it in ESXIi).

**Installed NFS**

I currently use Ubuntu Server for my home lab, but the process is basically the same for Red Hat and derivatives.

```bash
sudo apt-get install nfs-common
sudo apt-get install nfs-kernel-server

```  

Next, configure NFS so it can server your local LAN. Normally you would list only specific servers, but, well, we're being cheap and dirty today. Open /etc/exports in VI or your editor of choice.

**/etc/exports**  
```bash
/media/disk/Images 192.168.0.0/24(rw,no_root_squash,async

```  

Restart NFS.

```bash
sudo /etc/init.d/nfs-common

```  
Go to Configuration -> Storage -> Add Storage.  
  
Select NFS  
  
Fill in the info, see screenshot.  
  
Wait a minute. Voila! New datastore.  
  
  
**Images to come shortly.**