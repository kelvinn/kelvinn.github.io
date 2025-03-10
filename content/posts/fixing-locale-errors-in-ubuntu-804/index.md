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

```
perl: warning: Setting locale failed.
perl: warning: Please check that your locale settings:
LANGUAGE = (unset),
LC\_ALL = (unset),
LANG = "en\_US.UTF-8"
are supported and installed on your system.
perl: warning: Falling back to the standard locale ("C").

```  
  

Normally I just do 'dpkg-reconfigure locales', but with 8.04, this doesn't seem to do squat. The solution is to edit the **/var/lib/locales/supported.d/local** file, and insert the correct locales (it will normally not exist, so create it):

```
\# cat /var/lib/locales/supported.d/local
zh\_TW.UTF-8 UTF-8
zh\_TW BIG5
zh\_TW.EUC-TW EUC-TW
en\_US.UTF-8 UTF-8
en\_US ISO-8859-1
en\_US.ISO-8859-15 ISO-8859-15

```  

You can then do a 'dpkg-reconfigure locales' and they will be generated correctly. For a list of supported locales, try this:

```
cat /usr/share/i18n/SUPPORTED | grep US

```