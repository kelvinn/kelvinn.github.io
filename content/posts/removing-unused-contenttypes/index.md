---
title: 'Removing Unused ContentTypes'
date: 2011-01-19T21:30:00.002+11:00
draft: false
url: /2011/01/removing-unused-contenttypes_4881.html
tags: 
- django
- howtos
---

I've been cleaning up my personal blog a bit, and I noticed that my tagging system recently broke. I've investigated the cause, and it appears to be because I removed some apps but the contenttypes remained. This meant that whenever I tried calling a tag with a TaggedItem that had been deleted, I was getting this error:  

```plain
'NoneType' object has no attribute '_meta'


```  
  
The solution is to first list all app\_labels for contenttypes, and then delete any not in use.  

```plain
In [61]: from django.contrib.contenttypes.models import ContentType
 
In [62]: for ct in ContentType.objects.all(): print ct.app_label
   ....:
picasaweb
lifestream
readernaut
delicious
mapfeed
comments
...
```

I could then delete the unused contenttypes.  

```python
ct_list = ["delicious", "flickr", "photologue", "twitter"]
 
for ct_label in ct_list:
    for ct in ContentType.objects.filter(app_label=ct_label):
        ct.delete()
    
```  
  
And no more errors! For more details take a look at David's [article.](http://fragmentsofcode.wordpress.com/2010/09/21/cleanly-removing-a-django-app/)