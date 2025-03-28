---
title: 'Reduce Bandwidth By Shrinking Images'
date: 2010-01-24T21:30:00.002+11:00
draft: false
url: /2010/01/reduce-bandwidth-by-shrinking-images_3510.html
tags: 
- imagemagick
- traffic
- bash
- howtos
---

A friend has a simple WordPress-based website that I set up for him a few year ago - and he likes to post a lot of images. For various reasons I have it hosted on my VPS in Australia, which only comes with 15GB of bandwidth, most likely because I got a crazy good deal on it.

The problem is, that isn't much bandwidth. Each page of his site was previously using almost 10MB of bandwidth per view - which meant the 15GB was running out. I deduced the high usage in Firebug and noticed it was *gasp* from large images, some almost 1MB large. The images on the server are contained in subdirectories under a gallery folder - and I wanted to resize them. What I actually wanted to do was:

  
  
1. If the image was over 1024x900, resize it.  
2. If the image size (bytes) was over X, lower the quality.  
  
  

I ended up using ImageMagick, which is what first obviously came to mind for image manipulation. While there is likely a better way to resize all the images, this is what I came up with. Maybe somebody else will find it useful too.

```bash
for dir in /home/vhosts/website.com/html/wp-content/gallery/*
do
cd $dir
for filename in *.jpg
do
echo Filename: "$filename"
width=`identify -ping -format %w "$filename"`
height=`identify -ping -format %h "$filename"`
if [ $width -ge 1024 -a $height -ge 900 ]; then
convert "$filename" -resize "%80>" "$filename"
echo New Dimensions: $width x $height
fi
filesize=`stat -c%s "$filename"`
if [ $filesize -ge 414981 ]; then
convert "$filename" -quality 90 "$filename"
echo Old Filesize: $filesize
echo New Filesize: `stat -c%s "$filename"`
fi
done
done

```  
  

Save it as "resize.sh" and run it with "bash resize.sh". The output:

```plain
Filename: img_5364.jpg
Old Filesize: 950748
New Filesize: 331426
Filename: img_5366.jpg
Filename: img_5367.jpg
Filename: 1c10_1.jpg
Filename: 1.jpg
Filename: 2752_1.jpg
Filename: 42920014.jpg
New Dimensions: 1544 x 1024
Filename: 42920017.jpg
New Dimensions: 1544 x 1024


```