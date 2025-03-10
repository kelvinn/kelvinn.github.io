---
title: 'Alexa Site Thumbnail with Python II'
date: 2007-06-06T20:30:00.007+10:00
draft: false
url: /2007/06/alexa-site-thumbnail-with-python-ii_629.html
tags: 
- howtos
---

This is how I actually use Alexa Site Thumbnail, and since I'min a sharing mood, I'll extend the code your way. In short, this takes the url and searches in STORELOC first, then any urls not already in STORELOC are retrieved and named via a slug. You need to pass two variables to either of these: blog\_site.url and blot\_site.slug -- since I'm using Django, this is naturally how sites are returned after I filter a queryset. What I do is place the call to Alexa as high up the page as I can, and because I've threaded this, the page can continue to load without waiting for Alexa's response. For instance, let's say you have some model with cool sites, and you want to return the sites filtered by owner...  

#### views.py

  
```
from getAST import create\_thumbnail\_list
blog\_sites = CoolSiteListing.objects.filter(owner\_\_username\_\_iexact=user\_name, is\_active=True)
create\_thumbnail\_list(blog\_sites).start()

```  
  
Notice the .start() on the create\_thumbnail\_list function? That starts the thread.  

#### getAST.py

  
  
```
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

AWS\_ACCESS\_KEY\_ID = 'your-access-key-id'
AWS\_SECRET\_ACCESS\_KEY = 'your-super-secret-key'
STORELOC = "/path/to/store/thumbs/"

# This one is for an individual thumbnail...
class create\_thumbnail(threading.Thread):
   # Override Thread's \_\_init\_\_ method to accept the parameters needed:
    def \_\_init\_\_(self, site\_url, site\_slug):
        self.site\_url = site\_url
        self.site\_slug = site\_slug
        threading.Thread.\_\_init\_\_(self)
        
    def run(self):
        # First check if the thumbnail exists already
        # site\_slug is the name of thumbnail, for instance
        # I would generate the slug of my site as kelvinism\_com,
        # and the entire image would be kelvinism\_com.jpg 
        if not os.path.isfile(STORELOC+self.site\_slug+".jpg"):
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
                'Url': self.site\_url,
                'Action': 'Thumbnail',
                }
            url = 'http://ast.amazonaws.com/?'
            result\_xmlstr = urllib.urlopen(url, urllib.urlencode(parameters)).read()
            result\_xml = xml.dom.minidom.parseString(result\_xmlstr)
            image\_urls = result\_xml.childNodes\[0\].getElementsByTagName('aws:Thumbnail')\[0\].firstChild.data
            #image\_name = re.sub("\\.|\\/", "\_", result\_xml.childNodes\[0\].getElementsByTagName('aws:RequestUrl')\[0\].firstChild.data) + ".jpg"
            image\_name = self.site\_slug + ".jpg"
            store\_name = STORELOC + image\_name
            urllib.urlretrieve(image\_urls, store\_name)
            return image\_name
  
# And this one is for a list
class create\_thumbnail\_list(threading.Thread):
   # Override Thread's \_\_init\_\_ method to accept the parameters needed:
   def \_\_init\_\_(self, all\_sites):
      self.all\_sites = all\_sites
      threading.Thread.\_\_init\_\_(self)
   def run(self):     
        SITES = \[\]
        # go through the sites and only request the ones that don't
        # exist yet
        for s in self.all\_sites:
            if not os.path.isfile(STORELOC+s.slug+"SM.jpg"):
                SITES.append(s)
                       
        if SITES: 
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
            for s in SITES:
                image\_num = 'Thumbnail.%s.Url' % count
                image\_loc\[image\_num\] = s.url
                count += 1
                
            parameters = {
                'AWSAccessKeyId': AWS\_ACCESS\_KEY\_ID,
                'Timestamp': timestamp,
                'Signature': signature,
                'Action': 'Thumbnail',
                'Thumbnail.Shared.Size': 'Small',
                }
                
            parameters.update(image\_loc)
            
            ast\_url = 'http://ast.amazonaws.com/?'
                
            result\_xmlstr = urllib.urlopen(ast\_url, urllib.urlencode(parameters)).read()
            result\_xml = xml.dom.minidom.parseString(result\_xmlstr)
    
            count = 0
            for s in SITES:
                image\_urls = result\_xml.childNodes\[0\].getElementsByTagName('aws:Thumbnail')\[count\].firstChild.data
                image\_name = s.slug + "SM.jpg"
                store\_name = STORELOC + image\_name
                urllib.urlretrieve(image\_urls, store\_name)
                count += 1

```