---
title: 'Integrating OSSEC with Cisco IOS'
date: 2008-11-15T21:30:00.002+11:00
draft: false
url: /2008/11/integrating-ossec-with-cisco-ios_7061.html
tags: 
- mysql
- articles
- IDS
- ossec
- python
- xml
- hacking
---

I rank OSSEC as one of my favorite pieces of open source software, and finally decided to play around with it more in my own free time. (Yup, I do this sort of stuff for _fun_). My goal was quite simple: send syslog packets from my Cisco to my "proxy" server, running OSSEC. I found that, although OSSEC supports Cisco IOS logging, it didn't really work. In fact, I couldn't find any examples or articles of anybody actually getting it to work.

I initially tried to get it to work "correctly," and soon settled to "just getting it to work." I implemented some rules in the local_rules.xml file, which worked, but I'm pretty stubborn, and wanted to do it "correctly." With a couple pots of tea, and the support of my girlfriend, I became much, much more familiar with OSSEC. The key (and a lot of credit) goes to Jeremy Melanson for [hinting at some of the updates](http://www.ossec.net/ossec-list/2007-September/msg00124.html) to the decoder.xml file that need to take place.

The first step is to read the OSSEC + Cisco IOS [wiki page](http://www.ossec.net/wiki/index.php/PIX_and_IOS_Syslog_Config_examples#Configuring_Cisco_IOS_router). Everything on that page is pretty straight forward. I then added three explicit drop rules at the end of my Cisco's ACL:

```plain
...

access-list 101 deny tcp any host 220.244.xxx.xxx log
access-list 101 deny ip any host 220.244.xxx.xxx log
access-list 101 deny udp any host 220.244.xxx.xxx log

```  
  

(220.244.xxx.xxx is my WAN IP, and I'm sure you could figure out xxx.xxx pretty darn easily, but I'll x them out anyways).

To reiterate, OSSEC needs to be told to listen for syslog traffic, which you should be set on the Cisco. If you haven't done this, go re-read the wiki above.



```xml
<remote>
<connection>syslog</connection>
<allowed-ips>192.168.0.1</allowed-ips>
</remote>


```  
  

On or around line 1550 in /var/ossec/etc/decoder.xml I needed to update the regex that was used to detect the syslog stream.

```xml
...

<decoder name="cisco-ios">
<!--<prematch>^%\w+-\d-\w+: </prematch>-->
<prematch>^%\w+-\d-\w+: |^: %\w+-\d-\w+:</prematch>
</decoder>
 
<decoder name="cisco-ios">
<program_name>
<!--<prematch>^%\w+-\d-\w+: </prematch>-->
<prematch>^%\w+-\d-\w+: |^: %\w+-\d-\w+: </prematch>
</program_name></decoder>
 
<decoder name="cisco-ios-acl">
<parent>cisco-ios</parent>
<type>firewall</type>
<prematch>^%SEC-6-IPACCESSLOGP: |^: %SEC-6-IPACCESSLOGP: </prematch>
<regex offset="after_prematch">^list \d+ (\w+) (\w+) </regex>
<regex>(\S+)\((\d+)\) -> (\S+)\((\d+)\),</regex>
<order>action, protocol, srcip, srcport, dstip, dstport</order>
</decoder>


...

```  
  

In the general OSSEC configuration file, re-order the list of rules. I had to do this because syslog_rules.xml includes a search for "denied", and that triggers an alarm.

```xml
...
<include>telnetd_rules.xml</include>
<include>cisco-ios_rules.xml</include>
<include>syslog_rules.xml</include>
<include>arpwatch_rules.xml</include>
...


```  
  

Remember that these dropped events will go into /var/ossec/logs/firewall/firewall.log. Because this is my home connection, and I don't have any active_responses configured (yet!), I tightened the firewall_rules.xml file (lowering the frequency, raising the timeframe).

And in the end, I get a pretty email when somebody tries to port scan me.

#### Pretty email

  
  
```plain
OSSEC HIDS Notification.
2008 Nov 15 23:19:36
 
Received From: proxy->xxx.xxx.xxx.xxx
Rule: 4151 fired (level 10) -> "Multiple Firewall drop events from same source."
Portion of the log(s):
 
: %SEC-6-IPACCESSLOGP: list 101 denied tcp 4.79.142.206(36183) -> 220.244.xxx.xxx(244), 1 packet
: %SEC-6-IPACCESSLOGP: list 101 denied tcp 4.79.142.206(36183) -> 220.244.xxx.xxx(253), 1 packet
: %SEC-6-IPACCESSLOGP: list 101 denied tcp 4.79.142.206(36183) -> 220.244.xxx.xxx(243), 1 packet
: %SEC-6-IPACCESSLOGP: list 101 denied tcp 4.79.142.206(36183) -> 220.244.xxx.xxx(254), 1 packet
 
 
 
--END OF NOTIFICATION



```