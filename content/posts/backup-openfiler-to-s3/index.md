---
title: 'Backup OpenFiler to S3'
date: 2008-11-02T21:30:00.010+11:00
draft: false
url: /2008/11/backup-openfiler-to-s3_9140.html
tags: 
- howtos
- openfiler
---

Backing up your Openfiler box to S3  
  

While I don't think most pople would expect to backup their entire NAS/SAN to Amazon's S3, there might be a few very crucial things you need to backup. For instance, my girlfriend's PhD papers and data.

I've seen an implementation using Ruby and s3sync -- something that I do on my server -- but I'm trying to migrate everything to Python. Although there are a lot of great tools out there for S3, many of them Python-based, I wanted to do one thing and do it well: have one complete full backup available, and using as little bandwidth as possible. In these regards Duplicity would work well, except I wanted the ability to browse the S3 store using any other tool.

I've digged deeper into [s3cmd](http://s3tools.logix.cz/s3cmd), which I had noticed a long time ago, but I failed to notice it has a sync option. I have tested it out, and it appears to work very, very well. Here's how to use it with OF.

First, download [s3cmd](http://s3tools.logix.cz/download). You'll need to use subversion, so I first checked it out to my laptop, then uploaded it via SSH to OF. I put my s3cmd folder in /opt.

```
  
\[root@files opt\]# ls  
openfiler  s3cmd  
\[root@files opt\]#   

```  
  

If you don't have elementtree installed, now is a good time to install it.

```
  
conary update elementtree:python  

```  
  

We need to next configure s3cmd with our AWS creds.

```
  
\[root@files s3cmd\]# ./s3cmd --configure  

```  
  

In the end I didn't configure encryption for my files (so just hit enter), but you may choose to do so. I have configured the transfer to use HTTPS, however.

```
  
Save settings? \[y/N\] y  
Configuration saved to '/root/.s3cfg'  

```  
  

Cool. Now create a bucket on S3 for your NAS, e.g. blah2134accesskey.openfiler, using whatever method you choose (I typically use Cockpit). Now that you have a bucket, configure a \*really\* simple script to drop in cron:

```
  
#!/bin/bash  
  
/opt/s3cmd/s3cmd sync /mnt/openfiler/data/profiles/bunny s3://blah2134accesskey.openfiler/mnt/openfiler/data/profiles/bunny  
/opt/s3cmd/s3cmd sync /mnt/openfiler/data/profiles/kelvin-pc s3://blah2134accesskey.openfiler/mnt/openfiler/data/profiles/knicholson/kelvin-pc  

```  
  

Sweet! I like this approach quite a bit: I get file-level access to anything on the NAS, you don't have to actually install anything, and it 'just works.'