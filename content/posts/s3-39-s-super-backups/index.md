---
title: 'S3 Super Backups'
date: 2007-01-22T21:30:00.004+11:00
draft: false
url: /2007/01/s3-super-backups_8294.html
tags: 
- backup
- articles
- amazon
---

My buddy [Ian](http://www.ianfitzpatrick.com/)  mentioned Amazon's S3 service, and the potential for using it for fun webapps.  While utilizing it for webapps will have to wait a few months, I was able to use it as a cheap backup for my home server (pictures, documents, etc,.) -- and my server that houses my email and websites.  The setup is pretty quick, and most of it can be detailed [here](http://blog.eberly.org/2006/10/09/how-automate-your-backup-to-amazon-s3-using-s3sync/).  The ruby package is [here](http://s3sync.net/)   I'll toss in my recommendation to use the [jets3t Cockpit](https://jets3t.dev.java.net/) application for viewing the buckets, especially considering the Firefox extension didn't work as advertised.  My only two comments will be this:  
  
1) Making sure SSL is working.  The site mentioned above just has you hunt down some random bash file, that isn't even hosted anymore.  On my Debian system I simply added this to my upload.sh:  
  
```bash
export SSL_CERT_DIR=/etc/ssl/certs/
```  
2) The second suggestion is another example of the s2sync layout.  Let's say you created the bucket "kelvinism" -- the following would move the documents inside a test folder from /home/kelvin named test to a folder named test in the kelvinism bucket.  Sweet.  
  
```bash
 s3sync.rb -r --ssl --delete /home/kelvin/test kelvinism:/test  
```