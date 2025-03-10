---
title: 'Quick n&#39; Dirty Firewall'
date: 2006-08-15T20:30:00.002+10:00
draft: false
url: /2006/08/quick-n-dirty-firewall_8747.html
tags: 
- howtos
---

#### Abstract

The following is a Quick n' Dirty method at implementing a very simple firewall.  

#### Locate IPTables

Depending on your server, first locate iptables:  
  
  
  
```
 \[root@vps /\]# which iptables 
```  
  

#### Create IP Based Accept/Deny

  
  
Create a whitelist (ignored by firewall) or blacklist (packet dropped) if you wish:  
  
  
  
```
 \[root@vps /\]# vi /usr/local/etc/whitelist.txt 
```  
  
  
And/Or...  
  
  
  
```
\[root@vps /\]# vi /usr/local/etc/blacklist.txt 
```  
  
  
In each file, add each IP per line, for instance:  
  
  
  
```
 4.2.2.2 66.35.15.20 
```  

#### firewall.sh Script

  
  
Then put the following in /etc/init.d/firewall.sh, and edit to fit your needs:  
  
  
```

#!/bin/sh
#
## Quick n Dirty Firewall
#
## List Locations
#

WHITELIST=/usr/local/etc/whitelist.txt
BLACKLIST=/usr/local/etc/blacklist.txt

#
## Specify ports you wish to use.
#

ALLOWED="22 25 53 80 443 465 587 993"

#
## Specify where IP Tables is located
#

IPTABLES=/sbin/iptables

#
## Clear current rules
#

$IPTABLES -F
echo 'Clearing Tables F'
$IPTABLES -X
echo 'Clearing Tables X'
$IPTABLES -Z
echo 'Clearing Tables Z'
echo 'Allowing Localhost'

#Allow localhost.
$IPTABLES -A INPUT -t filter -s 127.0.0.1 -j ACCEPT

#
## Whitelist
#

for x in \`grep -v ^# $WHITELIST | awk \\'{print $1}\\'\`; do
        echo "Permitting $x..."
        $IPTABLES -A INPUT -t filter -s $x -j ACCEPT
done

#
## Blacklist
#

for x in \`grep -v ^# $BLACKLIST | awk \\'{print $1}\\'\`; do
        echo "Denying $x..."
        $IPTABLES -A INPUT -t filter -s $x -j DROP
done

#
## Permitted Ports
#

for port in $ALLOWED; do
        echo "Accepting port TCP $port..."
        $IPTABLES -A INPUT -t filter -p tcp --dport $port -j ACCEPT
done

for port in $ALLOWED; do
        echo "Accepting port UDP $port..."
        $IPTABLES -A INPUT -t filter -p udp --dport $port -j ACCEPT
done

#
## Drop anything else
#

$IPTABLES -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
$IPTABLES -A INPUT -p udp -j DROP
$IPTABLES -A INPUT -p tcp --syn -j DROP


```  
  

#### Start Firewall

  
  
```
 \[root@vps /\]# chmod 700 /etc/init.d/firewall.sh
  \[root@vps /\]# /etc/init.d/firewall.sh 
```