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
  
  
  
```plain
Jan  9 09:19:53 ip-11-222-23-223 postfix/smtpd[12345]: NOQUEUE: reject: RCPT from 12-13-14-15.abc.com.au[12.13.14.15]: 504 5.5.2 <localhost>: Helo command rejected: need fully-qualified hostname; from=<emailaddr kelvinism.com="kelvinism.com"> to=<emailaddr gmail.com="gmail.com"> proto=ESMTP helo=<localhost>
</localhost></emailaddr></emailaddr></localhost>
```  
  
We can see here that the stock Android email client is doing a 'helo localhost'. One part of my main.cf file specifies this:  
  
```bash
smtpd_helo_required = yes
smtpd_helo_restrictions =
    permit_mynetworks,
    reject_non_fqdn_helo_hostname,
    reject_invalid_helo_hostname,
    permit_sasl_authenticated,
    permit

```  
  
To resolve, unfortunately, just change the order to authenticated clients are permitted earlier:  
  
```bash
smtpd_helo_required = yes
smtpd_helo_restrictions =
    permit_mynetworks,
    permit_sasl_authenticated,
    reject_non_fqdn_helo_hostname,
    reject_invalid_helo_hostname,
    permit

```  
  
You also may need to do the same for smtpd_recipient_restrictions and/or smtpd_sender_restrictions (i.e. put permit_sasl_authenticated above the reject lines).