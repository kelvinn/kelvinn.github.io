---
title: 'Upgrading Cisco Wireless Firmware'
date: 2008-11-03T21:30:00.002+11:00
draft: false
url: /2008/11/upgrading-cisco-wireless-firmware_3066.html
tags: 
- tftp
- articles
- wireless
- cisco
---

I'm always forgetting the exact string to enter at the CLI for updating the IOS on a wireless Cisco AP, so I'll just put it here to end my future searches:

```
Chimp# archive download-sw /force-reload /overwrite tftp://192.168.83.150/c1100-k9w7-tar.123-8.JEC1.tar

```  
  

192.168.83.150 obviously being your tftp server, and the .tar file sitting in the root of the tftp server.

I suppose if you wanted to backup your IOS you could do something along the lines of:

```
Chimp# archive upload-sw tftp://192.168.83.150/someimage.tar

```  

But I haven't tried it...