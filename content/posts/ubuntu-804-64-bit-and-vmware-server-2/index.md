---
title: 'Ubuntu 8.04 64-Bit and VMware Server 2'
date: 2008-08-01T20:30:00.004+10:00
draft: false
url: /2008/08/ubuntu-804-64-bit-and-vmware-server-2_1451.html
tags: 
- esxi
- ubuntu
- vmware
- howtos
---

I now have successful installation of VMware Server 2 (Beta RC1) on top of Ubuntu 8.04 64-bit. I have been using various virtualization technologies for years, and VMware is usually the easiest to install and configure. So far, VMware Server 2 RC1, has proven to be the exception to the rule.

That said, I am very excited by the direction VMware is taking -- this new server version looks to have great potential.

  
  

The 'server' this is on is a mATX motherboard from Gigabyte (GA-G33M-DS2R), with 4GB (2x2GB) of Transcend DDR2-800 memory, topped off with the E8200. I have been nothing but impressed with this combination of hardware.

However, although I was thinking VMware Server 2 would install seamlessly over Ubuntu, I was wrong. There were a few things I had to tweak to get everything working correctly.

The first thing I had major issues with was VMware choking on the parallel port. Normally the parport is the first thing I would turn off, but in this instance, I guess excitement overtook me. My tip is to first remove the lp module from inside /etc/modules, and then disable the parallel port inside the BIOS. The symptoms I was having involved VMware halting/freezing on either startup or shutdown. This occurred for both RC1 as well as 1.0.6.

My second tip, if VMware freezes half way through starting up or shutting down, is to go through the vmware startup script, /etc/init.d/vmware, and comment out anything refering to the parport_pc. In particular, I looked for this line and made sure to comment it out:

```bash
/sbin/modprobe -r parport_pc >/dev/null 2>&1

```  
  

I commented out lines 974 and 1076. After doing this, VMware loaded perfectly.

The second major issue I had occurred after actually installing VMware. I opened Firefox and went to the IP of my virtual server, logged in just fine, and loaded up my first virtual machine. However, after booting the virtual machine, I was unable to open up the remote console. It turns out I had just upgraded to Firefox 3.0.1, and the Remote Console is set to fail on anything above 3.0.0.1. The fix is quite easy.

First click where it says "click anywhere to open the virtual machine". Copy the address of the XPI and use something like wget to download the file. This is an example:

```bash
wget --no-check-certificate https://192.168.50.10/ui/plugin/vmware-vmrc-linux-x86.xpi

```  
  

If you are using Gnome, right click the file you just downloaded and say Open With then Archive Manager. Do the same for the 'install.rdf' file inside, specifying gedit as the application if need be. Next, edit line 20 so it reads as follows:

```plain
3.0.*

```  
  

Save the file, open the XPI with Firefox, and you should be good to go.

I've seen a lot of other suggestions on the 'net on how to fix VMware RC1 when booting -- including disabling ipv6, checking the hosts file, and running the any-any patches. None of these approaches helped me at all, but maybe it is exactly what you need. My biggest tip is that if VMware isn't starting up or stopping correctly, open up /etc/init.d/vmware and find out exactly where it is faulting (add things like 'echo "fail"' inside the IF statements).