---
title: 'Fixing mysql warning message'
date: 2009-05-03T20:30:00.004+10:00
draft: false
url: /2009/05/fixing-mysql-warning-message_4782.html
tags: 
- mysql
- ubuntu
- articles
- tips
- debian
---

After restoring databases from one server to another I sometimes get this error on Ubuntu or Debian:

```bash
error: 'Access denied for user 'debian-sys-maint'@'localhost' (using password: YES)'

```  

This makes a lot of sense, and the solution is pretty simple. If you look in:

```bash
cat /etc/mysql/debian.cnf

```  

You'll see the defaults for your system. Copy the password listed there, and open a connection to MySQL as root (or some other user). Next, enter this (lets say your password specified in debian.cnf was 'abracadabra':

```bash
mysql> select PASSWORD('abracadabra');
+-------------------------------------------+
| PASSWORD('abracadabra')                   |
+-------------------------------------------+
| *38794E19D534EBA4F0F78903FA00F1DA2989DCA2 | 
+-------------------------------------------+
1 row in set (0.00 sec)


```  

Next, since we already have the prompt open, do this command:

```bash
mysql> USE mysql;
mysql> UPDATE user SET password='*38794E19D534EBA4F0F78903FA00F1DA2989DCA2' where user='debian-sys-maint';
mysql> FLUSH privileges;

```  

Restart MySQL, and the error should have gone away.