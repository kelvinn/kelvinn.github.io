---
title: 'How to convert 131500 TDX to GTFS'
date: 2012-07-02T13:59:00.000+10:00
draft: false
url: /2012/07/how-to-convert-131500-tdx-to-gtfs.html
tags: 
- tdx
- howtos
- gtfs
---

TDX data has been available for a number of years on 131500.info, but many tools are GTFS specific. I also find GTFS easier to work with.  
  
Luckily, converting from TDX to GTFS is not overly difficult, and below are some instructions. This howto is a bit old, as I am only now copying it from my "Notes" folder to put online to help others.  
  
**Note:** You can now directly download GTFS from the TransportInfo website: [https://tdx.131500.com.au](https://tdx.131500.com.au/)  
  
1) Signup for an account with EC2 (AWS), unless you have 16GB of memory available on a machine.  
2) Upload [TransXChange2GTFS](http://code.google.com/p/googletransitdatafeed/) to a place you can download from.  
3) Upload the latest TDX data dump from 131500.info to a place you can download from.  
4) Login to AWS and start an EC2 instance.  I picked a large instance and used 64-bit Ubuntu 10.04, us-east-1 ami-f8f40591  
5) Download the Data and transxchange to /mnt  
  
```bash
wget http://ec2-175-41-139-176.ap-southeast-1.compute.amazonaws.com/Data20110127.zip
wget http://cdn.kelvinism.com/transxchange2GoogleTransit.jar

```  
6) Install Sun JRE.  

```bash
apt-get install python-software-properties
add-apt-repository "deb http://archive.canonical.com/ lucid partner"
apt-get update
apt-get install sun-java6-jre
```bash

7) Check how much memory is available  

```bash
root@domU-12-31-39-10-31-B1:/mnt# free -m
             total       used       free     shared    buffers     cached
Mem:          7680        626       7053          0         11        329
-/+ buffers/cache:        285       7394
Swap:            0          0          0


```  
8) Create a configuration file **sydney.conf**  
  
```plain
url=http://131500.info
timezone=Australia/Sydney
default-route-type=2
output-directory=output
useagencyshortname=true
skipemptyservice=true
skiporhpanstops=true

```  
9) If you're on the train like me, start screen, and start converting. The number you pick for "-Xmx" obviously needs to fit in the amount of free memory you have.  
  
```bash
java -Xmx104000m -jar dist\\transxchange2GoogleTransit.jar Data20120524.zip -c sydney.conf

```