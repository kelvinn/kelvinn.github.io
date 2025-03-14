---
title: 'Compiling kernel for Vortex86dx'
date: 2009-05-10T20:30:00.002+10:00
draft: false
url: /2009/05/compiling-kernel-for-vortex86dx_5058.html
tags: 
- linux
- articles
- kernel
- ebox
---

**Update**: I've written up a [short tutorial](http://kelvinism.com/howtos/installing-debian-50-vortex86dx/) on the method I used to install Debian 5.0 on this device.

A few months ago I purchased the eBox-3300 from WDL Systems. The system was promptly shipped, and there were no "gotchas" from WDL. The little box fit my exact needs - it is small, and built very, very well. I flew back to Australia and, after some trial and error, installed Debian 5.0 on it. For quite some time I was just using the vmlinuz file provided by WDL, which was provided by ICOP (DMP). This worked well, but there were two issues:

  
  
1) I couldn't load any modules (e.g. NFS).  
2) I received an annoying email from OSSEC every few hours telling me it couldn't find modules.dep.  

At the end of last week I finally decided to do something about it, and considering this little box is "x86 compliant", I figured it wouldn't be too hard to create a new package. It has been several years since I last created a self-compiled Debian-packaged kernel, so I decided to document the process for the next time I do it. These steps are really just a summary - but if you have much Linux experience, they should be enough to guide you. If I'm unclear, just send me an email.

Because the eBox-3300 is embedded, I logically decided to create the package on another system. However, I wanted to maximize the chances of it working, so I installed Debian 5.0 in VirtualBox, updated it, and proceeded.

As a prep, you may need to install ncurses-dev and kernel-package in your build environment.

```bash
apt-get install ncurses-dev kernel-package

```  
  

1) Download latest kernel from: [http://www.kernel.org/pub/linux/kernel/v2.6/](http://www.kernel.org/pub/linux/kernel/v2.6/)
2) Download the DMP provided patch/config file for 2.6.27.3, copy it to /usr/src. Alternatively, you can borrow my [2.6.29.3 config](http://cdn.kelvinism.com/ebox/config-2.6.29.3-vortex86dx) Make a backup.
3) Untar kernel, cd into the kernel directory. Issue:

```bash
make menuconfig

```  
4) Configure kernel. If you used my config file, a lot of these should already be ticked.
-  Load alternative config file, I selected mine as /usr/src/config-2.6.27.9-vortex86dx, or if you downloaded the one from me, use config-2.6.29.3-vortex86dx  
-  Enable generic x86 support  
-  Enable Kernel .config support  
-  Device drivers -> Network -> 10 or 100Mbit -> RDC R6040, set at built in  
-  Turn off generic IDE support  
-  Exit, make sure to save the kernel  
-  Verify .config exists. If it doesn't, copy the config-2.6.x.x-vortex86dx file to .config  
  
5) Create the kernel debs. In the kernel directory, issue these commands. This will build the kernel image, the headers, and the modules.

```bash
make-kpkg --initrd kernel_image kernel_source kernel_headers modules_image

```  

6) Make coffee
7) Copy the debs to your running ebox by sftp (or usb, or whatever is available)
8) Install kernel in eBox-3300

```bash
dpkg -i linux-source-2.6.29.3-vortex86dx.deb
dpkg -i linux-headers-2.6.29.3-vortex86dx.deb
dpkg -i linux-image-2.6.29.3-vortex86dx.deb

```  
  

9) Reboot. If you want my compiled kernel/sources/header .DEBs, just shoot me an email and I'll make them available.

**Summary:** My only gripe about this little box was the lack of an easily customizable kernel, but no more. I'm still very happy with this $150 purchase.