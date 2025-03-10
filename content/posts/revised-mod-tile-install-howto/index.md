---
title: 'Revised mod_tile Install HOWTO'
date: 2008-11-01T21:30:00.005+11:00
draft: false
url: /2008/11/revised-modtile-install-howto_1369.html
tags: 
- OSM
- apache
- howtos
---

This is the laundry list of things I did while creating a mod\_tile VMware appliance based on Ubuntu Server 8.04. I've kept descriptions limited but left all the commands in. Let's start installing things...

  
**Useful goodies for compiling source**  
  
```
sudo apt-get build-essential

```  

**More goodies for Mapnik + Friends**

```
sudo apt-get install libboost-dev libboost-filesystem-dev libboost-filesystem1.34.1 libboost-iostreams-dev libboost-iostreams1.34.1 libboost-program-options-dev libboost-program-options1.34.1 libboost-python-dev libboost-python1.34.1 libboost-regex-dev libboost-regex1.34.1 libboost-serialization-dev libboost-serialization1.34.1 libboost-thread-dev libboost-thread1.34.1 libicu-dev libicu38 libstdc++5 libstdc++5-3.3-dev python2.5-dev

```  
```
sudo aptitude install libfreetype6 libfreetype6-dev libjpeg62 libjpeg62-dev libltdl3 libltdl3-dev libpng12-0 libpng12-dev libtiff4 libtiff4-dev libtiffxx0c2 python-imaging python-imaging-dbg proj

```  
```
sudo aptitude install libcairo2 libcairo2-dev python-cairo python-cairo-dev libcairomm-1.0-1 libcairomm-1.0-dev libglib2.0-0 libpixman-1-0 libpixman-1-dev libpthread-stubs0 libpthread-stubs0-dev ttf-dejavu ttf-dejavu-core ttf-dejavu-extra

```  
```
sudo aptitude install libgdal-dev python2.5-gdal postgresql-8.3-postgis postgresql-8.3 postgresql-server-dev-8.3 postgresql-contrib-8.3

```  
```
sudo aptitude install libxslt1.1 libxslt1-dev libxml2-dev libxml2 gdal-bin libgeos-dev libbz2-dev

```  
```
sudo aptitude install apache2 apache2-threaded-dev apache2-mpm-prefork apache2-utils

```  
```
sudo aptitude install subversion

```  

This checks out the mapnik source:

```
svn co svn://svn.mapnik.org/trunk mapnik-src

```  

Let's build mapnik with several specific locations included.

```
cd mapnik-src
python scons/scons.py PYTHON=/usr/bin/python PGSQL\_INCLUDES=/usr/include/postgresql PGSQL\_LIBS=/usr/lib/postgresql BOOST\_INCLUDES=/usr/include/boost BOOST\_LIBS=/usr/lib

```  
```
sudo python scons/scons.py install PYTHON=/usr/bin/python PGSQL\_INCLUDES=/usr/include/postgresql PGSQL\_LIBS=/usr/lib/postgresql BOOST\_INCLUDES=/usr/include/boost BOOST\_LIBS=/usr/lib

```  

And prepare a few things for the mapnik rendering...

```
svn co http://svn.openstreetmap.org/applications/rendering/mapnik/

```  
```
cd ~/mapnik
wget http://tile.openstreetmap.org/world\_boundaries-spherical.tgz 
tar -xpjf world\_boundaries-spherical.tgz
unzip processed\_p.zip 
cp coastlines/\* world\_boundaries/ 
rmdir coastlines 

```  

Time to setup postgres. I have the intentions of running renderd (the mod\_tile rendering engine) under whatever user Apache is running as, so I'll setup postgres to allow the OSM user to authenticate via password. I'm not a postgres expert, so if you see me doing something totally foolish, let me know.

  
```
sudo vi /etc/postgresql/8.3/main/pg\_hba.conf

```  

And edit the authentication part as so:

```
\# Database administrative login by UNIX sockets
local   all         postgres                          ident sameuser
local   all         osm                               password sameuser

```  

And now to actually configure postgres for the OSM data

```
sudo su postgres
createuser osm
createdb -E UTF8 -O osm gis
createlang plpgsql gis
psql -d gis -f /usr/share/postgresql-8.3-postgis/lwpostgis.sql
echo "ALTER TABLE geometry\_columns OWNER TO osm; ALTER TABLE spatial\_ref\_sys OWNER TO osm;"  | psql -d gis
echo "alter user osm with password 'columbia';" | psql

```  
```
sudo /etc/init.d/postgresql-8.3 restart

```  

Now, let's render a sample image. Edit set-mapnik-env by changing the DB to 'gis', the username to 'osm', and the password to 'columbia'

```
cd mapnik
source ./set-mapnik-env
./customize-mapnik-map >osm.xml
./generate\_image.py

```  

If you get an error about it not finding a lib, make sure to do a...

```
sudo ldconfig

```  

You should have an image called 'image.png' in the mapnik directory, and it should look distinctly like the UK.

  
```
svn co http://svn.openstreetmap.org/applications/utils/export/osm2pgsql
cd osm2pgsql
make

```  

Ok, that was easy. Let's load some data. I've used a sample snippit from Sydney in /home/osm to illustrate this.

```
./osm2pgsql -W -d gis ../sydney.osm

```  

Type in the password used for postgres ('columbia')

  

I'll now check that the data is accessible by editing generate\_image.py with the correct coords for Sydney.

  
```
ll = (150.29, -34.04, 151.25, -33.36)

```  

Time to get mod\_tile up and running.

  
```
sudo apt-get install libagg-dev

```  
```
svn co http://svn.openstreetmap.org/applications/utils/mod\_tile
cd mod\_tile

```  

Depending on the revision of mod\_tile you are using, you are going to have to edit the source before compiling. The two files you need to read through are the Makefile and render\_config.h. I change the apxs and apachectl locations to the correct place (lines 2, 13 and 14). Since I did it on a x86 image, I took out any references to lib54 (line 33). In render\_config.h, I made the following changes:

  

Line 8

  
```
#define WWW\_ROOT "/var/www"

```  

Line 23

  
```
#define OSM\_XML "/home/osm/mapnik/osm.xml"

```  

Removed references to lib64 on lines 26 and 29.

  
```
make && make install

```  

Set it up as a module for apache by creating a file in /etc/apache/conf.d called 'mod\_tile' and putting in there:

  
```
LoadModule tile\_module /usr/lib/apache2/modules/mod\_tile.so

```  

Created a folder called 'osm\_tiles2' and 'direct' in /var/www, and make sure they are writable by whatever apache runs as (likely www-data). Restart apache.

From here, I created a file that automatically zooms in on the map I just created -- you can check it out here. Start the renderd process as www-data, and browse to the sample file.

```
cd ~/mod\_tile
sudo su www-data
./renderd

```  

By now you should have a working mod\_tile/OSM setup. After a change and tune a few things on the Ubuntu image I'll make the VMware image available for download. I can't wait to do some OSM projects!