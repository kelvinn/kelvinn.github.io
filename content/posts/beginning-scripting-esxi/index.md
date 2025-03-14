---
title: 'Beginning Scripting ESXi'
date: 2009-01-06T21:30:00.002+11:00
draft: false
url: /2009/01/beginning-scripting-esxi_6126.html
tags: 
- esxi
- vmware
- scripting
- tips and tricks
- bash
- howtos
---

I'm not impressed too often with much software, especially the closed source kind. I find a leaning preference to all things FOSS. If I had a million dollars, I'd likely spend all day contributing to all the projects I wish I had time to contribute to. Regardless, there are a select few closed-source products that I believe are truly excellent. I mean, the type of software where you aren't asking "I wish this could do this" and start asking "I wonder what else this can do."

While I've played around with most types of virtualization out there (OpenVZ, Xen, V-Server, qemu...), I've really found a soft spot for VMWare.

Don't get me wrong, if I was going to host a heap of Linux web servers I would absolutely use Xen, but for a heterogeneous environment, I haven't used anything as easy as VMWare's products. Not that I judge a product by how easy it is to use, not by a long shot, but ease of use sure makes judging other factors easier.

Regardless, this isn't a post trumpeting VMWare. I just realized tonight that some of the VMs I have running don't need to be except for certain hours of the day, or if condition A is true. The first example is my backup mail server; I really don't need it even powered on unless my main server is down. The second example is my Server 2003 instance, which has VI3 on it; I don't need this running unless I'm asleep. One of the most useful resources I've seen for the vmrun command is over at [VirtualTopia](http://www.virtuatopia.com/index.php/Controlling_VMware_Virtual_Machines_from_the_Command_Line_with_vmrun) -- loaded with examples.

#### Turn off via time

  
  

On my "monitoring" instance, which is always up, I've decided to install the script that controls my VM. I've opted to use a soft shutdown.

  
192.168.0.10 = ESXi box  
  
datastore1 = name of datastore that hosts VMs  
  

```bash
#!/bin/sh
 
vmrun -t esx -h https://192.168.0.10/sdk -u root -p root_password stop "[datastore1] Server 2003 R2/Server 2003 R2.vmx" soft


```  

I have that saved in a file called **stop_2003.sh** in /opt/vmware/bin; make sure it isn't world readable. I also have a **start_2003.sh**:  
  

```bash
#!/bin/sh
 
vmrun -t esx -h https://192.168.0.10/sdk -u root -p root_password start "[datastore1] Server 2003 R2/Server 2003 R2.vmx"


```  

  
Next, edit root's crontab (crontab -e):  

```bash
# m h  dom mon dow   command
0 8 * * * /opt/vmware/bin/start_2003.sh
0 23 * * * /opt/vmware/bin/stop_2003.sh


```  
  

The conditional task is a tad bit more tricky, but just a tad. Ping won't do, since the mailserver could go down itself, so install nmap. Create a script:

```bash
#!/bin/bash

if nmap -p25 -PN -sT -oG - mail.kelvinism.com | grep 'Ports:.\*/open/' >/dev/null ; then
echo \`time\` >> mailserver.log
else
/opt/vmware/bin/start\_mail.sh
fi


```  

And sticking with our theme, **start\_mail.sh**:

```bash
#!/bin/sh

vmrun -t esx -h https://192.168.0.10/sdk -u root -p root\_password start "\[datastore1\] Mail Server/Mail Server.vmx"

```  
  

This of course changes the crontab entry to:

```bash
#!/bin/bash
 
if nmap -p25 -PN -sT -oG - mail.kelvinism.com | grep 'Ports:.*/open/' >/dev/null ; then
echo `time` >> mailserver.log
else
/opt/vmware/bin/start_mail.sh
fi


```  
  

So, that's it. detect\_port.sh is lacking any type of error detection or redundancy - if one packet/scan is dropped, the mail server will turn on. I'll re-work this at some point, but it works for now.

**Update**: Vmware has also released a decent blog entry about using vmrun: [on their blog](http://blogs.vmware.com/vix/2008/12/managing-vm-guests-using-vmrun.html).