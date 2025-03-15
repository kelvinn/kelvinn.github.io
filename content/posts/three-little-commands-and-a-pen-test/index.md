---
title: 'Three Little Commands and a Pen-Test'
date: 2006-10-15T20:30:00.005+10:00
draft: false
url: /2006/10/three-little-commands-and-pen-test_9.html
tags: 
- articles
- hacking
---

Yea, you read that right. Three commands and you can run a pen-test on your website/webserver. So, how?

```bash
kelvin@home:~$ sudo apt-get install nikto  
kelvin@home:~$ sudo nikto -update  
kelvin@home:~$ nikto -h www.thoughtdeposit.net
```

As you can see, Nikto is a web server scanner, apparently for over 3200 dangerous files/vulnerabilities. Additional features can be seen at the [Nikto](http://www.cirt.net/code/nikto.shtml) website, yet you will certainly want to add this old gem to your webserver toolbelt as soon as possible.