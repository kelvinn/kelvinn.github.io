---
title: 'Alexa Site Thumbnail And Django'
date: 2007-06-06T20:30:00.006+10:00
draft: false
url: /2007/06/alexa-site-thumbnail-and-django_7479.html
tags: 
- howtos
---

So, you've seen how to look up thumbnails [via python](/howtos/alexa-site-thumbnail-python/), but wonder how to integrate this with Django? I created a [sample app to demonstrate](/webthumbs/). One thing to note about this app is it is slightly more complex than just using the [previously mentioned](/howtos/alexa-site-thumbnail-python/) ThumbnailUtility. For starters, the thumbnail is downloaded from Alexa onto the server. Another part is first searching if the thumbnail exists already, and if it does, serving that instead of querying Alexa. Let's just start with some code.

#### getAST.py

  
  
```
  
  
#!/usr/bin/python  
import base64  
import datetime  
import hmac  
import sha  
import sys  
import re  
import urllib  
import xml.dom.minidom  
import os  
from urlparse import urlsplit  
  
AWS\_ACCESS\_KEY\_ID = 'your-access-key-id'  
AWS\_SECRET\_ACCESS\_KEY = 'your-secret-key'  
STORELOC = "/path/to/store/webthumbs/"  
  
def create\_thumbnail(site\_url):  
    image\_name = re.sub("\\.|\\/", "\_", '.'.join(urlsplit(site\_url)\[1\].rsplit('.', 2)\[-2:\])) + ".jpg"  
    if not os.path.isfile(STORELOC+image\_name):  
        def generate\_timestamp(dtime):  
            return dtime.strftime("%Y-%m-%dT%H:%M:%SZ")  
        def generate\_signature(operation, timestamp, secret\_access\_key):  
            my\_sha\_hmac = hmac.new(secret\_access\_key, operation + timestamp, sha)  
            my\_b64\_hmac\_digest = base64.encodestring(my\_sha\_hmac.digest()).strip()  
            return my\_b64\_hmac\_digest  
        timestamp\_datetime = datetime.datetime.utcnow()  
        timestamp\_list = list(timestamp\_datetime.timetuple())  
        timestamp\_list\[6\] = 0  
        timestamp\_tuple = tuple(timestamp\_list)  
        timestamp = generate\_timestamp(timestamp\_datetime)  
        signature = generate\_signature('Thumbnail', timestamp, AWS\_SECRET\_ACCESS\_KEY)  
        parameters = {  
            'AWSAccessKeyId': AWS\_ACCESS\_KEY\_ID,  
            'Timestamp': timestamp,  
            'Signature': signature,  
            'Url': site\_url,  
            'Action': 'Thumbnail',  
            }  
        url = 'http://ast.amazonaws.com/?'  
        result\_xmlstr = urllib.urlopen(url, urllib.urlencode(parameters)).read()  
        result\_xml = xml.dom.minidom.parseString(result\_xmlstr)  
        image\_urls = result\_xml.childNodes\[0\].getElementsByTagName('aws:Thumbnail')\[0\].firstChild.data  
        store\_name = STORELOC + image\_name  
        urllib.urlretrieve(image\_urls, store\_name)  
    return image\_name  
      
  
      

```  
  

Not too much to mention here, basically just an extended version of the ThumbnailUtility. The only difference is the test at the beginning, and actually downloading the thumbnail.

#### views.py

  
```
  
\# Create your views here.  
from django.shortcuts import render\_to\_response, get\_object\_or\_404  
from django.http import HttpResponseRedirect, HttpResponse  
from webthumbs.models import \*  
from django import newforms as forms  
from getAST import create\_thumbnail  
  
attrs\_dict = { 'class': 'form-highlight' }  
  
class imageForm(forms.Form):  
    url = forms.URLField(max\_length=100, verify\_exists=True, widget=forms.TextInput(attrs=attrs\_dict), initial='http://', label='Site URL')  
      
def index(request):  
    disp\_img = ''  
    # generate default form  
    f = imageForm()  
    # handle add events  
    if request.method == 'POST':  
        if request.POST\['submit\_action'\] == 'Submit':  
            # attempt to do add  
            add\_f = imageForm(request.POST)  
            if add\_f.is\_valid():  
                site\_url = request.POST\['url'\]  
                disp\_img = create\_thumbnail(site\_url)  
        else:  
            f = add\_f  
    return render\_to\_response(  
        'webthumbs/index.html',   
        {'printform': f,   
        'disp\_img': disp\_img  
        }  
    )  
  
  

```  
  

The key thing to look at here is how getAST is called:

```
  
  
site\_url = request.POST\['url'\]  
disp\_img = create\_thumbnail(site\_url)  
  
  

```  

#### index.html

  
```
  
{% extends "base.html" %}  
  
{% block title %}Kelvinism.com - Blog{% endblock %}  
  
{% block content %}  

  
What thumbnail do you want?  
  

  
    {{ printform }}  
  

  
  
![](http://media.kelvinism.com/webthumbs/{{ disp_img }})  

  
  
  
{% endblock %}  
  

```  

So, there you have it, the code to take a url via form and display it right away.