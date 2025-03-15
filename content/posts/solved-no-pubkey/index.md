---
title: 'Solved: NO PUBKEY'
date: 2007-05-25T20:30:00.005+10:00
draft: false
url: /2007/05/solved-no-pubkey_625.html
tags: 
- howtos
---

I've received this error more than once, so I'm finally writing my notes how I solve it.  

#### Error message:

  
W: GPG error: http://security.debian.org stable/updates Release: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY A70DAF536070D3A1  
  
This really is just your standard don't-have-the-gpg-keys error. So, get'em -- take the last eight digits from the long NO_PUBKEY string **that is displayed on your computer**. If you are using Debian 4.0, the above key is likely correct; if you are using Ubuntu or another version of Debian, it will be wrong. (The last eight digits are used as an identifier at the keyservers). Then:  
```
gpg --keyserver subkeys.pgp.net --recv-keys 6070D3A1
gpg --export 6070D3A1 | apt-key add -
```  
  
Repeat if necessary. All done, just do an apt-get update and no more warning!