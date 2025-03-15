---
title: 'Notes on Installing mod_tile for Mapnik'
date: 2008-04-22T20:30:00.002+10:00
draft: false
url: /2008/04/notes-on-installing-modtile-for-mapnik_168.html
tags: 
- howtos
---

I have no idea if these notes on how to install mod_tile will be useful for anybody. The current readme states that you need to edit the source code, but never actually where. Well, this is where, at least until the code can either take switches or can auto-configure itself. This is quite brief, so if you need more details, shoot me an email or leave a comment. I have repeated this process on two Ubuntu 7.10 machines.

1) Install mapnik as per normal -- you may also need to do a...

```bash
$ ./bootstrap
$ ./autogen.sh
$ ./configure
$ make
# make install

```  
  
2) Install libagg (apt-get install libagg-dev)
3) Make sure the mapnik library files are /usr/local/lib (libmapnik.*)
4) Make sure to copy/install fonts and input folders into /usr/local/lib/mapnik
5) Edit Makefile, change line 27 to where your include files are located

```c
RENDER_CPPFLAGS += -I/usr/local/include/mapnik

```  
  

6) Edit Makefile, change line 33 to where your mapnik libraries are (libmapnik.*)

```c
RENDER_LDFLAGS += -lmapnik -L/usr/local/lib

```  
  

7) Edit Line 40 of gen_tile.cpp to point to your osm.xml file (that you can verify works with generate_image.py)

```c
static const char *mapfile = "/home/kelvin/mapnik-osm/osm.xml";

```  
  

8) Edit line 219 of gen_tile.cpp to point to the correct location of the datasource input.

```c
datasource_cache::instance()->register_datasources("/usr/local/lib/mapnik/input");

```  
  

9) Edit line 221 of gen_tile.cpp to point to the correct location of your fonts directory.

```c
load_fonts("/usr/local/lib/mapnik/fonts", 0);

```  

10) The module will install in /usr/lib/apache2/modules, so mod_tile.conf should read:

```plain
LoadModule tile_module /usr/lib/apache2/modules/mod_tile.so

```  

**Final note:** I think it would be possible to just symlink the lib directory to lib64, although I would expect that could have some undesirable outcomes down the road. However, despite being pretty new code, how do I find mod_tile? Pretty good, actually. I expected more difficulties setting it up, but overall the procedure hasn't been too bad. I like the approach of creating a module vs. using several middle-layers. So once again, hats off to the OSM crew.