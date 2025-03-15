---
title: 'MySQL Compat'
date: 2006-11-15T21:30:00.002+11:00
draft: false
url: /2006/11/mysql-compat_1690.html
tags: 
- databases
- mysql
- articles
---

I've run into this error quite a few times, might as well toss blog entry about it:  
ERROR 1064 at line 17: You have an error in your SQL syntax near 'ENGINE=MyISAM DEFAULT CHARSET=latin1' at line 7  
One likely reason this comes about is because the data being imported/exported is not compatible with the database version. For instance, at home you export the information from a mysql5 database. Then you try to import it on a mysql3.23 database somewhere else -- and it fails on you. Bummer.  
The solution is quite simple:  
  
  
```bash
 mysqldump --compatible=mysql323 -u root -p database > exportName.sql
```