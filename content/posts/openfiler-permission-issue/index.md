---
title: 'OpenFiler Permission Issue'
date: 2008-12-07T21:30:00.010+11:00
draft: false
url: /2008/12/openfiler-permission-issue_2907.html
tags: 
- articles
- openfiler
---

I've had issues before with OpenFiler where doesn't update the permissions, although they appear correct in the UI. To rectify that, I stumbled upon a one liner that fixed it. Let's say you have a group called "Trusted" that you want to have full access to your music folder. Here's the one-liner:

```
\[root@files data\]# pwd
/mnt/openfiler/data
root@files data\]# setfacl --recursive -m u:nobody:rwx,g:Trusted:rwx music

```