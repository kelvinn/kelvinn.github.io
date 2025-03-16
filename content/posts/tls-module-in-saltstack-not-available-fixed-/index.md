---
title: 'TLS Module In SaltStack Not Available (Fixed)'
date: 2014-05-07T12:50:00.003+10:00
draft: false
url: /2014/05/tls-module-in-saltstack-not-available.html
tags: 
- linux
- python
- howtos
- saltstack
---

I was trying to install [HALite](https://github.com/saltstack/halite), the WebUI for [SaltStack](http://www.saltstack.com/), using the provided instructions. However, I kept getting the following errors when trying to create the certificates using Salt:  
```bash  
'tls.create_ca_signed_cert' is not available.  
'tls.create_ca' is not available.
```

Basically, the 'tls' module in Salt simply didn't appear to work. The reason for this is detailed on [intothesaltmind.org](http://intothesaltmine.org/install_and_configure_halite_alpha_on_arch_linux.html):  
  
_Note: Use of the tls module within Salt requires the pyopenssl python extension._  
  
That makes sense. We can fix this with something like:  
```bash  
apt-get install libffi-dev  
pip install -U pyOpenSSL  
/etc/init.d/salt-minion restart
```

Or, better yet, with Salt alone:  
  
```bash
salt '*' cmd.run 'apt-get install libffi-dev'  
salt '*' pip.install pyOpenSSL  
salt '*' cmd.run "service salt-minion restart"
```

The commands to create the PKI key should work now:  
  
```bash
Created Private Key: "/etc/pki/salt/salt_ca_cert.key." Created CA "salt": "/etc/pki/salt/salt_ca_cert.crt."  
```