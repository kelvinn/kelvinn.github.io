---
title: 'Stock Android and Postfix'
date: 2011-01-09T21:30:00.002+11:00
draft: false
url: /2011/01/stock-android-and-postfix_2931.html
tags: 
- articles
- android
- postfix
---

I was having some issues with my personal mail server (Postfix) and my phone (Android). The logs depicted the below issue:  
  
  
  
```
Jan  9 09:19:53 ip-11-222-23-223 postfix/smtpd\[12345\]: NOQUEUE: reject: RCPT from 12-13-14-15.abc.com.au\[12.13.14.15\]: 504 5.5.2 : Helo command rejected: need fully-qualified hostname; from= to= proto=ESMTP helo= 
```  
  
We can see here that the stock Android email client is doing a 'helo localhost'. One part of my main.cf file specifies this:  
  
```
smtpd\_helo\_required = yes
smtpd\_helo\_restrictions =
    permit\_mynetworks,
    reject\_non\_fqdn\_helo\_hostname,
    reject\_invalid\_helo\_hostname,
    permit\_sasl\_authenticated,
    permit
```  
  
To resolve, unfortunately, just change the order to authenticated clients are permitted earlier:  
  
```
smtpd\_helo\_required = yes
smtpd\_helo\_restrictions =
    permit\_mynetworks,
    permit\_sasl\_authenticated,
    reject\_non\_fqdn\_helo\_hostname,
    reject\_invalid\_helo\_hostname,
    permit
```  
  
You also may need to do the same for smtpd\_recipient\_restrictions and/or smtpd\_sender\_restrictions (i.e. put permit\_sasl\_authenticated above the reject lines).