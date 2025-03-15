---
title: 'Using Distcc'
date: 2008-01-01T21:30:00.002+11:00
draft: false
url: /2008/01/using-distcc_1425.html
tags: 
- distcc
- linux
- articles
- mapnik
---

I'm in the process of working on one of my projects, and the requirement came up to download a fairly large file (4GB). Since I only receive ~20GB/month at my house, I decided to just use my server in the U.S. The next requirement came about needing to compile Mapnik, which I had intended to do on the server at some point anyways, yet I ran into memory constraints.

Good old distcc comes to the rescue. I don't need to use distcc that often, yet when I do, it is very handy. However, I always forget to set g++ to use distcc as well. So, for when I forget next time...

```
DISTCC_HOSTS='home'
./configure
make CC=distcc CXX=distcc
```  
  

Maybe one of these days I'll write a more in depth tutorial for installing distcc, yet until then, you can [peruse the notes](http://wiki.vpslink.com/index.php?title=HOWTO:_Install/Configure_Distcc) I left on my VPS provider's wiki.