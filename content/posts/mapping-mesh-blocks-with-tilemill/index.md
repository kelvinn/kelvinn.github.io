---
title: 'Mapping Mesh Blocks with TileMill'
date: 2013-07-20T02:00:00.000+10:00
draft: false
url: /2013/07/mapping-mesh-blocks-with-tilemill.html
tags: 
- postgis
- gis
- tilemill
- howtos
---

This quick tutorial will detail how to prepair the ABS Mesh Blocks to be used with MapBox's TileMill. Beyond scope is how to install postgresql, postgis and TileMill. There is a lot of documentation how to do these tasks.  
  
First, we create a database to import the [shapefile](http://www.abs.gov.au/AUSSTATS/abs@.nsf/DetailsPage/1270.0.55.001July%202011?OpenDocument) and [population data](http://www.abs.gov.au/AUSSTATS/abs@.nsf/DetailsPage/2074.02011?OpenDocument) into:  
  
  
Using 'psql' or 'SQL Query', create a new database:  
  
```sql
CREATE DATABASE transport WITH TEMPLATE postgis20 OWNER postgres;
# Query returned successfully with no result in 5527 ms.
```  
It is necessary to first import the Mesh Block spatial file using something like PostGIS Loader.  
  
![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi8zpIUCky4eqQcl82ds0um_KZvlqepw11Svcc5SnyMT24IBX8O9ZTIurIyzM0nNivejDs3uiPyoejPNuxpuVcMgf45IY7xYb6FmtcCUG9TbTxCDiq2feCnileNBwms5M8PrEDjhP7DRtvG/s640/PostGISLoader2.png)  
  
We then create a table to import the Mesh Block population data:  
  
```sql
CREATE TABLE tmp_x (id character varying(11), Dwellings numeric, Persons_Usually_Resident numeric);
```  
And then load the data:  
  
```sql
COPY tmp_x FROM '/home/kelvinn/censuscounts_mb_2011_aust_good.csv' DELIMITERS ',' CSV HEADER;
```  
It is possible to import the GIS information and view it in QGIS:  
  
![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEir_OlfVmY_FZjQGoh_UdIr2wVe1xsNQLDzYH6M5gX5V5a-lknehk_lDEuhaZUC9tqwcoKHoKCv9KLLSSmlcqU5sX89jkJzne-FHgQYQUML9KwGoCoAQEa8DEOHuI3KA4qDq7n4kWtUbvC3/s640/qgis.png)  
  
Now that we know the shapefile was imported correctly we can merge the population with spatial data. The following query is used to merge the datasets:  
  
```sql
UPDATE mb_2011_nsw
SET    dwellings = tmp_x.dwellings FROM tmp_x
WHERE  mb_2011_nsw.mb_code11 = tmp_x.id;

UPDATE mb_2011_nsw
SET    pop = tmp_x.persons_usually_resident FROM tmp_x
WHERE  mb_2011_nsw.mb_code11 = tmp_x.id;

```  
We can do a rough validation by using this query:  
  
```sql
SELECT sum(pop) FROM mb_2011_nsw;
```  
And we get 6916971, which is about right (ABS has the 2011 official NSW population of 7.21 million).  
  
Finally, using TileMill, we can connect to the PostgGIS database and apply some themes to the map.  
  
```bash
host=127.0.0.1 user=MyUsername password=MyPassword dbname=transport
(SELECT * from mb_2011_nsw JOIN westmead_health on mb_2011_nsw.mb_code11 = westmead_health.label) as mb


```  
![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEheoXfae5qm5A8jKuBJg99a2zR_idp0NTWM3I40Belyi1GIwvM-kzHSOBbYd1rHEouJon19thdULDYo_GVKdZDMCF2JJ51iR6xc9JNdOw-K5dubGsvK32IXrLMGe2WUlxBWnALGhsV4ZlOK/s640/tilemill_1.png)  
  
![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgMEZ7vsutC7RO2T4jT78IIxxKpW4wVrk3Mokfgb9SqTXWQ7dt4Gysc5C03y6IZC7_IPRbzx0wjSBxgRrR5yapT-H3AGJL7a4jY3nsXeMeR8aVdR0o39Gkobs361WOckKzzK4_56_5j-9M7/s640/tilemill_2.png)  
  
After generating the MBTiles file I pushed it to my little $15/year VPS and used [TileStache](http://tilestache.org/) to serve the tiles and UTFGrids. The TileStache configuration I am using looks something like this:  
  
```json
{
  "cache": {
    "class": "TileStache.Goodies.Caches.LimitedDisk.Cache",
    "kwargs": {
        "path": "/tmp/limited-cache",
        "limit": 16777216
    }
  },
  "layers": 
  {
    "NSWUrbanDensity":
    {
        "provider": {
            "name": "mbtiles",
            "tileset": "/home/user/mbtiles/NSWUrbanDensity.mbtiles"
        }
    },
    "NSWPopDensity":
    {
        "provider": {
            "name": "mbtiles",
            "tileset": "/home/user/mbtiles/NSWPopDensity.mbtiles"
        }
    }
  }
}

```