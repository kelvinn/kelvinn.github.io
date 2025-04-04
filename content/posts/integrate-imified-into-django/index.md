---
title: 'Integrate imified into Django'
date: 2011-01-18T21:30:00.002+11:00
draft: false
url: /2011/01/integrate-imified-into-django_2631.html
tags: 
- django
- python
- howtos
- xmpp
---

I recently had the desire to send small updates to my so called [lifestream](http://www.blogger.com/about-me/) page via XMPP/GTalk. I played around with Twisted Words and several other Python XMPP clients, but I didn't really want to keep a daemon running if unnecessary. It turns out imified took a lot of the pain out of it. The steps for me were as follows:  
Create an account with imified, and create a URL, e.g. /app/api/  
We then configure the **urls.conf**  

```python
urlpatterns = patterns('',  
    (r'^app/api/$', bot_stream),
)

```  
  
We then create the necessary views. So, in **views.py**:  

```python
from django.shortcuts import render_to_response
from django.http import HttpResponse
from lifestream.forms import *
from datetime import datetime
from time import time
 
def bot_stream(request):
    if request.method == 'POST':
        botkey = request.POST.get('botkey')
        username = request.POST.get('user')
        msg = request.POST.get('msg')
        network = request.POST.get('network')
    
    if username == "username@gmail.com" or network == "debugger":
        blob_obj = Blob(id=time(), body=msg, service_name="Mobile",
        link="http://www.kelvinism.com/about-me/", published=datetime.now())
        blob_obj.save()
        resp = "OK"
    else:
        resp = "Wrong username %s" % username
    else:
        resp = "No POST data"
    return HttpResponse(resp)

```  
  
To complete this little example, you can see what I used for my **models.py**  

```python
class Blob(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    body = models.TextField(max_length = 1024, null = True, blank = True)
    service_name = models.CharField(max_length=50, null=True, blank=True)
    link = models.URLField(max_length=255, verify_exists=False, null=True, blank=True)
    published = models.DateTimeField(null=True, blank=True)
 
def __unicode__(self):
    return self.id
 
class Meta:
    ordering = ['-published']
    verbose_name = 'Blob'
    verbose_name_plural = 'Blobs'
 
def get_absolute_url(self):
    return "/about-me/"



```  
  
It maybe isn't super elegant, but it works just fine, and maybe can provide a hint if somebody else is contemplating using a homebuilt xmpp solution, or just pawning it off on IMified.