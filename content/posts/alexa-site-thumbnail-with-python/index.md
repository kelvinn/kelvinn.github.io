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

  
```

import base64
import datetime
import hmac
import sha
import sys
import re
import urllib
import xml.dom.minidom

AWS\_ACCESS\_KEY\_ID = 'your-access-key-id'
AWS\_SECRET\_ACCESS\_KEY = 'your-super-secret-key'

# This one is for an individual thumbnail...
def create\_thumbnail(site\_url, img\_size):
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
        'Size': img\_size,
        }
    url = 'http://ast.amazonaws.com/?'
    result\_xmlstr = urllib.urlopen(url, urllib.urlencode(parameters)).read()
    result\_xml = xml.dom.minidom.parseString(result\_xmlstr)
    image\_url = result\_xml.childNodes\[0\].getElementsByTagName('aws:Thumbnail')\[0\].firstChild.data
    return image\_url
  
# And this one is for a list
def create\_thumbnail\_list(all\_sites, img\_size):
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
    
    image\_loc = {}
    image\_num = \[\]
    image\_size = {}
    
    count = 1   
    for s in all\_sites:
        image\_num = 'Thumbnail.%s.Url' % count
        image\_loc\[image\_num\] = s
        count += 1
        
    parameters = {
        'AWSAccessKeyId': AWS\_ACCESS\_KEY\_ID,
        'Timestamp': timestamp,
        'Signature': signature,
        'Action': 'Thumbnail',
        'Thumbnail.Shared.Size': img\_size,
        }
        
    parameters.update(image\_loc)
    
    ast\_url = 'http://ast.amazonaws.com/?'
        
    result\_xmlstr = urllib.urlopen(ast\_url, urllib.urlencode(parameters)).read()
    result\_xml = xml.dom.minidom.parseString(result\_xmlstr)
    
    image\_urls = \[\]
    count = 0
    for s in all\_sites:
        image\_urls.append(result\_xml.childNodes\[0\].getElementsByTagName('aws:Thumbnail')\[count\].firstChild.data)
        count += 1
    return image\_urls


```  
  
This is how you interact with this code for a single thumbnail:  
```
\>>> from ThumbnailUtility import \*
>>> create\_thumbnail('kelvinism.com', 'Large')
u'http://s3-external-1.amazonaws.com/alexa-thumbnails/A46FF6A30BECB0730455F2AB306EDC28605BC19Cl?Signature=XpsxgPey4b0JgreZA46XnvHVVLo%3D&Expires=1181110547&AWSAccessKeyId=1FVZ0JNEJDA5TK457CR2'
```  
And for a list:  
```
\>>> from ThumbnailUtility import \*
>>> all\_sites = \['kelvinism.com', 'alexa.com', 'vpslink.com'\]
>>> create\_thumbnail\_list(all\_sites, 'Small')
\[u'http://s3-external-1.amazonaws.com/alexa-thumbnails/A46FF6A30BECB0730455F2AB306EDC28605BC19Cs?Signature=%2BfcOUKwH4xD9IH9o1vfto%2FMoALU%3D&Expires=1181110698&AWSAccessKeyId=1FVZ0JNEJDA5TK457CR2', u'http://s3-external-1.amazonaws.com/alexa-thumbnails/D798D8CE8F821FCC63159C92C85B70319E44D0EFs?Signature=6jriChrGM%2F8DoejN9dn9Dv3Lc5w%3D&Expires=1181110698&AWSAccessKeyId=1FVZ0JNEJDA5TK457CR2', u'http://s3-external-1.amazonaws.com/alexa-thumbnails/23529C34E0518AA9C2577653AC237D3647BA8D2Ds?Signature=5ksuwZx0I5TqXWL3Kt%2BWP6r2LQk%3D&Expires=1181110698&AWSAccessKeyId=1FVZ0JNEJDA5TK457CR2'\]
```  
  
This is just a simple example to get your feet wet, maybe you'll find it useful. If you are wondering how to integrate this with Django, don't worry, I've got you covered.