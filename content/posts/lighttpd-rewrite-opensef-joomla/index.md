---
title: 'Lighttpd+Rewrite+OpenSEF+Joomla'
date: 2006-10-14T20:30:00.002+10:00
draft: false
url: /2006/10/lighttpdrewriteopensefjoomla_4861.html
tags: 
- howtos
---

For those of you not needing Apache and the whole kitchen sink, [insert reason here], Lighttpd is a very attractive contender. For me, it has a small memory footprint, which is highly appealing. However, getting SEO urls to work (i.e. utilizing rewrite), isn't too straightforward.  
Tada! A little research yields two helpful links: one at lighttpd.net regarding how to [use ModRewrite](http://trac.lighttpd.net/trac/wiki/Docs:ModRewrite) and [another](http://forum.j-prosolution.com/opensef-documentation/1484-opensef-lighttpd.html?highlight=lighttpd) showing how to slightly modify the .htaccess file used by OpenSEF and Apache.  
So...  
1) Flush/clear any caches available  
2) Make sure site is listed in OpenSEFs manager inside Joomla  
3) Make sure SEO is Enabled insided the Joomla 'Site Configuration'  
4) Change your host conditional statement so it matches this:  
```bash
$HTTP[\"host\"] =~ \"(^|\\.)yourdomainname\\.com$\" {
     server.document-root = \"/var/www/your/domainlocation/\"
     url.rewrite-once = (
          \"^images*\\.(jpg|jpeg|gif|png)\" => \"$0\",
          \"^/administrator.*$\" => \"$0\",
          \"^/mambots.*$\" => \"$0\",
          \"(/|\\.htm|\\.php|\\.html|/[^.]*)$\" => \"/index.php\"
     )
}

```

Clear your browser cache, and check it out. If it doesn't work, you can try to "Delete All" URLs inside OpenSEF, and then your site will rebuild as necessary. Another note, as you can maybe tell by the above ruleset: you can have rewrite ignore directories. Just include:  
  
  
```bash
\"^/directory.*$\" => \"$0\",
```