---
title: 'Ubuntu 10.04, Django and GAE - Part 1'
date: 2010-06-12T20:30:00.004+10:00
draft: false
url: /2010/06/ubuntu-1004-django-and-gae-part-1_8750.html
tags: 
- ubuntu
- django
- gae
- python
- howtos
---

I've started to get into Google's App Engine again, and have started developing a simple product that I had a use for. The initial first draft was a quick 200 lines in webapp, and it worked great. However, I'm starting to find certain things quite cumbersome. I'm a huge fan of Django, and but also about keeping things as simple as possible, which is why I picked webapp to begin with.  
I'm now considering making a swap to Django, but there are some development issues; namely, I'm using Ubuntu 10.04, Python 2.6, and Django 1.2. This setup presents several setbacks, as GAE has the requirement of Django 1.1 and Python 2.5. There are two solutions that I found: a) use virtualenv, which [I've detailed](http://www.blogger.com/blogger.g?blogID=3439832858234004835#), or b) chroot. This document will hopefully show how to configure a chroot environment of Ubuntu 9.10 and prepare it for Django on GAE. Using a jailed environment should allow you to edit your code with your normal IDE and VCS, but use Django 1.1 and Python 2.5.  
First, I installed schroot and debootstrap.  

```bash
$ sudo apt-get install schroot debootstrap
```  
  
Second, I edited /etc/schroot/schroot.conf and added the following section to the end.  

```bash
[karmic]
description=karmic
type=directory
location=/var/chroot/karmic
priority=3
users=kelvinn #your username goes here
groups=admin
root-groups=root
run-setup-scripts=true
run-exec-scripts=true

```  
  
Third, I created the directories needed for the jailed environment and installed karmic.  

```bash
$ sudo mkdir -p /var/chroot/karmic
$ sudo debootstrap --arch i386 karmic /var/chroot/karmic
```  
  
Forth, I logged into the jailed environment and updated packages, installed Python 2.5 / Django 1.1. Make sure to note that I don't call 'python', I call 'python2.5'.  

```bash
$ sudo schroot -c karmic
(karmic)root@kelvinn-laptop:~# apt-get update
(karmic)root@kelvinn-laptop:~# apt-get install python2.5
(karmic)root@kelvinn-laptop:~# cd /usr/src
(karmic)root@kelvinn-laptop:~# apt-get install wget
(karmic)root@kelvinn-laptop:/usr/src# wget http://www.djangoproject.com/download/1.1.2/tarball/
(karmic)root@kelvinn-laptop:/usr/src# tar -xpzf Django-1.1.2.tar.gz
(karmic)root@kelvinn-laptop:/usr/src/Django-1.1.2# python2.5 setup install
(karmic)root@kelvinn-laptop:/usr/src/Django-1.1.2# exit
```  
  
Lastly, I log in as my normal user, and start the app. Let's say I have a folder called '~/gaeapps' for my GAE stuff, and that's where I put the SDK.  

```bash
$ scroot -c karmic
(karmic)kelvinn@kelvinn-laptop:~/gaeapps$ ls
google_appengine  myproject
(karmic)kelvinn@kelvinn-laptop:~/gaeapps$ google_appengine/dev_appserver.py myproject
```