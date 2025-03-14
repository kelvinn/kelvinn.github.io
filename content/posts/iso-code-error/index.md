---
title: 'ISO Code Error'
date: 2009-06-17T20:30:00.002+10:00
draft: false
url: /2009/06/iso-code-error_1265.html
tags: 
- ubuntu
- python
- pytz
- howtos
---

I've received this error a few times when working with pytz:

```python
Error reading file '/usr/share/xml/iso-codes/iso_3166.xml'

```  
  

In short, install the 'iso-codes' package in Ubuntu/Debian. I'm sure this is covered in the manual that I didn't read, but I'm sure others didn't read it too.

```bash
apt-get install iso-codes

```