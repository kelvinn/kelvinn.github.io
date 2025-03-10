---
title: 'Using Django with SQL Server and IIS'
date: 2008-11-08T21:30:00.002+11:00
draft: false
url: /2008/11/using-django-with-sql-server-and-iis_4115.html
tags: 
- django
- windows
- python
- howtos
- iis
---

As you can tell from reading some of the other pages, I like Linux and open source. But I also like to answer the question "what if..." This post is my \[brief\] run down of answering "what if I could run Django on Server 2003 with SQL Server and IIS." Why, you may ask? To be honest with you, at this point, I don't really know. One of the deciding factors was seeing that the django-mssql project maintains support for inspectdb, which means I could take a stock 2003 server running SQL Server, inspect the DB, and build a web app on top of it. The Django docs offer a lengthy [howto](http://code.djangoproject.com/wiki/DjangoOnWindowsWithIISAndSQLServer) for using Django with IIS and SQL Server, but the website for PyISAPIe seems to have been down for the last month or so. Without further delay, below are my notes on installing Django with SQL Server and IIS.

  
  
1a) Install python-2.x.x.msi from python.org  
  
1b) Consider adding C:\\Python25\\ to your Path (right click My Computer, Advanced, Environment Variables. Enter in blahblahblah;C:\\Python25\\)  
  
2) Download a 1.0+ branch of Django (and 7-zip if you need it)  
  
3a) Extract the contents of the Django. From inside Django-1.0, execute:  
  
```
C:\\Python25\\python.exe setup.py install

```  
3b) Consider adding C:\\Python25\\Script to your path.  
  
4) Look in C:\\Python25\\Lib\\site-packages -- confirm there is a Django package.  
  
5) Checkout django-mssql (http://code.google.com/p/django-mssql/), copy sqlserver\_ado from inside source to the site-packages directory  
  
6) Download and install PyWin32 from sf.net  
  
7) Start a test project in C:\\Inetpub\\ called 'test'  
  
```
c:\\Python25\\scripts\\django-admin.py startproject test

```  
8a) Create a database using SQL Management Studio, create a user. (First, go to the Security dropdown. Right click Logins, add a new user. Next, right click Databases, New Database. Enter in the name, and change the owner to the user you just created).  
  
8b) Edit the settings.py and add 'sqlserver\_ado' and add database credentials. Use the below example if your database comes up in the Studio as COMPUTERNAME\\SQLEXPRESS (you are using SQLExpress).  
  
```
import os
DATABASE\_ENGINE = 'sqlserver\_ado'           # 'postgresql\_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE\_NAME = 'crmtest'             # Or path to database file if using sqlite3.
DATABASE\_USER = 'crmtest'             # Not used with sqlite3.
DATABASE\_PASSWORD = 'password'         # Not used with sqlite3.
DATABASE\_MSSQL\_REGEX = True
DATABASE\_HOST =  os.environ\['COMPUTERNAME'\] + r'\\SQLEXPRESS' # I use SQLEXPRESS
DATABASE\_PORT = ''             # Set to empty string for default. Not used with sqlite3.

```  
9) Install/download FLUP: http://www.saddi.com/software/flup/dist/flup-1.0.1.tar.gz  
  
```
python setup.py install

```  
10a) Download pyisapi-scgi from http://code.google.com/p/pyisapi-scgi/  
  
10b) Extract the files to somewhere you can remember on your computer, like, c:\\scgi  
  
11) Double click pyisapi\_scgi.py  
  
12a) Follow the directions here: http://code.google.com/p/pyisapi-scgi/wiki/howtoen -- I set a temporary different port since I'm just testing this out.  
  
12b) The last few parts might be better served with an image or two:  
  

#### Using an app pool to get the right permissions

  
(No resource/photo)  
  
  

#### The SCGI configuration file

  
(No resource/photo)  
  
  

#### Properties of the web site

  
(No resource/photo)  
13) Start the scgi process from the Django folder directory  
  
```
python manage.py runfcgi method=threaded protocol=scgi port=3033 host=127.0.0.1

```  
14) Test your django page, http://192.168.12.34:8080  
  
  
  
(No resource/photo)