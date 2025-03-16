---
title: 'NetFlow into MySQL with flow-tools'
date: 2008-12-21T21:30:00.002+11:00
draft: false
url: /2008/12/netflow-into-mysql-with-flow-tools_5439.html
tags: 
- mysql
- monitoring
- cisco
- howtos
- netflow
---

I've been side-tracked on another little project, and keep coming back to NetFlow. For this project I'll need to access NetFlow data with [Django](http://www.djangoproject.com), but this is a bit tricky. First, I'm sort of lazy when it comes to my own project; maybe not lazy, I just like taking the most direct route. The most up-to-date NetFlow collector I noticed was [flow-tools](http://code.google.com/p/flow-tools/), and there is even a switch to export the information into MySQL. Sweet! However, I wanted to insert the flows into MySQL automatically, or at least on a regular basis. I first started writing a python script that would do the job, but after a few minutes noticed flow-capture had a rotate_program switch, and started investigating. Since I somehow couldn't find anywhere instructions how to insert the data automatically, here's what I came up with:

1) Download [flow-tools](http://code.google.com/p/flow-tools/); make sure to configure with --with-mysql (and you'll have to make sure you have the needed libraries).
2) Create a new database, I called mine 'netflow'.
3) Create a table that can contain all the netflow fields, a sample is below. I added a "flow_id" field that I used as a primary key, but you don't necessarily need this.

```sql
CREATE TABLE `flows` (
`FLOW_ID` int(32) NOT NULL AUTO_INCREMENT,
`UNIX_SECS` int(32) unsigned NOT NULL default '0',
`UNIX_NSECS` int(32) unsigned NOT NULL default '0',
`SYSUPTIME` int(20) NOT NULL,
`EXADDR` varchar(16) NOT NULL,
`DPKTS` int(32) unsigned NOT NULL default '0',
`DOCTETS` int(32) unsigned NOT NULL default '0',
`FIRST` int(32) unsigned NOT NULL default '0',
`LAST` int(32) unsigned NOT NULL default '0',
`ENGINE_TYPE` int(10) NOT NULL,
`ENGINE_ID` int(15) NOT NULL,
`SRCADDR` varchar(16) NOT NULL default '0',
`DSTADDR` varchar(16) NOT NULL default '0',
`NEXTHOP` varchar(16) NOT NULL default '0',
`INPUT` int(16) unsigned NOT NULL default '0',
`OUTPUT` int(16) unsigned NOT NULL default '0',
`SRCPORT` int(16) unsigned NOT NULL default '0',
`DSTPORT` int(16) unsigned NOT NULL default '0',
`PROT` int(8) unsigned NOT NULL default '0',
`TOS` int(2) NOT NULL,
`TCP_FLAGS` int(8) unsigned NOT NULL default '0',
`SRC_MASK` int(8) unsigned NOT NULL default '0',
`DST_MASK` int(8) unsigned NOT NULL default '0',
`SRC_AS` int(16) unsigned NOT NULL default '0',
`DST_AS` int(16) unsigned NOT NULL default '0',
PRIMARY KEY (FLOW_ID)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


```  
  
4) Setup your router so it sends netflow packets to your linux box (see README/INSTALL)
5) Create a "rotate program" that will actually enter in the information into mysql.

```bash
kelvin@monitor:/usr/bin$ cat flow-mysql-export 
#!/bin/bash

flow-export -f3 -u "username:password:localhost:3306:netflow:flows" < /flows/router/$1

```

6) Create the /flows/router directory
7) Start flow-capture (9801 is the port netflow traffic is being directed to); all done.

```bash
flow-capture -w /flows/router -E5G 0/0/9801 -R /usr/bin/flow-mysql-export

```