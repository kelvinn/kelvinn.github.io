---
title: 'Ubuntu 10.04, Django and GAE - Part 2'
date: 2010-06-12T20:30:00.005+10:00
draft: false
url: /2010/06/ubuntu-1004-django-and-gae-part-2_6130.html
tags: 
- ubuntu
- django
- gae
- python
- howtos
---

All my Django sites are running 1.2, which poses a conflict with writing apps for Google's App Engine, as use\_library currently only supports < Django 1.1. There are two solutions that I found: a) use virtualenv, or b) chroot, which [I've already detailed](http://www.kelvinism.com/howtos/ubuntu-1004-django-and-gae-part-1/). This document will hopefully show you how to create a virtual environment to use a secondary django version, especially for GAE. Of the two options, I think this one is a bit quicker, but there will likely be tradeoffs that a chroot environment can deal with better, e.g. python imaging (I don't use it for GAE).  
First, install PIP and virtualenv:  

```bash
kelvinn@kelvinn-laptop:~/workspace$ sudo easy_install -U pip
kelvinn@kelvinn-laptop:~/workspace$ sudo pip install -U virtualenv

```  
  
Second, configure an environment for any app that will use Django 1.1:  

```bash
kelvinn@kelvinn-laptop:~/workspace$ virtualenv --python=python2.5 --no-site-packages django-1.1
New python executable in django-1.1/bin/python
Installing setuptools............done.
kelvinn@kelvinn-laptop:~/workspace$ pip install -E django-1.1 yolk
kelvinn@kelvinn-laptop:~/workspace$ pip install -E django-1.1 Django==1.1
```  
  
Now, download the [python GAE sdk](http://code.google.com/appengine/downloads.html#Google_App_Engine_SDK_for_Python) and put it in the django-1.1 folder. I also just dump any project directory requiring Django 1.1 into this django-1.1 folder, although I guess you could create a virtualenv for each project. The last thing to do is start the virtual environment, and run the GAE app.  

```bash
kelvinn@kelvinn-laptop:~/workspace$ source django-1.1/bin/activate
(django-1.1)kelvinn@kelvinn-laptop:~/workspace$ yolk -l
(django-1.1)kelvinn@kelvinn-laptop:~/workspace$ cd django-1.1
(django-1.1)kelvinn@kelvinn-laptop:~/workspace/django-1.1$ ls
bin  google_appengine  include  lib  myproject1 myproject2
(django-1.1)kelvinn@kelvinn-laptop:~/workspace/django-1.1$ google_appengine/dev_appserver.py myproject1
```  
  
When you're all finished, you can jump out of virtualenv:  

```bash
(django-1.1)kelvinn@kelvinn-laptop:~/workspace/django-1.1$ deactivate
```  
  
**Update**: You'll find this article especially interesting if you get an error such as the following:  

```bash
UnacceptableVersionError: django 1.1 was requested, but 1.2.0.beta.1 is already in use
```