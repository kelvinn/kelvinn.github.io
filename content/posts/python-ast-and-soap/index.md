---
title: 'Python, AST and SOAP'
date: 2007-03-07T21:30:00.002+11:00
draft: false
url: /2007/03/python-ast-and-soap_3058.html
tags: 
- soap
- articles
- amazon
- python
- api
---

For one of my projects I need to generate thumbnails for a page. And lots and lots and lots of them. Even though I can generate them via a python script and a very light "gtk browser", I would prefer to mitigate the server load. To do this I've decided to tap into the Alexa Thumbnail Service. They allow two methods: REST and SOAP. After several hours of testing things out, I've decided to toss in the towel and settle on REST. If you can spot the error with my SOAP setup, I owe you a beer.  
I'm using the ZSI module for python.  

#### 1\. wsdl2py

  
I pull in the needed classes by using wsdl2py.  
```
wsdl2py -b http://ast.amazonaws.com/doc/2006-05-15/AlexaSiteThumbnail.wsdl
```  
  

#### 2\. Look at the code generated.

  
See [AlexaSiteThumbnail\_types.py](http://www.kelvinism.com/media/types.html) and [AlexaSiteThumbnail\_client.py](http://www.kelvinism.com/media/client.html).  
  

#### 3\. Write python code to access AST over SOAP.

  
  
```

#!/usr/bin/env python
import sys
import datetime
import hmac
import sha
import base64
from AlexaSiteThumbnail\_client import \*

print 'Starting...'

AWS\_ACCESS\_KEY\_ID = 'super-duper-access-key'
AWS\_SECRET\_ACCESS\_KEY = 'super-secret-key'

print 'Generating signature...'

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
timestamp\_str = generate\_timestamp(timestamp\_datetime)

signature = generate\_signature('Thumbnail', timestamp\_str, AWS\_SECRET\_ACCESS\_KEY)

print 'Initializing Locator...'

locator = AlexaSiteThumbnailLocator()
port = locator.getAlexaSiteThumbnailPort(tracefile=sys.stdout)

print 'Requesting thumbnails...'

request = ThumbnailRequestMsg()
request.Url = "alexa.com"
request.Signature = signature
request.Timestamp = timestamp\_tuple
request.AWSAccessKeyId = AWS\_ACCESS\_KEY\_ID
request.Request = \[request.new\_Request()\]

resp = port.Thumbnail(request)

```  
  
  
  

#### 4\. Run, and see error.

  
```
ZSI.EvaluateException: Got None for nillable(False), minOccurs(1) element 
(http://ast.amazonaws.com/doc/2006-05-15/,Url), 

 xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" 
xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" 
xmlns:ZSI="http://www.zolera.com/schemas/ZSI/" 
xmlns:ns1="http://ast.amazonaws.com/doc/2006-05-15/" 
xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

\[Element trace: /SOAP-ENV:Body/ns1:ThumbnailRequest\]
```  
  

#### 5\. Conclusion

  
  
I'm not entirely certain what I'm doing wrong. I've also written another version but actually with NPBinding connecting to the wsdl file. It seems to work much better, as it fully connects, and I get a 200, but it doesn't return the thumbnail location in the response, and I get a:  
```
TypeError: Response is "text/plain", not "text/xml"
```  
  
So, while I have things working fine with REST, I would like to get the SOAP calls working. One beer reward.