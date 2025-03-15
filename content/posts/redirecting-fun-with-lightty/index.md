---
title: 'Redirecting Fun with Lightty'
date: 2008-04-23T20:30:00.002+10:00
draft: false
url: /2008/04/redirecting-fun-with-lightty_330.html
tags: 
- articles
- lighttpd
- doh
- web
---

Two of my colleagues were having just a little bit [too much fun](http://www.kelvinism.com/blog/Australia/i-caught-fish/#c1926) with my blog, so I decided to have some fun back. Over a period of 10 minutes, they managed to leave 10+ comments. Luckily I have full control over my server, and was able to quickly create my practical joke.

```
$HTTP["remoteip"] == "123.45.678.910" {
url.redirect = (
"^/(.*)" => "http://www.urbandictionary.com/define.php?term=annoying+fuck",
"" => "http://www.urbandictionary.com/define.php?term=annoying+fuck",
"/" => "http://www.urbandictionary.com/define.php?term=annoying+fuck"
)
}

```