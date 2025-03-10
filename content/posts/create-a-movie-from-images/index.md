---
title: 'Create a Movie from Images'
date: 2009-06-01T20:30:00.002+10:00
draft: false
url: /2009/06/create-movie-from-images_6692.html
tags: 
- trash
- linux
- monitoring
- howtos
---

I've started leaving my webcam on as a motion detector to find out who is leaving the shopping cards on our lawn, and ultimately have found it useful to stitch the images together into a movie. There are several ways to do this - and my way maybe isn't the best - but it works for me.

  
  

I first installed and configured [motion](http://www.lavrsen.dk/twiki/bin/view/Motion/WebHome), which I've used for years. I then created a file in ~/.motion called motion.com:

$ cat ~/.motion/motion.conf

```
height 480
width 640
framerate 2

```  
  

By creating this file, it allows me to start motion without modifying the global motion.conf file permissions, or \*gasp\* running it under sudo. There are [lots of options](http://www.lavrsen.dk/foswiki/bin/view/Motion/ConfigFileOptions) you can put in your motion.com file.

With motion installed, and configured, now install mencoder.

I prefer to generate a seed file based on the creation date for each image. If you try to use mencoder with just a \*.jpg, it works, but my video jumped around.

```
$ pwd
/home/path/Desktop/motion
$ ls -rt \*.jpg > list.txt

```  
  

This list.txt file now has the filenames, in chronological order, ready for consumption. I create the video like so:

```
mencoder mf://@list.txt -o \`date +%G%m%d\`.avi -ovc lavc -lavcopts vcodec=mjpeg

```  
  

This will output a file with today's date in a few seconds. Remember, the \`'s are the key by the #1, not quotes.