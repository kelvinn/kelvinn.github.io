---
title: 'Enable ICMP through UFW'
date: 2010-09-21T20:30:00.002+10:00
draft: false
url: /2010/09/enable-icmp-through-ufw_461.html
tags: 
- firewall
- ubuntu
- ufw
- howtos
---

I like using Ubuntu's UFW command, but today I needed to allow outgoing ICMP. I received results as so:

```bash
$ ping 4.2.2.2  
PING 4.2.2.2 (4.2.2.2) 56(84) bytes of data.  
ping: sendmsg: Operation not permitted  
ping: sendmsg: Operation not permitted  
ping: sendmsg: Operation not permitted  

```  
  
  
  
  

To allow outbound icmp I edited 'before.rules' and added the following lines.

```bash
$ sudo vi /etc/ufw/before.rules
```  
  
  
```bash
# allow outbound icmp
-A ufw-before-output -p icmp -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
-A ufw-before-output -p icmp -m state --state ESTABLISHED,RELATED -j ACCEPT

```