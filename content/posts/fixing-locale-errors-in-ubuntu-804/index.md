---
title: 'Fixing locale errors in Ubuntu 8.04'
date: 2009-05-03T20:30:00.005+10:00
draft: false
url: /2009/05/fixing-locale-errors-in-ubuntu-804_7736.html
tags: 
- ubuntu
- linux
- locales
- tips
- howtos
---

I've hit this problem a few times, and figured I'd leave a note for myself how to fix it. Ubuntu 8.04 seems to hiccup sometimes (on a VPS) for generating the correct locales. In particular, I get this error, a lot:

```bash
perl: warning: Setting locale failed.
perl: warning: Please check that your locale settings:
LANGUAGE = (unset),
LC_ALL = (unset),
LANG = "en_US.UTF-8"
are supported and installed on your system.
perl: warning: Falling back to the standard locale ("C").


```  
  

Normally I just do 'dpkg-reconfigure locales', but with 8.04, this doesn't seem to do squat. The solution is to edit the **/var/lib/locales/supported.d/local** file, and insert the correct locales (it will normally not exist, so create it):

```bash
# cat /var/lib/locales/supported.d/local
zh_TW.UTF-8 UTF-8
zh_TW BIG5
zh_TW.EUC-TW EUC-TW
en_US.UTF-8 UTF-8
en_US ISO-8859-1
en_US.ISO-8859-15 ISO-8859-15


```bash

You can then do a 'dpkg-reconfigure locales' and they will be generated correctly. For a list of supported locales, try this:

```bash
cat /usr/share/i18n/SUPPORTED | grep US

```