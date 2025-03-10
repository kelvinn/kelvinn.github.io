---
title: 'Django SVN Update Goes Splat'
date: 2007-05-09T20:30:00.002+10:00
draft: false
url: /2007/05/django-svn-update-goes-splat_5490.html
tags: 
- django
- articles
- doh
---

I'm writing this just in case somebody runs into this same issue. I'm about to go live with a website and figured it would be best to have the latest SVN snapshot checked out from Django. I updated, and noticed that my voting module didn't quite work as expected. I was getting the following error:  
```
'module' object has no attribute 'GenericForeignKey'
```  
  
I jumped into Trac and noticed that _just yesterday_ some things were rearranged. In short, if you are using generic relations, you'll need to change two parts of your code. First, the generic relations field must be imported out of conttenttype.  
```
from django.contrib.contenttypes import generic
```  
  
And second, you'll need to change the 'location prefix' (for lack of a better description:  
**From:**  
```
generic\_field = models.GenericRelation(SomeOtherModel)
```  
  
**To:**  
```
generic\_field = generic.GenericRelation(SomeOtherModel)
```  
  
All should be find from there on out. For more information, take a look at [the reference wiki article](http://code.djangoproject.com/wiki/BackwardsIncompatibleChanges).