---
title: 'A Division in 30 Days'
date: 2005-06-30T20:30:00.003+10:00
draft: false
url: /2005/06/a-division-in-30-days_9756.html
tags: 
- projects
---

Status:  ✅
  
On a Friday I was told we might purchase a division from another company. Monday I heard that we purchased the division, and that we needed to have a website taking orders and a call center, capable of handling 500+/day (and not short calls); by the end of the month. Not to mention that the products wouldn't even ship out of the same warehouse that held the call center, but a warehouse half-way across the country. And that a recall was occurring, which had additional requirements. On Tuesday the CEO, and my boss, left for Asia.

There are basically two of us that handle IT at this company, yet the "other half" of the IT department is in China working remotely and studying. So, the goal: take a small company handling almost solely distribute orders to a company that can handle 500+ lengthy calls a day, with an e-commerce website. And the recall, so we have to process, replace and ship these additional products.

With our timeline, requirements and goals laid out, we began putting this in motion.

The project required working all but one day for basically a month (including weekends, of course). Luckily another colleague at work (not in IT, but gets an IT award anyways) and I were able to team up and tackle the PBX. We immediately researched and brought in several PBX resellers, and eventually decided on an Avaya system. Naturally we dragged in a T1 (all voice, well, 23 b-channels and one d-channel). The installation is supposed to take up to a month, but our business partner stepped up and pushed Verizon to hurry up (in the end, we still had to wait for Verizon to finish their end of the connection, plus a delay to port the 800# over).

Next on the list was the physical wiring. Hiring somebody to come in and lay the network/telephone cables would have likely cost quite a bit, plus we were rushing to get things done. Having crimped way too much cat5 in my life, and my colleague having done some telephone wiring historically, we joined and spent a full Saturday laying 24 (really 48+, if so desired) drops from the POP to where the call center is to be arranged. The call center is to have 10 reps, so we terminated appropriately, tested, and tested again. The cable was pulled through the ceiling, enclosed in a 3" or so pipe, and terminated into a patch panel behind the call center, and again into a patch panel in the wiring rack (which lives in the "server room").

Since everybody has owned laptops before, and not needed a domain, we haven't used one (read: small company). But, with an immediate additional 15 or so people, here comes a DC. Since time is a a huge issue (we needed to do training well before the month switch over), I slapped together a PDC (a few gigs of RAM, RAID1, you get the point) -- and dropped in Windows 2003. About the same time I had 10 IBM systems from my contact at CDW rushed over to the call center. We went shopping for cubicles, and had 10 sets brought over. There goes Sunday. I configured the appropriate policies, setup logins, and training of the CSRs started without any major hitches. Since we had already put together their desks and chairs, their first task was to put together the actual cubicles (I was too busy working on the website to take part in this pleasure).

Next was the website. Since I wanted the change to be as transparent to the user as possible, I took the very unmaintained website, changed the backend to PHP (since that is what I know best, and it works just fine), setup e-commerce, and made sure to get SSL working (cert from NS/VS).

Last is the recall. Two issues surrounded this: first, to get shipped the replacement products that had already been requested, just not shipped (and the previous company had stopped shipping these products at least two months prior to our purchase, sometimes even up to five months). I setup a quick wizard for people to select the right product, and that wizard dumped into a database. Half-way across the country I set them up to connect via ODBC to the database, batch import and then batch print the orders. Everything went into the correct field, automatically calculated shipping, sent the customer and email, and printed off the shipping labels -- all with just a few clicks from the shipping people's standpoint. I must say, Worldship's ODBC support is very handy. A similar setup was done for any orders online, and any orders taken through the call center. Finally, for the recall I created a quick interfact "admin" page for the previous company to pull the status of orders, how many orders are pending, their tracking numbers, and the ability to export any of this (since they needed to be able to generate these reports).

All transfers done between the two sites are over a VPN, but just running off mediocre DSL lines. Upgrades to come shortly.

As a bonus, I setup Worldship to export all data back into the database. Then I created a quick page on the website that searched through all the exported data, and showed the status of your order (including tracking number). Problem is, the data is coming from several different sources (website, recall, call center), so the only way to search is by First/Last Name + Zip. Not ideal, but that is how it has to be.
