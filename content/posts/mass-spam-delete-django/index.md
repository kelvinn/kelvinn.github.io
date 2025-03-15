---
title: 'Mass Spam Delete Django'
date: 2007-10-02T20:30:00.002+10:00
draft: false
url: /2007/10/mass-spam-delete-django_8712.html
tags: 
- django
- articles
- spam
- travel
---

As you can read, I've been traveling around quite a bit lately. This means I haven't been checking the comments on my blog, which means quite a bit of spam has been entered. I am blocking the spam via akismet, however, it is still recorded in the database. Being somebody who hates cluttered desktops, you can imagine how I feel about having a lot (447) of spam. Well, since akismet flips the is_public switch True for good comments and False for bad comments, that makes a **really** easy query in mysql.

```bash
mysql> delete from comments_freecomment where is_public = False

```  

Of course, make sure you have backed up your database first.