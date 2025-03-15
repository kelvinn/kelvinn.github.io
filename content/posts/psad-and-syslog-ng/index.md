---
title: 'PSAD and Syslog-NG'
date: 2007-04-18T20:30:00.002+10:00
draft: false
url: /2007/04/psad-and-syslog-ng_7378.html
tags: 
- syslog
- articles
- IDS
- monitoring
---

I really like using PSAD, both on my server and my laptop. You never know where the mean people are. I also seem to use syslog-ng quite often, meanwhile PSAD seems oriented to syslog. This is fine, and I'm pretty sure the install.pl for the source built will configure syslog-ng.conf automatically. However, I almost always tend to stick with packages if I can -- if they are even remotely close to the current version.  
Anyways, if you need to get syslog-ng.conf configured for PSAD, this is what you need to do:  
Add this code to the "# pipes" section, maybe stick to keeping it alphabetical.  
```
destination psadpipe { pipe("/var/lib/psad/psadfifo"); };
```  
  
Next, go down a little to the "# filters" section, add this:  
```
filter f_kerninfo { facility(kern); };
```  
  
And finally in the last section, add this:  
```
log {
        source(s_all);
        filter(f_kerninfo);
        destination(psadpipe);
};
```  
  
Restart syslog-ng, and you are good to go. Cheers to Michael Rash at [Cipherdyne](http://www.cipherdyne.org/psad/) for his work on PSAD.