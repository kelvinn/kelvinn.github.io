---
title: 'Database Woopsie'
date: 2008-02-13T21:30:00.002+11:00
draft: false
url: /2008/02/database-woopsie_863.html
tags: 
- database
- articles
---

I returned to my computer today to notice I had the following error:

```
(145, "Table './databasename/comments_freecomment' is marked as crashed and should be repaired")

```  
  

Well, crap. The solution is quite easy, however:

```
mysqlcheck -uUsername -pPassword databasename comments_freecomment

```  
  

Now you know what you already know, you can fix it:

```
mysqlcheck -r -uUsername -pPassword databasename comments_freecomment

```  
  

If that doesn't work, you can try a slightly different method. First, go to the location where your databases are stored on the disk (most likely something like /var/lib/mysql/databasename). Next, stop the database -- and try to free up as much memory as possible. Then run:

```
myisamchk -r comments_freecomment

```  
  

If that doesn't work, try to force it:

```
myisamchk -r comments_freecomment -f

```  
  

Hope that helps!