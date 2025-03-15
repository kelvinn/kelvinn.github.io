---
title: 'Simple Ajax with Django'
date: 2007-06-01T20:30:00.005+10:00
draft: false
url: /2007/06/simple-ajax-with-django_1754.html
tags: 
- ajax
- django
- json
- articles
- colddirt
---

So, the Django developers, in my opinion, are freaking smart. Instead of bundling Django with a particular library, they have added XML and JSON serialization; us humble users can choose whatever AJAX library we want. [Prototype 1.5.1](http://www.prototypejs.org/) has been pretty fun to work with, so I'll kick off this demo with a really simple example.  
How simple? The intended goal is to have the total number of 'dirts' update without user intervention. _Laaaammmeee_. If you are a visual type of person, [take a look](http://www.colddirt.com/huh/) on the Colddirt [huh](http://www.colddirt.com/huh/) page. That number automatically increases without user intervention. And this is how.  
The process (some pseudocode) will go like this:  


check /dirt_count/ for an update  
  
if update:  
  
  make number bigger  
  
else:  
  
  check less frequently  
  
  
Pretty simple, eh?  

#### urls.py

  
```bash
    (r'^dirt_count/$', views.dirt_count),
```  
As you can see, it just sends the request to the view.  

#### views.py

  
```bash
def dirt_count(request):
    from django.http import HttpResponse
    countd = str(Dirt.objects.all().count())
    return HttpResponse(countd, mimetype='text/plain')

```  
  
Pretty simple -- count the dirts. That makes sense.  

#### dirty.js

  
```javascript
new Ajax.PeriodicalUpdater('dirtcount', '/dirt_count/', {
  method: 'get',
  frequency: 3,
  decay: 2,
});
```  
  
Yea, Prototype makes that _real_ easy. Just make sure to have a element in your template somewhere with an id of 'dirtcount'.  

#### templates/huh.html

  
```bash
0
```