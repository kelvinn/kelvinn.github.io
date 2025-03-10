---
title: 'New Atheros Module and Ubuntu'
date: 2009-09-22T20:30:00.002+10:00
draft: false
url: /2009/09/new-atheros-module-and-ubuntu_1580.html
tags: 
- ubuntu
- linux
- kernel
- wireless
- howtos
---

I've been using Atheros for quite some time, and I've always liked the madwifi drivers. They allowed really easy switching into monitor mode, and decent levels of packet injection. However, since I'm mostly in an office now, instead of writing web apps in cafes and trying to score free internet, I don't really need anything fancy. My gentoo stage 1 (3?) days are over. I use Ubuntu, because I'm lazy, and it mostly works.

My new laptop (well, 1.5 year old laptop now, but still new in my eyes) gave me the option between an Intel card and a Atheros wifi card. I chose the Atheros card; then the ath5k module came out, and life has been turbulent ever since.

In summary: the ath5k driver in the 2.6.28 kernel, which is what Ubuntu 9.04 uses, isn't as up-to-date as the drivers in compat-wireless. _Fancy that..._ This presents me with the option of compiling a new kernel specifically with it, or just installing compat-wireless. I'm lazy, so...

I'll get a few basic troubleshooting commands out of the way first. After updating the kernel I kept getting disconnected - it appeared I was associate/disassociating frequently.

```
\# dmesg
...
2577.134060\] wlan0: associated
\[ 2580.984838\] wlan0: disassociating by local choice (reason=3)
...

```  
  
  
```
\# lspci | grep Atheros
03:00.0 Ethernet controller: Atheros Communications Inc. AR5212 802.11abg NIC (rev 01)

```  
  
  
```
\# ping 192.168.1.1
...
64 bytes from 192.168.1.1: icmp\_seq=2409 ttl=64 time=1.13 ms
64 bytes from 192.168.1.1: icmp\_seq=2410 ttl=64 time=2236.61 ms
64 bytes from 192.168.1.1: icmp\_seq=2411 ttl=64 time=4562.40 ms
64 bytes from 192.168.1.1: icmp\_seq=2412 ttl=64 time=6521.868 ms
...

```  
  

The steps to resolve are as follows:

*   1) Make sure you have headers for your current kernel.
*   2) Make sure you have ability to compile programs.
*   3) Download and install compat-wireless
*   4) Unload and load the module.

  
  

So, first, use Synapitc to get the latest kernel headers and the 'build-essential' packages.

Next, download the compat-wireless package. I needed to use one from a few weeks ago because I received the following error:

```
make -C /lib/modules/2.6.28-15-generic/build M=/usr/src/compat-wireless-2009-09-22 modules
make\[1\]: Entering directory \`/usr/src/linux-headers-2.6.28-15-generic'
CC \[M\]  /usr/src/compat-wireless-2009-09-22/drivers/net/wireless/b43/main.o
/usr/src/compat-wireless-2009-09-22/drivers/net/wireless/b43/main.c: In function 'b43\_do\_interrupt':
/usr/src/compat-wireless-2009-09-22/drivers/net/wireless/b43/main.c:1888: error: 'IRQ\_WAKE\_THREAD' undeclared (first use in this function)
/usr/src/compat-wireless-2009-09-22/drivers/net/wireless/b43/main.c:1888: error: (Each undeclared identifier is reported only once
/usr/src/compat-wireless-2009-09-22/drivers/net/wireless/b43/main.c:1888: error: for each function it appears in.)
/usr/src/compat-wireless-2009-09-22/drivers/net/wireless/b43/main.c: In function 'b43\_request\_firmware':
/usr/src/compat-wireless-2009-09-22/drivers/net/wireless/b43/main.c:2218: warning: format not a string literal and no format arguments
/usr/src/compat-wireless-2009-09-22/drivers/net/wireless/b43/main.c: In function 'b43\_wireless\_core\_start':
/usr/src/compat-wireless-2009-09-22/drivers/net/wireless/b43/main.c:3867: error: implicit declaration of function 'request\_threaded\_irq'
make\[4\]: \*\*\* \[/usr/src/compat-wireless-2009-09-22/drivers/net/wireless/b43/main.o\] Error 1
make\[3\]: \*\*\* \[/usr/src/compat-wireless-2009-09-22/drivers/net/wireless/b43\] Error 2
make\[2\]: \*\*\* \[/usr/src/compat-wireless-2009-09-22/drivers/net/wireless\] Error 2
make\[1\]: \*\*\* \[\_module\_/usr/src/compat-wireless-2009-09-22\] Error 2
make\[1\]: Leaving directory \`/usr/src/linux-headers-2.6.28-15-generic'
make: \*\*\* \[modules\] Error 2

```  
  

You can download a working 2009-09-05 set from [orbit-lab.org](http://www.orbit-lab.org/kernel/compat-wireless-2.6/2009/09/compat-wireless-2009-09-05.tar.bz2)

```
\# tar -xpjf compat-wireless-2009-09-05.tar.bz2
# cd compat-wireless-2009-09-05
# make
# make install
# make unload
# modprobe ath5k

```  
  

All done. My variable ping times and random disconnections seem to have been mitigated. Thanks wireless guys!