---
title: 'Resize a VMWare Image of Windows XP'
date: 2007-01-27T21:30:00.002+11:00
draft: false
url: /2007/01/resize-vmware-image-of-windows-xp_4908.html
tags: 
- howtos
---

Over the years I have been shrinking the number of computers I own.  At one point my dorm was littered with old P100s, running whatever OS I felt like playing with at the time.    
  
VMWare comes to help.  In this recent oops, an image I made (for Windows XP), was slightly too small.  I didn't feel like reinstalling XP + cruft, so just resized the image.  This is the process:  
  
  
1) Make Clone or just backup your VMWare image.  
  
2) Note: if your disk is a Dynamic Disk, you won't be able use GParted.  There is a chance you can use Disk Management inside Computer Managemen inside XP.  
  
3) Turn off VMWare image.  
  
4) Grow the image.    
  
  
  
```
 vmware-vdiskmanager -x sizeGB yourimagename.vmdk 
```  
  
  
5) Download the [GParted LiveCD](http://gparted.sourceforge.net/download.php)  
  
5) Change the CD-ROM drive of your  VMWare image to boot from the ISO you just downloaded.  
  
6) Boot VMWare image.  Make sure to press ESC right when it starts.  
  
7) Follow the instructions for GParted. I had to select the Xvesa option, then Done.  Choose your language and keyboard and resolution.  
  
8) GParted will come up.  First delete the partition (the empty one!), and make sure it says unallocated.  Then go up to Edit and hit Apply.  Then select the partition and say Resize.  Hit apply again.  
  
9) Reboot image.  Windows XP will come up, and go through checking the disk.  It will reboot again, and you should then be able to log in.