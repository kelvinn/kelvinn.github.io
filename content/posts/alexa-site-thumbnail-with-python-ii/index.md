---
title: 'Alexa Site Thumbnail with Python II'
date: 2007-06-06T20:30:00.007+10:00
draft: false
url: /2007/06/alexa-site-thumbnail-with-python-ii_629.html
tags: 
- howtos
---

This is how I actually use Alexa Site Thumbnail, and since I'min a sharing mood, I'll extend the code your way. In short, this takes the url and searches in STORELOC first, then any urls not already in STORELOC are retrieved and named via a slug. You need to pass two variables to either of these: blog_site.url and blot_site.slug -- since I'm using Django, this is naturally how sites are returned after I filter a queryset. What I do is place the call to Alexa as high up the page as I can, and because I've threaded this, the page can continue to load without waiting for Alexa's response. For instance, let's say you have some model with cool sites, and you want to return the sites filtered by owner...  

#### views.py


```python
from getAST import create_thumbnail_list
blog_sites = CoolSiteListing.objects.filter(owner__username__iexact=user_name, is_active=True)
create_thumbnail_list(blog_sites).start()

```  
  
Notice the .start() on the create_thumbnail_list function? That starts the thread.  

#### getAST.py

  
  
```bash
import base64
import datetime
import hmac
import sha
import sys
import re
import urllib
import xml.dom.minidom
import os
import threading

AWS_ACCESS_KEY_ID = 'your-access-key-id'
AWS_SECRET_ACCESS_KEY = 'your-super-secret-key'
STORELOC = "/path/to/store/thumbs/"

# This one is for an individual thumbnail...
class create_thumbnail(threading.Thread):
   # Override Thread's __init__ method to accept the parameters needed:
    def __init__(self, site_url, site_slug):
        self.site_url = site_url
        self.site_slug = site_slug
        threading.Thread.__init__(self)
        
    def run(self):
        # First check if the thumbnail exists already
        # site_slug is the name of thumbnail, for instance
        # I would generate the slug of my site as kelvinism_com,
        # and the entire image would be kelvinism_com.jpg 
        if not os.path.isfile(STORELOC+self.site_slug+".jpg"):
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
                'Url': self.site_url,
                'Action': 'Thumbnail',
                }
            url = 'http://ast.amazonaws.com/?'
            result_xmlstr = urllib.urlopen(url, urllib.urlencode(parameters)).read()
            result_xml = xml.dom.minidom.parseString(result_xmlstr)
            image_urls = result_xml.childNodes[0].getElementsByTagName('aws:Thumbnail')[0].firstChild.data
            #image_name = re.sub("\.|\/", "_", result_xml.childNodes[0].getElementsByTagName('aws:RequestUrl')[0].firstChild.data) + ".jpg"
            image_name = self.site_slug + ".jpg"
            store_name = STORELOC + image_name
            urllib.urlretrieve(image_urls, store_name)
            return image_name
  
# And this one is for a list
class create_thumbnail_list(threading.Thread):
   # Override Thread's __init__ method to accept the parameters needed:
   def __init__(self, all_sites):
      self.all_sites = all_sites
      threading.Thread.__init__(self)
   def run(self):     
        SITES = []
        # go through the sites and only request the ones that don't
        # exist yet
        for s in self.all_sites:
            if not os.path.isfile(STORELOC+s.slug+"SM.jpg"):
                SITES.append(s)
                       
        if SITES: 
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
            
            image_loc = {}
            image_num = []
            image_size = {}
            
            count = 1   
            for s in SITES:
                image_num = 'Thumbnail.%s.Url' % count
                image_loc[image_num] = s.url
                count += 1
                
            parameters = {
                'AWSAccessKeyId': AWS_ACCESS_KEY_ID,
                'Timestamp': timestamp,
                'Signature': signature,
                'Action': 'Thumbnail',
                'Thumbnail.Shared.Size': 'Small',
                }
                
            parameters.update(image_loc)
            
            ast_url = 'http://ast.amazonaws.com/?'
                
            result_xmlstr = urllib.urlopen(ast_url, urllib.urlencode(parameters)).read()
            result_xml = xml.dom.minidom.parseString(result_xmlstr)
    
            count = 0
            for s in SITES:
                image_urls = result_xml.childNodes[0].getElementsByTagName('aws:Thumbnail')[count].firstChild.data
                image_name = s.slug + "SM.jpg"
                store_name = STORELOC + image_name
                urllib.urlretrieve(image_urls, store_name)
                count += 1

```