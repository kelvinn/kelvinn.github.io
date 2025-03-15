---
title: 'Installing Mapnik on Ubuntu 7.10'
date: 2008-04-19T20:30:00.002+10:00
draft: false
url: /2008/04/installing-mapnik-on-ubuntu-710_6688.html
tags: 
- postgis
- articles
- python
- mapnik
---

I have managed to install mapnik 0.4, 0.5, 0.5.1 and various SVN releases in-between on Ubuntu. While this isn't in itself exciting, I think I manage to stumble at every installation. I typically forget to add the flags when building, so, to prevent myself from stumbling again, I'm going to write them out here.

**Build mapnik**  
  
```
$ python scons/scons.py PYTHON=/usr/bin/python \\ 

PGSQL_INCLUDES=/usr/include/postgresql \\

PGSQL_LIBS=/usr/lib/postgresql BOOST_INCLUDES=/usr/include/boost BOOST_LIBS=/usr/lib

```  
  
  
  
  
**Then install it**  
```
$ sudo python scons/scons.py install PYTHON=/usr/bin/python \\ 

PGSQL_INCLUDES=/usr/include/postgresql \\

PGSQL_LIBS=/usr/lib/postgresql BOOST_INCLUDES=/usr/include/boost BOOST_LIBS=/usr/lib

```  
  

Then proceed as normal.