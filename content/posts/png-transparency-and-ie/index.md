---
title: 'PNG Transparency and IE'
date: 2007-05-07T20:30:00.002+10:00
draft: false
url: /2007/05/png-transparency-and-ie_2740.html
tags: 
- howtos
---

![I Hate IE!](http://media.kelvinism.com/images/freakingannoying.png)  
I've vowed to not use transparent PNGs until almost everybody has switched to IE7, where they are actually supported (despite being supported by every other major browser). I've done the hacks, and have had good results. I like using PNGs, I'll admit it. [Inkscape](http://www.inkscape.org/) exports them directly, however one slight problem: transparency still exists. This isn't really a problem since I'm not layering images, or is it?  
My initial assumption is that IE would simple pull the white background and everything would be dandy. Well, we all know what they say about assumptions.  
  
  
A few options exist:  

  
*   Convert them to GIFs
  
*   Try some sneaky PNG IE hack
  
*   Do a rewrite and send all IE6 traffic to download firefox. Err... Do a rewrite and send all IE6 traffic to download firefox
  
*   Open each in GIMP and add a white background
  
*   Use [ImageMagick](http://www.imagemagick.org/) and convert the background to white.

  
  
We have a winner! The problem is, for the life of me, I couldn't figure out a simple convert command to do this. The quick bash script would suffice:  
```
#/bin/bash
CONVERT=/usr/bin/convert
for image in \*.png; do
 $CONVERT -background white $image $image
 echo "Finished converting: $image"
done
```  
  
**Note:**This is gonna convert all PNGs.  
  
  
So, no the transparent GIFs have a "white" base layer, IE renders them fine, normal browswers render the images fine, and I'm allowed a cup of coffee. I hope this helps somebody, if so, leave a note!