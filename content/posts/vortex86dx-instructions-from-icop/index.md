---
title: 'Vortex86DX Instructions from ICOP'
date: 2009-12-05T21:30:00.002+11:00
draft: false
url: /2009/12/vortex86dx-instructions-from-icop_3935.html
tags: 
- debian
- embedded
- howtos
- ebox
---

Alexandru T. and I have exchanged a few emails, and he sent through a few helpful suggestions that were provided from ICOP. I have included them below. Thanks Alexandru!

  
  
1. Install Debian 5.0 on a normal PC (using a netinst image, for minimal install)  
2. After installation boot normally from the same PC  
3. Then, take the kernel from ftp://icop.com.tw/DIS_info/VDX/operating_system/VDX_Linux/linux-image-2.6.30-vortex86mx_1.0_i386.deb and then issue the following commands :  
  
  
```bash
# dpkg -i  linux-image-2.6.30-vortex86mx_1.0_i386.deb
# update-initramfs -k 2.6.30-vortex86mx -c
# update-grub
# restart


```  
  
  
4. Then take the hard-drive and install it on the Vortex86DX  
5. When GRUB menu appears, press "e" and modify the boot loader as follows :  
  
  
```bash
root        (hd0,0)
kernel        /boot/vmlinuz-2.6.30-vortex86mx root=/dev/hdb1 ro         --> if hdb1 does not work you can try (hda1= Primary Master or hdc1=Secondary Master)
initrd        /boot/initrd.img-2.6.30-vortex86mx


```  
  
Then press b to boot  
  
  
  
6. After booting, go to /boot/grub/menu.lst and make modifications from above permanently, so you will boot without any intervention ;)  
  
  
  

**Edit:**Bob A. has also sent through some additional resources for your eboxing pleasures.

FYI - this Swedish company, [http://www.lweb.se/tag/ubuntu/](http://www.lweb.se/tag/ubuntu/), has a pre-made ISO for Ubuntu 8.04LTS with the correct kernel for the eBox 3300/3310. It even supports the new (1011) IDE controller on the recent models. You can just put the ISO on a thumb drive, stick it in your eBox, and install normally. No need to install first on another machine, and no need to update the kernel after you're done. If you're happy with running 8.04 then this is way easier than any other install option that I've found  
so far.