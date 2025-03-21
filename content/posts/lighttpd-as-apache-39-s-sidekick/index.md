---
title: 'Lighttpd As Apache Sidekick'
date: 2006-12-12T21:30:00.002+11:00
draft: false
url: /2006/12/lighttpd-as-apache-sidekick_4400.html
tags: 
- howtos
---

So, you have a web server. So, you have PHP. So, you want to make it a little quicker? The following are a few ideas to let you do that. First, let me share my experiences.  
I have always been wondering "what would a digg do to my site." I mean, I don't run a commenting system, so I'm refering to just some article. Because I prefer to manage my own server, I have decided to use a VPS (Virtual Private Server) from [VPSLink](http://www.vpslink.com/). Before purchasing I searched around, read reviews, and finally tested it out. Liking what I tested, I stayed. However, since I just host a few 'play' sites (http/email/ftp), and a few sites for friends, I am not going to spend much money on a high-end plan. That leaves me with a little problem: how can I maximize what I've got?  
I've tried quite a few things. I finally ended up using Apache to handle php and [Lighttpd](http://www.lighttpd.net/) to serve all static stuff. So, how?  

#### Staticzerize A Page

One of the first things you will need to do is pull down a static copy of your page.  
  
  
```bash
 user@vps:~$ wget http://www.kelvinism.com/howtos/notes/quick-n-dirty-firewall.html 
```

That was easy enough. Next, let's create a directory for static pages.  

```bash
user@vps:~$ sudo mkdir /var/www/html/kelvinism/static
user@vps:~$ sudo mv quick-n-dirty-firewall.html /var/www/html/kelvinism/static/ 
```

Sweet. (This is assuming of course that the site's DirectoryRoot is /var/www/html/kelvinism). Next, Lighttpd.  

#### Lighttpd Configuration

  
  
Install Lighttpd however you [choose](http://trac.lighttpd.net/trac/wiki/TutorialInstallation). There are a few key changes to make in the configuration.  
First, change the directory for your base DocumentRoot. Next, change what ports the server will listen on.  
  
  
```bash
server.document-root = \"/var/www/html\"
## bind to port (default: 80)
server.port = 81
## bind to localhost (default: all interfaces)
server.bind = \"127.0.0.1\"
```  
  
Ok, Lighttpd is all done. Now just start her up, and move onto Apache.  
  
  
```bash
user@vps:/etc/lighttpd$ sudo /etc/init.d/lighttpd start 
```  
  

#### Master Configuration

Depending on your distro and what apache you installed, you might need to do this a little different. I will illustrate how to do it with the Apache package from the Debian repository. Let's activate the mod_proxy module.  
  
  
```bash
 user@vps:~$ sudo a2enmod
Password:
 Which module would you like to enable?
 Your choices are: actions alias asis auth_basic auth_digest authn_alias authn_anon authn_dbd authn_dbm authn_default authn_file authnz_ldap authz_dbm authz_default authz_groupfile authz_host authz_owner authz_user autoindex cache cern_meta cgi cgid charset_lite dav dav_fs dav_lock dbd deflate dir disk_cache dump_io env expires ext_filter file_cache filter headers ident imagemap include info ldap log_forensic mem_cache mime mime_magic negotiation php5 proxy proxy_ajp proxy_balancer proxy_connect proxy_ftp proxy_http rewrite setenvif speling ssl status suexec unique_id userdir usertrack version vhost_alias

 Module name? proxy_http
```  
  
If you are not using a system with a2enmod, you can edit your configuration by hand. Just insert the following into your apache2.conf or httpd.conf files:  
  
  
```bash
LoadModule proxy_module /usr/lib/apache2/modules/mod_proxy.so
LoadModule proxy_http_module /usr/lib/apache2/modules/mod_proxy_http.so 
```  
  
The actual location of the extension (\*.so) will vary depending on where you installed it. If you have tried this out and get forbidden errors, or it just simply isn't working, the reason is because the proxy modules isn't configured right. You will likely get an error like:  

```bash
 client denied by server configuration: proxy 
```  
  
To solve this, you need to edit /etc/apache2/mods-enabled/proxy.conf or your httpd.conf file.  
  
  
```bash
<IfModule mod_proxy.c>
   #turning ProxyRequests on and allowing proxying from all may allow
    #spammers to use your proxy to send email.
    ProxyRequests Off
    <Proxy \*>
        AddDefaultCharset off
        Order deny,allow
        Deny from all
        Allow from .kelvinism.com
    </Proxy>
    # Enable/disable the handling of HTTP/1.1 \\"Via:\\" headers.
    # (\\"Full\\" adds the server version; \\"Block\\" removes all outgoing Via: headers)
    # Set to one of: Off | On | Full | Block
    ProxyVia On
</IfModule>

```
Now, open up your httpd-vhosts.conf or httpd.conf or wherever your site configuration is stored, and add the following inside the `virtualhost` directive:  
  
```bash
#DocumentRoot is just for reference, I assume you know how to setup virtualhosts.

DocumentRoot /var/www/html/kelvinism/
ProxyRequests Off
ProxyPreserveHost On
ProxyPass /howtos/notes/quick-n-dirty-firewall.html http://127.0.0.1:81/kelvinism/stat ic/quick-n-dirty-firewall.html 
ProxyPass /images/ http://127.0.0.1:81/kelvinism/images/ 
ProxyPassReverse / http://127.0.0.1:81/kelvinism/
```  
  
As an alternative, you could use a rewrite rule.  
  
  
```bash
#DocumentRoot is just for reference, I assume you know how to setup virtualhosts.
DocumentRoot /var/www/html/kelvinism/
RewriteEngine On
RewriteRule ^/howtos/notes/quick-n-dirty-firewall\.html$
http://127.0.0.1:81/kelvinism/static/quick-n-dirty-firewall.html [P,L]
ProxyPass /images/ http://127.0.0.1:81/kelvinism/images/
ProxyPassReverse / http://127.0.0.1:81/kelvinism/
 
```  
  
So what this does is pass the page http://www.kelvinism.com/howtos/notes/quick-n-dirty-firewall.html through mod_proxy to Lighttpd. So, test it out, and you are all done!