---
title: 'Postfix/Dovecot + MySQL'
date: 2007-05-24T20:30:00.005+10:00
draft: false
url: /2007/05/postfixdovecot-mysql_1687.html
tags: 
- howtos
---

As you can see by [another post](http://www.blogger.com/tech-blog/gentoo-test/), I decided to reinstall the server. This isn't really a problem, I have pretty good backups. I've installed apache and friends a bagillion times. However, Postfix(chroot)+Dovecot authenticating from MySQl, that doesn't install quite so smoothly.  
Just for my future reference, and maybe helpful for somebody, someday. Clearly not a tutorial. The postfix chroot = /var/spool/postfix  

#### cannot connect to saslauthd server: No such file or directory

  
  
First, get the saslauthd files into the postfix chroot. Edit /etc/conf.d/saslauthd (or /etc/default/saslauthd), and add this:  
```
SASLAUTHD\_OPTS="-m /var/spool/postfix/var/run/saslauthd"
```  
  
Second, add it to the init script.  
```
stop() {
        ebegin "Stopping saslauthd"
        start-stop-daemon --stop --quiet /
--pidfile /var/spool/postfix/var/run/saslauthd/saslauthd.pid
        eend $?
}
```  
  
Third, maybe, change /etc/sasl2/smtpd.conf (or /etc/postfix/sasl/smtpd.conf) and add this:  
```
saslauthd\_path: /var/run/saslauthd/mux
```  
  
Ok, that error should go away now.  

#### Recipient address rejected: Domain not found;

  

#### (Host or domain name not found. Name service error for name=_domain.com_

  
  
These are actually the same type of error. Copy /etc/resolv.conf into the chroot.  

#### fatal: unknown service: smtp/tcp

  
  
Copy /etc/services into the chroot.  
I searched google for these answers, to a certain degree at least, but couldn't really find much. Then I remembered "crap, this is a chroot, it needs things" -- and fixed stuff. If you came here from google, and these super quick notes were helpful, feel free to leave a comment, or contact me directly if you have any questions.