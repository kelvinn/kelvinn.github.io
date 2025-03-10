---
title: 'Lenny on Ebox 3310A'
date: 2009-11-03T21:30:00.002+11:00
draft: false
url: /2009/11/lenny-on-ebox-3310a_5547.html
tags: 
- ubuntu
- linux
- embedded
- howtos
- ebox
---

As a preface, I take absolutely no credit for the below instructions. Stefan L kindly sent these through these instructions on installing Debian on the 3310A. I need to send a special thanks to Stefan, as I receive a lot of emails about the 3310 - but I don't have one, so I can't really do much:(  
The only edit I've done is change out the links to my files on S3. If you find these helpful, or want to suggest an alteration, please leave a comment.  
Download these files first:  

*   [2.6.31.5 kernel image](http://cdn.kelvinism.com/ebox/linux-image-2.6.31.5-vortex86-sl3_2.6.31.5-vortex86-sl3-10.00.Custom_i386.deb)
*   [2.6.31.5 kernel headers](http://cdn.kelvinism.com/ebox/linux-headers-2.6.31.5-vortex86-sl3_2.6.31.5-vortex86-sl3-10.00.Custom_i386.deb)
*   [2.6.31-14 custom pata\_rdc module](http://cdn.kelvinism.com/ebox/initrd.img-2.6.31-14-generic-pata_rdc)

  
  
The steps to install Lenny to CF in brief is:  

*   1) Install i386 version of Lenny to CF on another computer
*   2) Add the revised kernel deb with dpkg -i \*.deb
*   3) Change fstab from hda1 to sdb1 (sda1 if there is no micro sd card) - uuids  
    may be better
*   4) Change /boot/grub/menu.lst to:
```
title           Debian GNU/Linux, kernel 2.6.31.5-vortex86-sl3
root            (hd0,0)
kernel          /boot/vmlinuz-2.6.31.5-vortex86-sl3 root=/dev/sdb1 ro verbose

```5) Probably need to change /boot/grub/device.map```
(hd1)   /dev/sda
(hd0)   /dev/sdb

```With no micro sd it would be:```
(hd0) /dev/sda

```6) delete the section below "# PCI device ...." in /etc/udev/rules.d/70-persistent-net.rules (Otherwise the eBox network gets remapped to eth1 and may not appear if only eth0 is specified in the network settings) 7) **Reboot & pray** (bold added by Kelvin:P ). The next one is a revised initrd for the current Ubuntu 9.10: http://staff.washington.edu/lombaard/initrd.img-2.6.31-14-generic-pata\_rdc [2.6.31-14 pata\_rdc module for Ubuntu 9.10](http://cdn.kelvinism.com/ebox/initrd.img-2.6.31-14-generic-pata_rdc-Ubuntu_9.10) The two changes are: blacklist dm\_raid45 & add pata-rdc.ko "blacklist dm\_raid45" needs to be added to /etc/modprobe.d/blacklist.conf I managed to boot into gnome desktop without any further problems. I have enabled PCI IDE Bus Mastering, plug&play and IDE native mode in the bios. Hope this saves someone else a few hours of frustration.