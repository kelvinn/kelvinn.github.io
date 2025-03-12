---
title: 'Error opening /dev/sda: No medium found'
date: 2014-03-01T10:02:00.000+11:00
draft: false
url: /2014/03/error-opening-devsda-no-medium-found.html
tags: 
- linux
- tips and tricks
- howtos
---

I have had this issue before, solved it, and had it again.  
  
Let's say you plug in a USB drive into a Linux machine, and try to access it (mount it, partition it with fdisk/parted, or format it), and you get the error  

```bash
Error opening /dev/sda: No medium found  
```
  
Naturally the first thing you will do is ensure that it appeared when you plugged it in, so you run 'dmesg' and get:  

```bash
sd 2:0:0:0: [sda] 125045424 512-byte logical blocks: (64.0 GB/59.6 GiB)  
```
  
And it appears in /dev  

```bash
Computer:~ $ ls /dev/sd*  
/dev/sda  
Computer:~ $  
```
  
Now what? Here's what has bitten me twice: make sure the drive has enough power. Let's say you mounted a 2.5" USB drive into a Raspberry Pi. The Pi probably doesn't have enough current to power the drive, but it _does_ have enough to make the drive recognisable. Or, if you are like me, the USB charger powering the drive is faulty, so even though it has power, it doesn't have enough.  
  
The next troubleshooting step should be obvious: give the drive enough power to completely spin up.