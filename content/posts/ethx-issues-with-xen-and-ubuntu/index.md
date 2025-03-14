---
title: 'ethX Issues with Xen and Ubuntu'
date: 2008-04-20T20:30:00.002+10:00
draft: false
url: /2008/04/ethx-issues-with-xen-and-ubuntu_2003.html
tags: 
- articles
- virtualization
- xen
---

My new guest VMs under Xen seem to be having issues where upon each reboot, the network interface gets incremented by 1. For instance, it starts at eth0, then goes to eth1, then eth2, and eventually ethX. There are two issues to fix: 1) get the count back to 0, and 2) stop it from counting again.

I was able to get them to decrease by looking in the /etc/udev/rules.d/70-persistent-net.rules file and removing all entries.

Next, I was able to prevent this by simply inserting a MAC address to the interface in the configuration. For instance, one of my domU's has this entry:

```bash
vif         = [ 'mac=00:D0:59:83:DC:B5,bridge=xenbr0' ]

```  
  

Lastly, I made sure (as I would with any server) to create an entry in the /etc/network/interfaces file.

```bash
auto eth0
iface eth0 inet static
address 192.168.1.16
gateway 192.168.1.1
netmask 255.255.255.0

```  
  

Works like a charm.