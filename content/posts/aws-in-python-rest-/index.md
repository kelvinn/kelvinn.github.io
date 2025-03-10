---
title: 'AWS in Python (REST)'
date: 2007-03-03T21:30:00.002+11:00
draft: false
url: /2007/03/aws-in-python-rest_5343.html
tags: 
- articles
- amazon
- python
- rest
- api
---

As some of you may know, I have some projects cooked up. I don't expect to make a million bucks (wish me luck!), but a few extra bills in the pocket wouldn't hurt. Plus, I'm highly considering further education, which will set me back a few-thirty grand. That said, one of my projects will rely heavily on [Amazon Web Services](http://www.amazon.com/gp/redirect.html?ie=UTF8&location=http%3A%2F%2Fwww.amazon.com%2FAWS-home-page-Money%2Fb%3Fie%3DUTF8%26node%3D3435361&tag=kelvinismcom-20&linkCode=ur2&camp=1789&creative=9325)![](http://www.assoc-amazon.com/e/ir?t=kelvinismcom-20&l=ur2&o=1). Amazon has, for quite some time now, opened up their information via REST and SOAP. I've been trying (virtually the entire day) to get SOAP to work, but seem to get snagged on a few issues. Stay tuned.  
However, in my quest to read every RTFM I stumbled upon a post regarding Python+REST to access [Alexa Web Search](http://www.amazon.com/gp/redirect.html?ie=UTF8&location=http%3A%2F%2Fwww.amazon.com%2Fb%3Fie%3DUTF8%26node%3D269962011%26no%3D239513011%26me%3DA36L942TSJ2AJA&tag=kelvinismcom-20&linkCode=ur2&camp=1789&creative=9325)![](http://www.assoc-amazon.com/e/ir?t=kelvinismcom-20&l=ur2&o=1). After staring at Python code, especially trying to grapple why SOAP isn't working, updating the outdated REST code was a 5 minute hack. So, if you are interested in using Alexa Web Search with Python via Rest, look below:  
  
  

#### websearch.py

  
```

#!/usr/bin/python

"""
Test script to run a WebSearch query on AWS via the REST interface.  Written
 originally by Walter Korman (shaper@wgks.org), based on urlinfo.pl script from 
  AWIS-provided sample code, updated to the new API by  
Kelvin Nicholson (kelvin@kelvinism.com). Assumes Python 2.4 or greater.
"""

import base64
import datetime
import hmac
import sha
import sys
import urllib
import urllib2

AWS\_ACCESS\_KEY\_ID = 'your-access-key'
AWS\_SECRET\_ACCESS\_KEY = 'your-super-secret-key'

def get\_websearch(searchterm):
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
    
    signature = generate\_signature('WebSearch', timestamp, AWS\_SECRET\_ACCESS\_KEY)
    
    def generate\_rest\_url (access\_key, secret\_key, query):
        """Returns the AWS REST URL to run a web search query on the specified
        query string."""
    
        params = urllib.urlencode(
            { 'AWSAccessKeyId':access\_key,
              'Timestamp':timestamp,
              'Signature':signature,
              'Action':'WebSearch',
              'ResponseGroup':'Results',
              'Query':searchterm, })
        return "http://websearch.amazonaws.com/?%s" % (params)
    
    # print "Querying '%s'..." % (query)
    url = generate\_rest\_url(AWS\_ACCESS\_KEY\_ID, AWS\_SECRET\_ACCESS\_KEY, searchterm)
    # print "url => %s" % (url)
    print urllib2.urlopen(url).read()


```  
  
You run it like this:  
```
\>>> from websearch import get\_websearch
>>> get\_websearch('python')
```