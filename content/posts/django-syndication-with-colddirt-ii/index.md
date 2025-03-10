---
title: 'Django Syndication with Colddirt II'
date: 2007-06-03T20:30:00.006+10:00
draft: false
url: /2007/06/django-syndication-with-colddirt-ii_3665.html
tags: 
- django
- articles
- xml
---

Since I've already covered a really simple syndication example, I'll move onto something a little more complex. Let's say you want to offer syndication that is slightly more custom. The Django [syndication docs](http://www.djangoproject.com/documentation/syndication_feeds/) give an example from [Adrian's](http://www.holovaty.com/) [Chicagocrime.org](http://www.chicagocrime.org/) syndication of beats. I had to ponder a minute to get "custom" syndication to work, so here's my example from start to finish.  
First, as usual, feeds.py  

#### feeds.py

  
```
class PerDirt(Feed):

    link = "/"
    copyright = 'Copyright (c) 2007, Blog Mozaic'
    
    def get\_object(self, bits):
        from django.shortcuts import get\_object\_or\_404
        if len(bits) != 1:
            raise ObjectDoesNotExist
        my\_dirt = get\_object\_or\_404(Dirt, slug\_\_exact=bits\[0\])
        return my\_dirt

    def title(self, obj):
        return obj.slug
    
    def description(self, obj):
        return obj.description
    
    def items(self, obj):
        from django.contrib.comments.models import FreeComment
        return FreeComment.objects.filter(object\_id=obj.id).order\_by('-submit\_date')

```  
You can see that this differs slightly from the simpler syndication example. I'll not a few things. But first, I need to show urls.py:  

#### urls.py

  
```
feeds = {
    'mydirt': PerDirt,
}

urlpatterns = patterns('',
    (r'^feeds/(?P<url>.\*)/$', 'django.contrib.syndication.views.feed', {'feed\_dict': feeds}),
)
```  
  
  
  
Let's pretend the dirt word (or if you were doing a blog, you could do this based on slug) is "nifty". So, the process is like this: a request comes in as /feeds/mydirt/nifty/ -- it is first looked up in the feed\_dict (because of the mydirt part) and then sent to PerDict. Once in PerDict it hits the first def, get\_object. One of the things that confused me at first is what the 'bits' part is. Simply put: it is the crap after you tell Django which feed to use. Similar to the beats example, I'm testing to make sure the length is only one -- so if the word doesn't exist or somebody just types in feeds/mydirt/nifty/yeehaaa/ -- they will get an error. Next the object is looked up, in this case the dirt word (in your case, maybe a blog entry).  
The title and description are self-explanatory. The items are a query from the FreeComment database, ordered by date. What we need next is the correct templates.  

#### templates/feeds/mydirt\_title.html

  
  
```
Comment by {{ obj.person\_name }}
```  
  
  
  
  
Once again, the filename is important (mydirt\_title). obj.person\_name is the name from the comment.  

#### templates/feeds/mydirt\_description.html

  
  
  
  
```
{{ obj.comment }}
Posted by: {{ obj.person\_name }}
Published: {{ obj.submit\_date }}
```  
  
  
  
  
If you are curious how to get that little orange icon next to your site's url, you do this:  
```

```  
  
That's it. Hopefully I've explained how to create somewhat custom syndication feeds, in case you needed another example.