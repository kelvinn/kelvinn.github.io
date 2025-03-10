---
title: 'Mapping Urban Density in Sydney'
date: 2013-07-20T00:34:00.001+10:00
draft: false
url: /2013/07/mapping-urban-density-in-sydney.html
tags: 
- postgis
- gis
- articles
- tilemill
---

Five years ago I started exploring different mapping technologies by detailing instructions on [installing Mapnik](http://www.kelvinism.com/2008/04/setting-up-mapnik-server-on-ubuntu_118.html) and [mod\_tile](http://www.kelvinism.com/2008/11/revised-modtile-install-howto_1369.html). Times have changed significantly in the last five years, and thanks a lot to the products offered by [MapBox](http://www.mapbox.com/). After playing with TileMill, MBTiles, Leaflet and UTFGrids, it is great how many annoyances have been fixed by MapBox. I find it enjoyable making maps now, as I no longer need to worry about patching code just to get it to run, or mucking about with oddities in web browser.  
  
Each night this week I have created a new map using Mesh Block spatial data from the Australian Bureau of Statistics (Mesh Blocks are the smallest area used when conducting surveys). I am thankful to live in a country that provides a certain amount of open data, and the ABS should be applauded for the amount of data they provide. They provide [spatial data](http://www.abs.gov.au/AUSSTATS/abs@.nsf/DetailsPage/1270.0.55.001July%202011?OpenDocument) about Mesh Blocks, as well as [population counts](http://www.abs.gov.au/AUSSTATS/abs@.nsf/DetailsPage/2074.02011?OpenDocument) for this spatial data. It is relatively easy to merge the two and then visualise them using TileMill.  
  
First up - population density of Sydney, i.e. persons reported to be living in each mesh block. Darker red indicates a higher population count.  
  
  
[View Full Screen](http://maps.kelvinism.com/syd_pop_density.html)  
  
I find it interesting to see how many people live in certain Mesh Blocks. You will notice that Mesh Blocks with high population levels tend to be nearer public transport - either major roads with frequent bus service, or train stations.  
  
We can look at the urban densities by determining dwellings per hectare, and do this per Mesh Block. The definition I used for urban densities comes from [Ann Forsyth](http://annforsyth.net/) in "Measuring Density: Working Definitions for Residential Density and Building Intensity" ([pdf](http://www.corridordevelopment.org/pdfs/from_MDC_Website/db9.pdf)). Ann discusses the need to consider net or gross densities, depending on the type of land use. At the Mesh Block level the land use type appears to be singular: Industrial, Parkland, Commercial, Residential, and Transport. Because the land use type was generally singular I have not adjusted to gross/net, but still used Ann's definitions of certain density bands:  

*   Very low density: 11 dw/ha
*   Low density: 11-22 dw/ha
*   Medium density: 23-45 dw/ha
*   High density: 45 dw/ha

"dw/ha" is dwellings per hectare. I decided to map the four density levels, which can be relatively easily achieved using TileMill. See below for an example.  
  
  
[View Full Screen](http://maps.kelvinism.com/syd_urban_density.html)  
  

You can zoom in and scroll over any Mesh Block in Sydney to find out more. Additional installation information on how I did this can be found on this special page: [Mapping Mesh Block Data](http://www.kelvinism.com/2013/07/mapping-mesh-blocks-with-tilemill.html).