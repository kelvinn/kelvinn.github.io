---
title: 'Alexa Site Thumbnail with Python'
date: 2007-06-06T20:30:00.008+10:00
draft: false
url: /2007/06/alexa-site-thumbnail-with-python_803.html
tags: 
- howtos
---

For one of my sites I needed to get thumbnails, yet [Alexa Site Thumbnail](http://developer.amazonwebservices.com/connect/kbcategory.jspa?categoryID=51) didn't have any code snippets for Python. Well, no they/you do.  

#### ThumbnailUtility.py

  
```python

import base64
import datetime
import hmac
import sha
import sys
import re
import urllib
import xml.dom.minidom

AWS_ACCESS_KEY_ID = 'your-access-key-id'
AWS_SECRET_ACCESS_KEY = 'your-super-secret-key'

# This one is for an individual thumbnail...
def create_thumbnail(site_url, img_size):
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
        'Size': img_size,
        }
    url = 'http://ast.amazonaws.com/?'
    result_xmlstr = urllib.urlopen(url, urllib.urlencode(parameters)).read()
    result_xml = xml.dom.minidom.parseString(result_xmlstr)
    image_url = result_xml.childNodes[0].getElementsByTagName('aws:Thumbnail')[0].firstChild.data
    return image_url
  
# And this one is for a list
def create_thumbnail_list(all_sites, img_size):
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
    for s in all_sites:
        image_num = 'Thumbnail.%s.Url' % count
        image_loc[image_num] = s
        count += 1
        
    parameters = {
        'AWSAccessKeyId': AWS_ACCESS_KEY_ID,
        'Timestamp': timestamp,
        'Signature': signature,
        'Action': 'Thumbnail',
        'Thumbnail.Shared.Size': img_size,
        }
        
    parameters.update(image_loc)
    
    ast_url = 'http://ast.amazonaws.com/?'
        
    result_xmlstr = urllib.urlopen(ast_url, urllib.urlencode(parameters)).read()
    result_xml = xml.dom.minidom.parseString(result_xmlstr)
    
    image_urls = []
    count = 0
    for s in all_sites:
        image_urls.append(result_xml.childNodes[0].getElementsByTagName('aws:Thumbnail')[count].firstChild.data)
        count += 1
    return image_urls


```  
  
This is how you interact with this code for a single thumbnail:  
```python
>>> from ThumbnailUtility import *
>>> create_thumbnail('kelvinism.com', 'Large')
u'http://s3-external-1.amazonaws.com/alexa-thumbnails/A46FF6A30BECB0730455F2AB306EDC28605BC19Cl?Signature=XpsxgPey4b0JgreZA46XnvHVVLo%3D&Expires=1181110547&AWSAccessKeyId=1FVZ0JNEJDA5TK457CR2'

```  
And for a list:  
```python
>>> from ThumbnailUtility import *
>>> all_sites = ['kelvinism.com', 'alexa.com', 'vpslink.com']
>>> create_thumbnail_list(all_sites, 'Small')
[u'http://s3-external-1.amazonaws.com/alexa-thumbnails/A46FF6A30BECB0730455F2AB306EDC28605BC19Cs?Signature=%2BfcOUKwH4xD9IH9o1vfto%2FMoALU%3D&Expires=1181110698&AWSAccessKeyId=1FVZ0JNEJDA5TK457CR2', u'http://s3-external-1.amazonaws.com/alexa-thumbnails/D798D8CE8F821FCC63159C92C85B70319E44D0EFs?Signature=6jriChrGM%2F8DoejN9dn9Dv3Lc5w%3D&Expires=1181110698&AWSAccessKeyId=1FVZ0JNEJDA5TK457CR2', u'http://s3-external-1.amazonaws.com/alexa-thumbnails/23529C34E0518AA9C2577653AC237D3647BA8D2Ds?Signature=5ksuwZx0I5TqXWL3Kt%2BWP6r2LQk%3D&Expires=1181110698&AWSAccessKeyId=1FVZ0JNEJDA5TK457CR2']

```  
  
This is just a simple example to get your feet wet, maybe you'll find it useful. If you are wondering how to integrate this with Django, don't worry, I've got you covered.