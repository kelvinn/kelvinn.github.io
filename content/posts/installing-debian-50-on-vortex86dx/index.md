---
title: 'Installing Debian 5.0 on Vortex86DX'
date: 2009-06-14T20:30:00.006+10:00
draft: false
url: /2009/06/installing-debian-50-on-vortex86dx_3246.html
tags: 
- kernel
- vortex86dx
- debian
- howtos
- compiling
- ebox
---

After writing about [compiling a new kernel](http://kelvinism.com/tech-blog/compiling-kernel-vortex86dx/) for the Vortex86DX, I've had quite a few people email me asking how I installed Debian in the first place. The installation is actually quite straightforward, but it involved several quirky techniques. After doing another install I decided to keep track of the process of installing Debian 5.0 on my eBox-3300.

The following guide assumes a few things. First, you are currently using Linux and a debian variety (although instructions could be altered if using Windows). Second, your USB shows up as /dev/sdb. Third, your eBox-3300 has the HDD set in Native mode. Forth, you are patient.

1. Download the custom vmlinuz and initrd.gz files from my site. Also, download the custom deb files we'll use near the end of installation:

```plain
http://cdn.kelvinism.com/ebox/vmlinuz
http://cdn.kelvinism.com/ebox/initrd.gz
http://cdn.kelvinism.com/ebox/linux-headers-2.6.29.3-vortex86dx.deb
http://cdn.kelvinism.com/ebox/linux-image-2.6.29.3-vortex86dx.deb

```  
  

2. Download an i386 netinst iso:

```plain
http://www.debian.org/CD/netinst/

```  
  

3. Make sure the USB has an MBR installed:

```bash
apt-get install syslinux mtools mbr
install-mbr /dev/sdb

```  

4. Format the device as FAT32 with whatever tool you like.
5. Run syslinux on it:

```bash
syslinux /dev/sdb1

```  
6. Mount the USB (or pull it out and plug it in again so it shows up on your desktop), and copy the downloaded vmlinuz, initrd, netinst.iso and deb files onto the USB. There should be a file called ldlinux.sys already; create a file called syslinux.cfg and put the following in it:

```bash
default vmlinuz
append initrd=initrd.gz root=/dev/rd/0 devfs=mount,dall rw DEBCONF_PRIORITY=medium

```  
  

It should look like this:

![Ebox files](http://cdn.kelvinism.com/images/ebox3300files.png)  
  
7. Unmount the USB, and put it in your eBox-3300. When the system boots up initially, hit F11. Select your USB device. Depending how you created the MBR it might come up as saying "MBR FA:". Press "A". When 1234F comes up, press "1". Press enter at the SYSLINUX "boot:" screen.
8. Proceed as normal through the menu. It will search for an ISO image, and should detect the netinst image you inserted earlier. When you get to the "Load installer components" section, it will complain about no kernel modules found. Select YES. On the next screen you shouldn't need to load any components, so hit continue. Proceed as normal.
9. If you are ever asked about starting PC card services, hit NO. Proceed as normal.
10. Eventually you will hit a screen that says LVM is not available, hit CONTINUE. Proceed as normal.
11. Near the end it will toss up a list of available kernels. Select either, it shouldn't matter. When you are allowed to select drivers to include in the initrd, select TARGETED. Proceed as normal.
12. You might get to a point where it says Install GRUB boot loader on a hard disk. This will fail. That's ok, just skip it and select "continue without boot loader".
13. You will end up on the "Finish the installation" menu. **DO NOT** finish! We now need to swap out the current kernel with one that works. Scroll down and select "Execute a shell". Press CONTINUE. Try these steps when the shell prompt appears:

```bash
cd hd-media
cp *.deb /target/usr/src/
cp vmlinuz /target/boot/vmlinuz-2.6.26-2.486
cp initrd.gz /target/boot/
cd /target/boot
gunzip initrd.gz
mv initrd initrd.img-2.6.26-2-486
reboot


```  
  

Your system will now reboot, and it should actually boot correctly. However, you're using a kernel that doesn't have any headers or modules, which means you can't activate anything. Once the box boots up, login and install the included custom kernels:

```bash
cd /usr/src
dpkg -i linux-image-2.6.29.3-vortex86dx.deb
dpkg -i linux-headers-2.6.29.3-vortex86dx.deb
reboot

```  
  

Once the system comes back up, you should be running a spiffy 2.6.29 kernel, with the ability to add modules.

You may want to follow the tuning section from the [MicroClient page](http://groups.google.com/group/microclient/web/ubuntu-on-microclient-sr) on Google Groups. I also modified my fstab file to help reduce wear on the CF card:

```bash
tmpfs /var/run tmpfs defaults,noatime 0 0
tmpfs /var/lock tmpfs defaults,noatime 0 0
tmpfs /var/tmp tmpfs defaults,noatime 0 0

```  

**Contribution 1:** [Francois Fleuret](http://www.idiap.ch/~fleuret/) emailed through a kind reminder that the qemu-onto-SD card method is a viable option. So, if you want to go the SD route, and have an SD reader, this might be what you're after!

```plain
Basically, install Debian on a SD card with qemu (start qemu with the
install disk iso as cdrom and the SD card as hda), while you are still
in qemu, download and install the kernel deb file

ftp://ftp.icop.com.tw/upload/Shawn/linux-image-2.6.27.9-vortex86dx_2.6.27.9-vortex86dx_i386.deb

then quit qemu, put the SD card in the box and reboot. You are done!


```  
  

If you want the source file for the above kernels, you can get it from here: [2.6.29-3 source](http://cdn.kelvinism.com/ebox/linux-source-2.6.29.3-vortex86dx.deb). I recently recompiled the kernel with some extra modules enabled (e.g. ecryptfs), so if you would like to try a newer kernel, you can download my updated kernels too:

```plain
http://cdn.kelvinism.com/ebox/linux-headers-2.6.30.4-vortex86dx.deb
http://cdn.kelvinism.com/ebox/linux-image-2.6.30.4-vortex86dx_2.6.30.4.deb

```  
  

**Contribution 2**: Trent L has also recompiled a 2.6.28 kernel with wireless extensions built into it, which is what was needed for his wireless card. He has kindly allowed me to distribute them; you can find them here:

```plain
http://cdn.kelvinism.com/ebox/linux-source-2.6.28.10_vortex86dx.deb
http://cdn.kelvinism.com/ebox/linux-image-2.6.28.10_vortex86dx.deb
http://cdn.kelvinism.com/ebox/linux-headers-2.6.28.10_vortex86dx.deb
http://cdn.kelvinism.com/ebox/2.6.28.config

```  

**Contribution 3**: If you have the ebox-3310, you can still read through this, but you may also want to see a [suggested installation method and kernels](http://kelvinism.com/howtos/lenny-ebox-3310a/) from Stefan.

**Contribution 4**: Alexandru T. sent through some instructions directly received from ICOP. I've added [another page](http://www.kelvinism.com/howtos/vortex86dx-instructions-icop/) with the details. Thanks Alex!

**Contribution 5:**: Rainbow sent through the solution if your kernel panics with:  
  

```plain
it report "kernel bug at fs/buffer.c 1864" and system go mad, even
> "halt" "reboot" take no effect.

```  
  
  

Rainbow reported that:

```plain
this issue cause by an error Vcore, 0.90v refered by datasheet, and it should be above 0.97.

```  
  
  

**Contribution 6:**: Bob's also sent through his [config](http://cdn.kelvinism.com/ebox/config-2.6.29.3-ziti.3) file.

**Contribution 7**: Bob A. has sent through some resources about a special ISO specific for the ebox. It has been added to [another page](http://www.kelvinism.com/howtos/vortex86dx-instructions-icop/).  
  

**Update**: I've needed to recompile a new Lenny vortex86dx-enabled kernel for 2.6.31.5: [image](http://cdn.kelvinism.com/ebox/linux-image-2.6.31.5-vortex86dx.deb), [headers](http://cdn.kelvinism.com/ebox/linux-headers-2.6.31.5-vortex86dx.deb), [source](http://cdn.kelvinism.com/ebox/linux-source-2.6.31.5-vortex86dx.deb) and [config](http://cdn.kelvinism.com/ebox/config-2.6.31.5).