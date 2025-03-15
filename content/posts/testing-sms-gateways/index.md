---
title: 'Testing SMS Gateways'
date: 2009-07-14T20:30:00.002+10:00
draft: false
url: /2009/07/testing-sms-gateways_5212.html
tags: 
- alarm
- sms
- articles
- arduino
---

For one of my projects I'm testing an SMS gateway, and decided it would be fun to build a useful alarm clock out of it. For those of you who know Python, you may find this funny. /dev/ttyUSB0 is my Arduino with a temperature sensor.

```python
import serial
import urllib2
 
def check_temp():
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    t = ser.readline().strip()
    return float(t)
 
    t = check_temp()
    if int(t) < 8:
        message = "It+is+now+%f+degrees;+chuck+a+sicky." % t
        f = urllib2.urlopen('http://api.clickatell.com/http/sendmsg?user=johnd&password=p@55w0rd&api_id=2132867&from=61433735555&to=61433735555&text=%s' % message)

```bash

And in crontab:

```bash
45 6 * * * python /opt/scripts/temp_alarm.py


```