---
title: 'Remove Dead Tags'
date: 2009-09-21T20:30:00.002+10:00
draft: false
url: /2009/09/remove-dead-tags_6886.html
tags: 
- django
- howtos
---

I've noticed my django-tagging install has been giving a lot of empty entries when doing a lookup on a tag. Tonight I finally got around to looking at what was causing this. This is surely not the best way to do this, but at 12:00am on a weekday, well, I shouldn't be doing it in the first place... I first wanted to see what type of content was generating the error:

```
for item in TaggedItem.objects.all():
try:
print item.object
except:
print item.content\_type\_id

```  
  

Now that I could see what was causing it (I had removed an app that used django-tagging, but it left the tags with empty pointers). Removing the empty tags was easy enough:

```
for item in TaggedItem.objects.all():
try:
print item.object
except:
item.delete()

```  
  

No more hanging TaggedItems.