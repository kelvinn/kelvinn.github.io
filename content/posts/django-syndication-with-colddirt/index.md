---
title: 'Django Syndication with Colddirt'
date: 2007-06-03T20:30:00.007+10:00
draft: false
url: /2007/06/django-syndication-with-colddirt_5107.html
tags: 
- syndication
- django
- articles
- colddirt
---

Creating feeds in Django is freaking simple. I'll start with an example of just updating a feed with the newest objects (for instace, newest blog posts). Similar to the forms.py way of handling our different forms, I've created a feeds.py to handle the feeds.  

#### feeds.py

  
```python

from django.contrib.syndication.feeds import Feed
from colddirt.dirty.models import Dirt

class LatestDirts(Feed):
    title = "Cold Dirt"
    link = "/"
    description = "When you have dirt, you've got dirt.  Right..."
    copyright = 'All Rights Unreserved'
    
    def items(self):
        return Dirt.objects.all()[:50]


```  
  
What this will do is query our Dirt DB and return an obj. The fields here are pretty well documented in the Django docs, besides being pretty obvious.  

#### urls.py

  
We need three things in our urls.py -- first, import our feeds from feeds.py:  
```python
from colddirt.feeds import LatestDirts
```  
  
Next, we map the feed we want to a name urls.py can use:  
```python
feeds = {
    'newdirt': LatestDirts,
}

```  
  
Finally we create which URL to use for the feeds:  
```python
    (r'^feeds/(?P.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
```  
  
When we look at a request, the process goes like this: it comes in as /feeds/newdirt/, which then gets looked up and matches newdirt in the feeds_dict. Next, LatestDirts is looked at and evaluated, and returned. But how is it returned? One final thing to do is create a template for the feed to use, which is where we can tell exactly _what_ is to be displayed to the user.  

#### templates/feeds/newdirt_title.html

  
```plain
{{ obj.dirtword }}
```  

#### templates/feeds/newdirt_description.html

  
```plain
{{ obj.description }}
```  
The naming for the templates, as usual, is important. If you want to have that little orange RSS button near your url, add this to your template's head. 

  
So, there you have it, a simple example of how to use Django's syndication framework. I'll follow this up with another slightly more complex tutorial.