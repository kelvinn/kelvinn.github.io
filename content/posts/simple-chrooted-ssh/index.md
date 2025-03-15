---
title: 'Simple Chrooted SSH'
date: 2007-03-29T20:30:00.002+10:00
draft: false
url: /2007/03/simple-chrooted-ssh_6907.html
tags: 
- howtos
---

You might be asking: why would you want to chroot ssh? Why use ssh anyways? Here are the quick answers:  

  
*   **FTP usually isn't great**. Unless sent over SSL, all information is sent _cleartext_.
*   **SSH usually is much better**. SSH sends all data over an encrypted channel -- the main drawback is: you can often browse around the system, and if permissions aren't set right, read things you shouldn't be able to.
*   **Chroot'd SSH rocks**. The solution to both the above problems.  
  
  
So, let me tell a quick story.  
When I started uni in 2001 I was a nerd. Still a nerd, I guess. I was cramped in my apartment on campus with like 5 boxes, most of them old p100s running Linux or OpenBSD. Life was good.  
I started a CS degree (shifted into Business with a focus on IT), and we were told to use the school's main servers to compile our programs. The other interesting thing is that _all_ user accounts were visible when logged in via ssh -- but hey, that is just the nature of Linux. I knew this, but asked the head I.T. person "why don't you jail the connections?" He responded quickly telling me to go away.  
Well, shortly after making the comment (although solutions existed at the time being), pam-chroot was released. This is right about the time students figured they could spam everybody in the school, some 25,000 emails, quickly and easily -- 'cause all the accounts were displayed. Sweet -- now we can chroot individual ssh connections.  
This quick demo will be on Debian, we'll create a pretend user named "karl." (I'll assume you've already added the user before beginning these steps). Also, the jails will be in /var/chroot/{username}  

#### First: Install libpam-chroot and makejail

session required pam_chroot.so  
  
```bash
kelvin@server ~$ sudo apt-get install libpam-chroot makejail
```  
  

#### Second: makejail config file

  
  
Put the following in /etc/makejail/create-user.py:  
```python
#Clean the jail

cleanJailFirst=1
preserve=["/html", "/home"]
chroot="/var/chroot/karl"
users=["root","karl"]
groups=["root","karl"]
packages=["coreutils"]

```  
  
  
**Edit**: If you need to use SFTP also, try this config:  
  
  
```python
cleanJailFirst=1
preserve=["/html", "/home"]
chroot="/home/vhosts/karl"
forceCopy=["/usr/bin/scp", "/usr/lib/sftp-server", /
 "/usr/bin/find", "/dev/null", "/dev/zero"]
users=["root","karl"]
groups=["root","karl"]
packages=["coreutils"]

```  
  
As you'll see, there is a "preserve" directive. This is so that when you "clean" the jail (if you need to refresh the files, for instance), you won't wipe out anything important. I created an /html so that the user can upload their web docs to that file.  

#### Third: configure libpam_chroot

  
Add the following to /etc/pam.d/ssh:  
```bash
# Set up chrootd ssh

session required pam_chroot.so

```  
  

#### Forth: allow the actual user to be chrootd

  
Edit /etc/security/chroot.conf and add the following:  
```bash
karl /var/chroot/karl
```  
  

#### Fifth: create/chown the chroot'd dir

  
```bash
kelvin@server ~$ sudo mkdir -p /var/chroot/karl/home

kelvin@server ~$ sudo chown /var/chroot/karl/home

```  
  
Now you should be able to log in, via the new username karl.