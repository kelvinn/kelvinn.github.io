---
title: 'Using Raw Disks with VMware Server 2'
date: 2008-08-11T20:30:00.002+10:00
draft: false
url: /2008/08/using-raw-disks-with-vmware-server-2_3562.html
tags: 
- vmware
- dirty
- disk
- howtos
---

For various reasons I had the need to open a raw disk inside VMware Server 2. The reports from the field say that this just isn't supported. Although I don't need to actually run a raw disk, I needed to get some data off it -- 400GB worth. It turns out 'not supported' really means 'not in the UI.' I don't know the reason why it isn't in the UI, maybe marketing wants people to use ESX, or maybe the UI guys fell behind with their workload.

Alas, it is possible. And here's how.

  
  
1) Take out your 'raw disk' and put it into another machine.  
  
2) Fire up Server 1.0.x or Workstation and open a virtual machine (or create a new one). Edit the preferences and add a new hard disk. Select 'use a physical disk', and select the disk you put in above. Select use entire disk. You may want to change the SCSI LUN to SCSI1:0 (depending how many disks are in your 'proper' server).  
  
3) Save it as something like 500GB.vmdk  
  
5) Copy out the relevant bit from the vmx file, e.g.  
  
```
\# Test VM.vmx
scsi1.present = "TRUE"
scsi1:0.present = "TRUE"
scsi1:0.fileName = "500GB.vmdk"
scsi1:0.deviceType = "rawDisk"

```  
  

And of course, the entire 500GB.vmdk file

```
\# 500GB.vmdk
# Disk DescriptorFile
version=1
CID=7e245252
parentCID=ffffffff
createType="fullDevice"

# Extent description
RW 976773168 FLAT "/dev/sdb" 0

# The Disk Data Base 
#DDB

ddb.virtualHWVersion = "6"
ddb.geometry.cylinders = "60801"
ddb.geometry.heads = "255"
ddb.geometry.sectors = "63"
ddb.geometry.biosCylinders = "60801"
ddb.geometry.biosHeads = "255"
ddb.geometry.biosSectors = "63"
ddb.adapterType = "buslogic"

```  

**Note**: If your guest OS is 64-bit, you won't be able to use buslogic. Switch the last entry above to 'lsilogic'.

While you could likely create the vmdk file by hand, the only number I'm not certain about is the part after the RW. (UPDATE: Note added to page). The Disk Data Base you can just see by typing in 'fdisk /dev/sdb'

  
  
4) Move the disk back to the 'server' and turn the server back on.  
  
5) Edit the vmx file of whatever virtual machine you want to use and put in the part copied from the vmx file of your other machine. Alternatively, if you did an upgrade, you could just copy it across now. Create a new 500GB.vmdk file in the same directory, paste in the bit you copied out from the test virtual machine. Double check that the 'raw disk' comes up as the same node in /dev.  
  
6) Boot up the virtual machine. You will notice in the WebUI that a new scsi controller is inserted. You should also noticed a new disk accessible inside your virtual machine, e.g.  
  
```
\[root@files dev\]# ls sd\*
sda  sda1  sda2  sda3  sdb  sdb1
\[root@files dev\]# ls /mnt
cdrom  floppy
\[root@files dev\]# mkdir /mnt/disk
\[root@files dev\]# mount /dev/sdb1 /mnt/disk
\[root@files dev\]# ls /mnt/disk
Files  lost+found  Movies  Music  Personal  VMWare
\[root@files dev\]#

```  
  

**Update**: Peter Jonsson kindly sent in the answer to "I don't know what to put after the RW." Below is the description of how to find the correct number. Thanks Peter!

```
The magic formula is:

ThePartAfterTheRW  =  TOTAL AMMOUNT OF DISKBYTES   /   512


This is my Western Digital 500 GB drive: 

fdisk -l

Disk /dev/sdc: 500.1 GB, 500107862016 bytes

256 heads, 63 sectors/track, 60563 cylinders

Units = cylinders of 16128 \* 512 = 8257536 bytes

Disk identifier: 0x00000000

And using the formula I got the "RW" stuff:

500107862016 / 512  = 976773168

```