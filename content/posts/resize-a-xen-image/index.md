---
title: 'Resize a Xen Image'
date: 2006-11-08T21:30:00.004+11:00
draft: false
url: /2006/11/resize-xen-image_3704.html
tags: 
- howtos
---

So, you've got a few Xen images around, and they are starting to fill up. How do you add a few more gigs to 'em?

```
 root@tpe:/# xm shutdown vm01  
 root@tpe:/# cd /xenimages  
 root@tpe:/xenimages# dd if=/dev/zero bs=1024 count=1000000 >> vm01.img  
 root@tpe:/path/to/images# resize2fs -f vm01.img  
 
```That's it, you just added a gig to your image called 'vm01.img'.