---
title: 'Tunneling over SSH'
date: 2007-06-07T20:30:00.005+10:00
draft: false
url: /2007/06/tunneling-over-ssh_6040.html
tags: 
- howtos
---

As a rule, whenever I'm online I'm logged into my server back in the States. I'm also usually wireless, which we all know is beyond insecure -- I've found it _especially_ useful to tunnel firefox over SSH. I try my best to tunnel stuff over SSH back, and if you want to also, this is how.  

#### Setup the SSH/SOCKS tunnel

I'm on Linux, so this is pretty darn easy.  
```bash
ssh user@domain.com -D 1080

```  
If the SSH daemon runs on a different port, you'd do something like this:  
```bash
ssh -oPort=1234 user@damon.com -D 1080

```  
Remember ports below 1024 are reserved, and you would need root access. Now it is time to configure the different programs to use the newly created tunnel.  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh5MWWeIZYH4RZuL3binMtkPHLDyvU5HRdNdJCtBdH5IYYrdEqk95ROxmFMKWJTjFxY267VFVw-_eohgpwD4K-RVRM4X9m80Mv1Gv6HxJJAO7T57eV7y_hZF_9RWEWKnDUp0d5pcr52Nq9S/s400/gnome-settings.jpg)](https://picasaweb.google.com/lh/photo/QH-jPk3gHgigKtmQcrhoig?feat=embedwebsite)

#### Setting up Gnome (optional)

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiRsef8lcC6qNZh2vdPbGZ1t8cL91ibwCeuHwy1hwZMlqQpNDKw7MRh7zBMmxvRfsFcL6iYe7xKv_Mdnqsn_394B_buuZlRoApNOT7z9vgwOChr6x2yByWue3Awgo-NHtPmI7aecOXTlg4F/s400/msn-settings.jpg)](https://picasaweb.google.com/lh/photo/USO3dEudCNgJGvNOh8IAQA?feat=embedwebsite)

#### Tunneling Pidgen

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi7xGVXjZDHSQlReX7mAad4ko6zk7Lf7JWyIe6TYj2yrIAk7L8jCpo0mypVrNP0DqU4OTPEPX2TuEbOo8ySZgdzkexVU7V_hnBguhfg_ACbXfjTM_KNvtdj-gLDmiqMzIoCpKEvYWXhifSN/s400/xchat-settings.jpg)](https://picasaweb.google.com/lh/photo/HX-kbMnfI3fwpbUyRf17FA?feat=embedwebsite)

#### Tunneling XChat

**Tunneling Firefox**  
_Note_: I'm going to list two examples, one is with FoxyProxy and the other is with the ordinary proxy settings.  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjGCLf_YOke30XnQgqrLAW_6aRGAm1INIHSEzcA7NZitNF4CMpOADpfBRmnhZ3UcLGhGNUiFj6BnJc66DDA8CnhE1GaSrh-mTFzFXXS7OsiviFdYNKH4o-yTnZIjl8hW4NMR4biKUvC0ws8/s400/foxyproxy-settings.jpg)](https://picasaweb.google.com/lh/photo/iKYUjPKEnU6WWq5ytUlftg?feat=embedwebsite)

#### FoxyProxy

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi3N60K_2L5EX61zgiQG42vWxG-0oiEU0gNQE_M5JYd9ulZBx9p-NW4jBmk6sRYPG4U4VQIOelYAktI3WPT1UGztDyAJ1jSEVAaHn1HBfzG-L-Mw-WyAIA53StGCrV8SoIAiYnk_VyiwNpJ/s400/firefox-settings.jpg)](https://picasaweb.google.com/lh/photo/gCoCFhGSNBf2T0vGhHoSrA?feat=embedwebsite)

#### Normal Proxy

_Make sure the other fields or empty, or you won't connect._  
  
So, there you have it. There are quite a few unix shell providers out there, I'm sure it wouldn't be too hard to spot a link for one. I've seen [QuadSpeedInternet](http://www.quadspeedi.net/?page=services) having SSH access for $3/month, and [JVDS](http://www.jvds.com/freeshells/) or [Lonestar](http://sdf.lonestar.org/) offering possible free shells. Alternatively, you could just get a _really_ inexpensive VPS at [VPSLink](http://www.vpslink.com/vps-hosting/) ($6-$8/month, but they often have 25% off discounts).