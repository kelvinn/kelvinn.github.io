---
title: 'Converting GTFS to GraphServer'
date: 2011-06-06T14:07:00.000+10:00
draft: false
url: /2011/06/converting-gtfs-to-graphserver.html
tags: 
- howtos
- gtfs
---

If you want to use Graphserver to do some analysis with GTFS, you will need to convert GTFS into the database. This is how I did it.  

#### Get an appropriate AMI from Amazon's EC2

I used the following AMI. If you have enough memory, you don't need to do this.  
  
```plain
ami-7000f019

```  
Lookup and read the GTFSDB [INSTALL.txt](http://code.google.com/p/gtfsdb/downloads/detail?name=GTFSDB%20INSTALL.txt) document  

#### Prepare system

```bash
sudo apt-get install mercurial
hg clone https://gtfsdb.googlecode.com/hg/ gtfsdb
sudo apt-get install python-setuptools
sudo easy_install psycopg2
sudo apt-get install build-essential
```

#### Download GTFS database

```bash
ubuntu@domU-12-31-39-00-5D-B8:/mnt/gtfsdb$ pwd
/mnt/gtfsdb
sudo python setup.py install
sudo wget http://cdn.kelvinism.com/google_transit.zip
sudo apt-get install python-psycopg2
```




#### Prepare configuration file

```plain
#default.cfg
[options]
create = True
database = postgresql://nsw:131500@10.128.49.175:5432/nsw
filename = /mnt/google_transit.zip
geospatial = True
#schema = None
```

#### Perform import

```bash
screen
python gtfsdb/scripts/load.py

```