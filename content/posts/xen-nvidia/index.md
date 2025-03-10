---
title: 'Xen + nVidia'
date: 2006-11-02T21:30:00.003+11:00
draft: false
url: /2006/11/xen-nvidia_5527.html
tags: 
- projects
---

Status:  
  

I've played with quite a bit of virtualization, especially VMWare for ages. About eight months ago I started to play around with Xen, and got it to work great, except for the fact that the nvidia driver wouldn't work with the Xen kernel. That said, I'm gonna give another go.

Throughout senior high, and especially my last year, I managed to score a bunch of crappy motherboards and random parts and pieces. Six or so years later, my parents are _still_ finding old motherboards. Considering these computers were mainly P120s with 64-128 megs of RAM, they weren't so hot. What is one to do?

As you could guess, when I started university I had quite a few computers in my room. I had about three or so P120s (one in a hampster cage, don't ask), one AMD600, an AMD1ghz and one iBook (500 whooping mhz). Computers would die, get replaced, but overall they worked quite well. Considering almost all the computers ran Linux (the AMD1ghz also ran Windows -- to play games -- and the iBook sort of ran OSX -- and YDL), every system was quite happy. I had an OpenBSD box as my gateway. Life was good.

But now I don't like having five+ systems. Electricity alone is a strong factor, plus, I don't _really_ want to manage all those systems. Plus noise.

Because of this, I have two systems: my workstation/test lab, and my laptop. I hopefully will never need anything more. But, because of thise, I needed Xen to play nice with my Nvidia closed source driver -- which when I tested it eight months or so ago, it wasn't. Since then I have been using Linux-Vserver, and while it works great, my requirements have started to change.

Luckily Nvidia has released a few new updates, and a few hackers have patched the driver to include support for a xen-based kernel. Maybe I'll write up a tutorial at some point.

Since I've already done the creation of the doms before, and it is somewhat similar to Vserver, everything went smoothly. You can expect some fun screencasts and experiments in the near future.