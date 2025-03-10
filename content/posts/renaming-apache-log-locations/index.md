---
title: 'Renaming Apache Log Locations'
date: 2009-01-25T21:30:00.002+11:00
draft: false
url: /2009/01/renaming-apache-log-locations_1724.html
tags: 
- scripting
- linux
- articles
- apache
- bash
---

I realized a few of my log files were growing unusually large, and even worse, logrotate was skipping them. I took a look in logrotate.d and straight away realized why: I had created silly names for the log file. logrotate look for .log files, but I had specified mine as .log -- e.g. kelvinism\_access\_log. I was as familiar with logrotate when I set up the domains, so set forth to get them in the rotation.

Firstly, I had to rename the actual log files. So, to rename kelvinism\_access\_log to kelvinism\_access.log, a one-liner:

```
for x in \*\_log; do mv $x \`basename $x \_log\`.log; done;

```  
  

Next, I needed to rename the log location inside each of the Apache config files. While a one-liner might be possible, I used the following tiny script:

```
#!/bin/sh

for x in \*
do
sed 's/\\\_log/\\.log/' $x > /tmp/tmpfile.tmp
mv /tmp/tmpfile.tmp $x
done

```