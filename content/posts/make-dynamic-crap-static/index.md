---
title: 'Make Dynamic Crap Static'
date: 2006-12-07T21:30:00.002+11:00
draft: false
url: /2006/12/make-dynamic-crap-static_7513.html
tags: 
- howtos
---

Let's say one page on your site is getting hit hard. And I mean, it was digg'd or something. If the page resides on some CMS or blog, and each request is being processed by PHP and resulting in requests to your database, crap is gonna hit the fan. Well, at least if you're cheap like me, you'll try to squeeze every penny out of what you've got.  
That said, mod\_rewrite comes to the rescue.  
There are only a few modifications that you need to do. The first is to ensure that mod\_rewrite is enabled. If you have apache installed on debian, this might do:  
  
```
user@vps:~$ sudo a2enmod
Password:
Which module would you like to enable?
Your choices are: actions alias asis auth\_basic auth\_digest authn\_alias authn\_anon authn\_dbd authn\_dbm authn\_default authn\_file authnz\_ldap authz\_dbm authz\_default authz\_groupfile authz\_host authz\_owner authz\_user autoindex cache cern\_meta cgi cgid charset\_lite dav dav\_fs dav\_lock dbd deflate dir disk\_cache dump\_io env expires ext\_filter file\_cache filter headers ident imagemap include info ldap log\_forensic mem\_cache mime mime\_magic negotiation php5 proxy proxy\_ajp proxy\_balancer proxy\_connect proxy\_ftp proxy\_http rewrite setenvif speling ssl status suexec unique\_id userdir usertrack version vhost\_alias
Module name? rewrite 
```  
  
Otherwise, you'll need to drop the following in your apache2.conf (or httpd.conf).  
  
```
LoadModule rewrite\_module /usr/lib/apache2/modules/mod\_rewrite.so
```  
Next, grab the page that is getting hit hard from your site.  
  
  
```
user@vps:~$ wget http://www.kelvinism.com/stuff/hit-hard.html
```  
Next, let's create a static directory and move that page into it.  
  
  
```
user@vps:~$ sudo mkdir /var/www/html/kelvinism/static
user@vps:~$ sudo mv hit-hard.html /var/www/html/kelvinism/static/
```  
  
Coolio. Now we'll rewrite the normal URL (the one being hit hard) to the static URL.  
If you have full access to the server, just mimic the following to a VirtualHost:  
  
  
```
<VirtualHost \*>
    DocumentRoot /var/www/html/kelvinism
    ServerName www.kelvinism.com
    ServerAlias kelvinism.com www.kelvinism.com
<Directory \\"/var/www/html/kelvinism\\">
    Options Indexes -FollowSymLinks +SymLinksIfOwnerMatch
    allow from all
    AllowOverride None
    RewriteEngine On
    RewriteRule ^stuff/hit-hard\\\\.html$ /static/hit-hard.html \[L\]
</Directory>
</VirtualHost>
```  
  
If you don't have access to the server, you can just add the following to a .htaccess file:  
  
  
```
RewriteEngine On
RewriteRule ^stuff/hit-hard\\.html$ /static/hit-hard.html \[L\]
```Sweet.