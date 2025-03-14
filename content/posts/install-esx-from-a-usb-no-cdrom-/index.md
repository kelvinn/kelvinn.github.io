---
title: 'Install ESX from a USB (no CDROM)'
date: 2008-12-07T21:30:00.011+11:00
draft: false
url: /2008/12/install-esx-from-usb-no-cdrom_3723.html
tags: 
- esxi
- vmware
- howtos
---

My little server doesn't have a cdrom, but I didn't want to actually run ESX from a USB (i.e. esx-on-a-stick). Here are my notes of configuring a flash disk to boot the ESX installer (so you can install it onto a local disk). For this demo, my USB is /dev/sdb

  
  
1) Install the syslinux utils to your computer (apt-get install syslinux mboot)  
2) Install the MBR  
  
```bash
sudo install-mbr /dev/sdb

```  
3) Copy all the files from the ISO to your fat32 formated partition  
4) Install syslinux  
  
```bash
sudo syslinux /dev/sdb1

```  
5) Move isolinux.cfg to syslinux.cfg, and try booting. If it doesn't work, edit syslinux.cfg says something like:  
  
```bash
default menu.c32
menu title ESXi Boot
timeout 100

label ESXi
menu label Boot VMware ESXi
kernel mboot.c32
append vmkernel.gz --- binmod.tgz --- environ.tgz --- cim.tgz
ipappend 2

```  
6) Unplug your USB, put it in your server, reboot, boot to USB-HDD (or select the USB disk), and install ESX to the local disk. You will likely be greeted with a sign saying "MBR FA:", where you need to press "A" and then "1".