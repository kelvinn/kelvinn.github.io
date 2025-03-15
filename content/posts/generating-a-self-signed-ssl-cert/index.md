---
title: 'Generating a Self-Signed SSL Cert'
date: 2007-05-11T20:30:00.002+10:00
draft: false
url: /2007/05/generating-self-signed-ssl-cert_2490.html
tags: 
- howtos
---

I have the need to generate an SSL cert (Apache2) about once every 3 months. And since I'm cheap, I don't ever actually *buy* one, I just self-sign it. And every time I forget the commands needed. So, here they are, for my reference only.  
**1) Generate Private Key**  
  
```
openssl genrsa -des3 -out server.key 1024
```  
**2) Generate a CSR**  
  
```
openssl req -new -key server.key -out server.csr
```  
**3) Remove passphrase**  
  
```
cp server.key server.key.org
openssl rsa -in server.key.org -out server.key
```  
**4) Generate Self-Signed Cert**  
  
```
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
```