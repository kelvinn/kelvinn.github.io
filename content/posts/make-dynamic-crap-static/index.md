---
title: 'Make Dynamic Sites Static'
date: 2006-12-07T21:30:00.002+11:00
draft: false
url: /2006/12/make-dynamic-sites-static_7513.html
tags: 
- howtos
---

Let's say one page on your site is getting hit hard. And I mean, it was digg'd or something. If the page resides on some CMS or blog, and each request is being processed by PHP and resulting in requests to your database, which, as they say, crap is gonna hit the fan. Well, at least if you're cheap like me, you'll try to squeeze every penny out of what you've got.  
That said, mod_rewrite comes to the rescue.  
There are only a few modifications that you need to do. The first is to ensure that mod_rewrite is enabled. If you have apache installed on debian, this might do:  
  
```bash
user@vps:~$ sudo a2enmod
Password:
Which module would you like to enable?
Your choices are: actions alias asis auth_basic auth_digest authn_alias authn_anon authn_dbd authn_dbm authn_default authn_file authnz_ldap authz_dbm authz_default authz_groupfile authz_host authz_owner authz_user autoindex cache cern_meta cgi cgid charset_lite dav dav_fs dav_lock dbd deflate dir disk_cache dump_io env expires ext_filter file_cache filter headers ident imagemap include info ldap log_forensic mem_cache mime mime_magic negotiation php5 proxy proxy_ajp proxy_balancer proxy_connect proxy_ftp proxy_http rewrite setenvif speling ssl status suexec unique_id userdir usertrack version vhost_alias
Module name? rewrite 
```  
  
Otherwise, you'll need to drop the following in your apache2.conf (or httpd.conf).  
  
```bash
LoadModule rewrite_module /usr/lib/apache2/modules/mod_rewrite.so
```  
Next, grab the page that is getting hit hard from your site.  
  
  
```bash
user@vps:~$ wget http://www.kelvinism.com/stuff/hit-hard.html
```  
Next, let's create a static directory and move that page into it.  
  
  
```bash
user@vps:~$ sudo mkdir /var/www/html/kelvinism/static
user@vps:~$ sudo mv hit-hard.html /var/www/html/kelvinism/static/
```  
  
Coolio. Now we'll rewrite the normal URL (the one being hit hard) to the static URL.  
If you have full access to the server, just mimic the following to a VirtualHost:  
  
  
```bash
<VirtualHost *>
    DocumentRoot /var/www/html/kelvinism
    ServerName www.kelvinism.com
    ServerAlias kelvinism.com www.kelvinism.com
<Directory \"/var/www/html/kelvinism\">
    Options Indexes -FollowSymLinks +SymLinksIfOwnerMatch
    allow from all
    AllowOverride None
    RewriteEngine On
    RewriteRule ^stuff/hit-hard\\.html$ /static/hit-hard.html [L]
</Directory>
</VirtualHost>
```  
  
If you don't have access to the server, you can just add the following to a .htaccess file:  
  
  
```bash
RewriteEngine On
RewriteRule ^stuff/hit-hard\\.html$ /static/hit-hard.html [L]
```
Sweet.