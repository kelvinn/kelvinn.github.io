---
title: 'Speeding Up VMWare Server'
date: 2008-12-07T21:30:00.008+11:00
draft: false
url: /2008/12/speeding-up-vmware-server_791.html
tags: 
- vmware
- articles
- performance
- tips and tricks
---

I found VMWare Server to have very slow I/O, and sought to improve it. Below are a list of tests I performed, the change, and the results.

```bash
  
  
### Host OS ###  
/dev/sdb1:  
 Timing buffered disk reads:  220 MB in  3.05 seconds =  72.17 MB/sec  
kelvin@gorilla:~$ sudo hdparm -t /dev/sdb1  
  
/dev/sdb1:  
 Timing buffered disk reads:  266 MB in  3.01 seconds =  88.33 MB/sec  
kelvin@gorilla:~$ sudo hdparm -t /dev/sdb1  
  
/dev/sdb1:  
 Timing buffered disk reads:  310 MB in  3.01 seconds = 102.99 MB/sec  
  
  
### Before Changes ###  
  
/dev/mapper/openfiler-data:  
 Timing buffered disk reads:    8 MB in  3.36 seconds =   2.38 MB/sec  
[root@files etc]# hdparm -t /dev/mapper/openfiler-data  
  
/dev/mapper/openfiler-data:  
 Timing buffered disk reads:   24 MB in  3.63 seconds =   6.61 MB/sec  
[root@files etc]# hdparm -t /dev/mapper/openfiler-data  
  
/dev/mapper/openfiler-data:  
 Timing buffered disk reads:   28 MB in  4.54 seconds =   6.16 MB/sec  
  

```  
  

I made several changes, but the changes that seemed to have the most impact are below:

```bash  
vm.dirty_background_ratio = 5  
vm.dirty_ratio = 10  
vm.swappiness = 0  
  

```  

Pop this into the virtual machine's .vmx file, reboot, and off you go. One unfortunate side effect is that you can no longer overload the memory (e.g. allocate more memory with the VMs than you actually have available).

```bash
  
  
### After Changes ###  
  
/dev/mapper/openfiler-data:  
 Timing buffered disk reads:   52 MB in  3.13 seconds =  16.61 MB/sec  
[root@files ~]# hdparm -t /dev/mapper/openfiler-data  
  
/dev/mapper/openfiler-data:  
 Timing buffered disk reads:   82 MB in  3.31 seconds =  24.75 MB/sec  
[root@files ~]# hdparm -t /dev/mapper/openfiler-data  
  
/dev/mapper/openfiler-data:  
 Timing buffered disk reads:  118 MB in  3.19 seconds =  36.97 MB/sec  
[root@files ~]# hdparm -t /dev/mapper/openfiler-data  
  
/dev/mapper/openfiler-data:  
 Timing buffered disk reads:  144 MB in  3.32 seconds =  43.37 MB/sec  
  
[root@files ~]# hdparm -t /dev/mapper/openfiler-data  
  
/dev/mapper/openfiler-data:  
 Timing buffered disk reads:  160 MB in  3.10 seconds =  51.57 MB/sec  

```  
  

**UPDATE**: Those wanting all the speed and still want to use memory overloading, I'd suggested you give ESXi a try. So far, so good.

```bash
  
## With ESXi, same hardware ##  
[root@files ~]# hdparm -t /dev/mapper/openfiler-data   
  
/dev/mapper/openfiler-data:  
 Timing buffered disk reads:  200 MB in  3.18 seconds =  62.92 MB/sec  

```