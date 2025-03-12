---
title: 'Geocoding Photos (Mac)'
date: 2014-12-13T10:00:00.000+11:00
draft: false
url: /2014/12/geocoding-photos-mac.html
tags: 
- photography
- howtos
- mac
---

I've recently started using OSX (again), and am really enjoying it (again). One Windows-only tool that I found really useful is [Geosetter](http://www.geosetter.de/en/), which allows you to add geo coordinates into photos. There don't appear to be any free geocoding tools that work to my satisfaction to do this, so the next best thing was geocode like you would using Linux. Here's how.  
  
We're going to use the command line program [ExifTool](http://www.sno.phy.queensu.ca/~phil/exiftool/) (by Phil Harvey) to extract coordinates from a gpx file and embed them in a directory of images.  
  
Firstly, install exiftool using [brew](http://brew.sh/). Here's the command:  
  
```bash
brew install exiftool

```

Copy the gpx files into your image directory and initiate the sync with the geotag flag:  
  
```bash
exiftool -geotag=gpslog2014-12-10_212401.gpx ./

```  
It is possible to also specify multiple gpx files (e.g. multiple day trip):  
  
```bash
exiftool -geotag=gpslog2014-12-10_212401.gpx -geotag=gpslog2014-12-07_132315.gpx -geotag=gpslog2014-12-08_181318.gpx -geotag=gpslog2014-12-10_073811.gpx ./

```  
And finally, you can include a time offset with the geosync flag. For instance, I had an 11-hour (39600 seconds) difference due to a timezone hiccup with my new camera, so we can get rid of that:  
  
```bash
exiftool -geotag=gpslog2014-12-10_212401.gpx -geotag=gpslog2014-12-07_132315.gpx -geotag=gpslog2014-12-08_181318.gpx -geotag=gpslog2014-12-10_073811.gpx -geosync=39600 ./

```  
It will process the images, renaming the original with an ".original" extension, and give you a report at the end:  
  
```bash
1 directories scanned
193 image files updated
83 image files unchanged

```  
If your camera is set to GMT, then put all the GPX files in the same directory as the photos to geocode, and do this:  
  
```bash
TZ=GMT exiftool -geotag "\*.gpx" *.jpg

```  
For any additional manual geocoding I fallback on Picasa's Places [GeoTag](http://www.snafu.org/GeoTag/) to add the coordinates.  
  
If you have Lightroom, then try doing a search for a suitable ExifTool Lightroom plugin, as there seem to be a few.