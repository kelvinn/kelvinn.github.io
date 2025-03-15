---
title: 'Linux as a TFTP Server'
date: 2006-01-16T21:30:00.002+11:00
draft: false
url: /2006/01/linux-as-tftp-server_570.html
tags: 
- howtos
---

So, you need a TFTP server for something? Cool, you must be doing something fun. I need a TFTP server to copy Cisco IOS images onto the routers; hopefully you are doing something cooler.  
1) Enable TFTP in inetd.conf  
Open up /etc/inetd.conf and look for the following line:  
```bash
kelvin@pluto:~$ vi /etc/inetd.conf

#tftp  dgram   udp     wait    root    /usr/sbin/in.tftpd  in.tftpd -s /tftpboot -r blksize
```
This is on line 72 for me (hint: in vi press ctrl+c, then :set number). Uncomment it. If you don't have this line, bummer. Search for in.tftpd and use that as a substitute.  
  
```bash
kelvin@pluto:~$ which in.tftpd
/usr/sbin/in.tftpd
kelvin@pluto:~$
```  
2) Create the TFTP directory  
As you can see, we need the directory tftpbood. Create it.  
  
```bash
 kelvin@pluto:~$ sudo mkdir /tftpboot 
```  
3) Restart inetd  
  
```bash
kelvin@pluto:~$ sudo kill -1 [inetd pid]
```  
You can get the inetd pid by typing:  
```bash
kelvin@pluto:~$ ps -aux | grep inetd 
```
Cheers.  
  
**Edit**: A colleague in New Zealand was searching for something and stumbled upon this page. I gave him the tip that if you need to find the tftp server (or any service), you can do it based on port:  
```bash
lsof -i :69
```