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

  
  
```python
  
  
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

AWS_ACCESS_KEY_ID = 'your-access-key-id'
AWS_SECRET_ACCESS_KEY = 'your-secret-key'
STORELOC = "/path/to/store/webthumbs/"

def create_thumbnail(site_url):
    image_name = re.sub("\.|\/", "_", '.'.join(urlsplit(site_url)[1].rsplit('.', 2)[-2:])) + ".jpg"
    if not os.path.isfile(STORELOC+image_name):
        def generate_timestamp(dtime):
            return dtime.strftime("%Y-%m-%dT%H:%M:%SZ")
        def generate_signature(operation, timestamp, secret_access_key):
            my_sha_hmac = hmac.new(secret_access_key, operation + timestamp, sha)
            my_b64_hmac_digest = base64.encodestring(my_sha_hmac.digest()).strip()
            return my_b64_hmac_digest
        timestamp_datetime = datetime.datetime.utcnow()
        timestamp_list = list(timestamp_datetime.timetuple())
        timestamp_list[6] = 0
        timestamp_tuple = tuple(timestamp_list)
        timestamp = generate_timestamp(timestamp_datetime)
        signature = generate_signature('Thumbnail', timestamp, AWS_SECRET_ACCESS_KEY)
        parameters = {
            'AWSAccessKeyId': AWS_ACCESS_KEY_ID,
            'Timestamp': timestamp,
            'Signature': signature,
            'Url': site_url,
            'Action': 'Thumbnail',
            }
        url = 'http://ast.amazonaws.com/?'
        result_xmlstr = urllib.urlopen(url, urllib.urlencode(parameters)).read()
        result_xml = xml.dom.minidom.parseString(result_xmlstr)
        image_urls = result_xml.childNodes[0].getElementsByTagName('aws:Thumbnail')[0].firstChild.data
        store_name = STORELOC + image_name
        urllib.urlretrieve(image_urls, store_name)
    return image_name
      
  
      

```  
  

Not too much to mention here, basically just an extended version of the ThumbnailUtility. The only difference is the test at the beginning, and actually downloading the thumbnail.

#### views.py

  
```python
  
# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from webthumbs.models import *
from django import newforms as forms
from getAST import create_thumbnail

attrs_dict = { 'class': 'form-highlight' }

class imageForm(forms.Form):
    url = forms.URLField(max_length=100, verify_exists=True, widget=forms.TextInput(attrs=attrs_dict), initial='http://', label='Site URL')
    
def index(request):
    disp_img = ''
    # generate default form
    f = imageForm()
    # handle add events
    if request.method == 'POST':
        if request.POST['submit_action'] == 'Submit':
            # attempt to do add
            add_f = imageForm(request.POST)
            if add_f.is_valid():
                site_url = request.POST['url']
                disp_img = create_thumbnail(site_url)
        else:
            f = add_f
    return render_to_response(
        'webthumbs/index.html', 
        {'printform': f, 
        'disp_img': disp_img
        }
    )
  
  

```  
  

The key thing to look at here is how getAST is called:

```python
  
  
site_url = request.POST['url']  
disp_img = create_thumbnail(site_url)  
  
  

```  

#### index.html

  
```html
  
{% extends "base.html" %}  
  
{% block title %}Kelvinism.com - Blog{% endblock %}  
  
{% block content %}  

  
What thumbnail do you want?  
  

  
    {{ printform }}  
  
  
  
{% endblock %}  
  

```  

So, there you have it, the code to take a url via form and display it right away.