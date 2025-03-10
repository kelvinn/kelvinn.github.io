---
title: 'IoT Foray with Sonoff S20 / IFTTT / Lambda / CloudMQTT'
date: 2018-05-26T14:08:00.002+10:00
draft: false
url: /2018/05/ys-and-i-recently-purchased-echo-from.html
tags: 
- iot
- articles
---

I recently purchased an Echo from Amazon, and we were contemplating how else to better integrate it with our somewhat minimalistic home. I thought it would be interesting to get it to link to a WiFi-enabled power outlet, but unfortunately they are pretty expensive in Australia.  
  
Then I stumbled across the [Sonoff](http://sonoff.itead.cc/en/) devices by Itead, and learned that they were somewhat hackable via a [custom firmware](https://github.com/arendst/Sonoff-Tasmota). Coincidentally I received the two devices on the same day my daughter was off sick, so when she had her nap, I got hacking.  
  
The first bottleneck was discovering that the units I received did not have any headers. A little quick soldering later, and we had headers.  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjzXxcHLSh3p-9YEHjtC6rnj6mJO17whJj92HUsJts2ZxD9umE7b7Rb-KUL6yFe2Ppu3ckOaoFhBmDr5yX915j97AKICugRNSOTQ-RI9dK90n6zR9J_0HnftlSFtzP-tXW0o7Q0pCrdWL1K/s640/20180502_200103.jpg)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjzXxcHLSh3p-9YEHjtC6rnj6mJO17whJj92HUsJts2ZxD9umE7b7Rb-KUL6yFe2Ppu3ckOaoFhBmDr5yX915j97AKICugRNSOTQ-RI9dK90n6zR9J_0HnftlSFtzP-tXW0o7Q0pCrdWL1K/s1600/20180502_200103.jpg)

No headers mom :(

  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgxcIKHmY3Z3RMOShYMEGg92Tyd9QG6ENDpfn7QiDMiUtLbWhkm8smrsGYHTc7wNlkGv0f8T760LOqsISTPu7XEVetkuuIuzGOpqWQkjFOmUVo8mAyMBFju8GHWN-VLs1mCPzvdpNogJhd9/s640/20180502_163741.jpg)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgxcIKHmY3Z3RMOShYMEGg92Tyd9QG6ENDpfn7QiDMiUtLbWhkm8smrsGYHTc7wNlkGv0f8T760LOqsISTPu7XEVetkuuIuzGOpqWQkjFOmUVo8mAyMBFju8GHWN-VLs1mCPzvdpNogJhd9/s1600/20180502_163741.jpg)

Now we have headers!

A few notes of warning: the $2 programmer I got from AliExpress has 3.3v and 5v, but the _output_ is 5v. I'm glad I measured it with my multimeter, and used a random 3.3v breadboard supply instead.  
  
In hindsight I wish I had just purchased the [FTDI programmer](https://www.itead.cc/foca.html) from Itead. It looks pretty neat.  
  
After following the rest of the Tasmoto [hardware instructions](https://github.com/arendst/Sonoff-Tasmota/wiki/Sonoff-S20-Smart-Socket), and then the [PlatformIO instructions](https://github.com/arendst/Sonoff-Tasmota/wiki/Upload), I was able to successfully flash both my units with the custom firmware.  
  
I then created a Lambda function that sends a signal to CloudMQTT, and connected the two devices.  
  
Voila!