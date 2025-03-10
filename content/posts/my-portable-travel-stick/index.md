---
title: 'My Portable Travel Stick'
date: 2007-06-29T20:30:00.006+10:00
draft: false
url: /2007/06/my-portable-travel-stick_1543.html
tags: 
- articles
- taiwan
- tips and tricks
- travel
---

This will be my last post from Taiwan, and I'm placing it in my tech section. Shortly I will be flying to Hong Kong, and then traveling into China. I'm not bringing my laptop with me. I'm always a little wary of using public computers, especially in many of the poorly run internet cafes. Often the logged in user is the administrator, and we all know the computers are obviously crawling with worms and keyloggers. What can I do?  
  
My partner kindly gave me a 128MB flash disk, which is perfect for what I want to do. I've installed the following applications to run directly from it:  

  
*   **[Portable Clamwin](http://portableapps.com/apps/utilities/clamwin_portable)** - I plan to fire it up and do a memory scan before I start typing any passwords.
  
*   **[Portable Putty](http://portableapps.com/apps/internet/putty_portable)** - This is useful for two reasons. Firstly, in case my server (or any server with SSH) needs help, I'm on it. Secondly, and more importantly, for security. Putty can easily be used as a SOCKS5 proxy over SSH, so I can tunnel Firefox and IM securely. Password sniffers, be gone! A side benefit is the ability to bypass the "Great Firewall", if needed (e.g. the block my Google account).
  
*   **[Portable Miranda](http://portableapps.com/apps/internet/miranda_portable)** - In case I'm feeling home sick, or have some crazy desire to talk on IRC. Don't count on it.
  
*   **Firefox** - I tried the Portable Apps package, yet it didn't work.

  
I noticed in the "known issues" that it doesn't work if loaded on a drive with a non-asci path, which this machine (and those in China) usually have. The "resolution" is to run it in Win98 compat mode, but this didn't work for me. To get around this, I downloaded the normal Firefox, installed it, copied the contents of "Mozilla Firefox" and dumped it in /Firefox. Then I created a profile directory called /FFProfile, and created a bat file called "firefox.bat":  
```
start \\Firefox\\firefox.exe -profile \\FFProfile
```  
  
Double click the bat file, and you have FF running on your usb drive.  
I'm in a search for a better keylogger detector, as I don't know how complete ClamAV will be. If you know of one, let me know. Until then, I'm going to pretend I have the perfect traveling USB companion.