---
title: 'Migrating large disks into ESXi'
date: 2008-12-07T21:30:00.009+11:00
draft: false
url: /2008/12/migrating-large-disks-into-esxi_4692.html
tags: 
- vmware
- ESXi
- articles
---

I recently had the need to move a rather large (450GB) VMDK file from an external hard drive into ESXi. Since ESXi doesn't support external hard drives, this makes things quite a bit more difficult. At first I tried using SCP to copy the file over (after enabling SSH access for ESXi). However, when I tried to do this the time left was almost 20 hours -- a tad too long!

I rethought my idea and decided to use this process:

  
1) Create an NFS share on my laptop, using the external hard drive (with the VMDK) as a mount point.  
2) Use vmkfstools to move the image over.  
3) Update any bugs I encountered.  
  
  

Creating the NFS share on Linux is extermily easy. After install nfs via whatever package management tool you choose, put this entry into your /etc/exports file:  

```bash
  
/media/disk-1 192.168.1.0/24(ro,no_root_squash,async)  

```  

This assumes your USB disk is mounted as /media/disk-1, and your local subnet is 192.168.1.0/24. In OpenFiler, add a new storage with type NFS and use your laptops IP as the hose, and /media/disk-1 as the mount point. For safey, tick read-only.

Next, unlock SSH if you haven't already. Once you are in, browse to /vmfs/volumes and you can see your nfs share and your other datastores. Let's say you USB virtual disk is located at /vmfs/volumes/nfs/bigdisk.vmdk, and you want to import it into your normal datastore, under a folder called 'NAS'. Using vmware specific tools, you can import the file as so:

```bash
  
# vmkfstools -i /vmfs/volumes/nfs/bigdisk.vmdk /vmfs/volumes/datastore1/NAS/bigdisk.vmdk  

```  

I needed to update the hardware version of my imported disk. To do this, open up the .vmdk file (you should also have a -flat.vmdk file), and update the virtualHWVersion entry from 7 to 4. With that, join your disk to an image, and you should be good to go.

An addition result I noticed was the speed at which it came over. By using SCP, the entire file was going to take 20hr. By using NFS and vmkfstools, the files was migrated in under 10 hours.