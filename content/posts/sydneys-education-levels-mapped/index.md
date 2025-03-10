---
title: 'Sydney''s Education Levels Mapped'
date: 2013-09-08T10:45:00.001+10:00
draft: false
url: /2013/09/sydneys-education-levels-mapped.html
tags: 
- postgis
- gis
- articles
---

I was talking to a friend about what education levels might look like across Sydney, and a friend challenged me to map it. The below map is my first draft.  
  
The map was derived by combining three datasets from the Australian Bureau of Statistics ([ABS](http://www.abs.gov.au/) - a department releasing some great datasets). The first dataset was the spatial data for "SA2" level boundaries, the second the population data for various geographic areas, and the third from the 2011 Census on Non-School Qualification Level of Education (e.g. Certificates, Diplomas, Masters, Doctorates). I aggregated all people with bachelors or higher in an SA2 region, and then divided that number by the total number of people in that region. A different methodology could have been used.  
  
**EDIT**: I should have paid more attention to mapping education levels. I mapped the percentage of overall population, but should have mapped the percentage of 25 to 34 year olds, as this would have aligned to various government metrics.  
  
Reported education levels differ vastly by region, e.g. "North Sydney - Lavender Bay" (40%) vs. "Bidwell - Hebersham - Emerton" (3%). It is interesting to look at the different [urban density levels](http://www.kelvinism.com/2013/07/mapping-urban-density-in-sydney.html) of the areas, as well as the [commute times to the nearest centre](http://www.kelvinism.com/2013/08/sydney-commute-times-mapped-part-2.html).  
  
Without trying to sound too elitist, I was hoping to use this map to guide me where to consider buying our next property (i.e. looking for a well educated, clean area with decent schools and frequent public transport). It was interesting to discover that the SA2 region we currently live in has the second highest percentage in NSW.  
  
Feel free to take a [look at the aggregated data](https://docs.google.com/spreadsheet/pub?key=0Ak3XfQfX87ELdEJRYVhIYlFRUGRZaDhQel9sbXlHY0E&output=html) yourself or [download it](https://docs.google.com/spreadsheet/pub?key=0Ak3XfQfX87ELdEJRYVhIYlFRUGRZaDhQel9sbXlHY0E&single=true&gid=0&output=csv) (attribution to ABS for source datasets).  
  
  
[View Full Screen](http://maps.kelvinism.com/sydney_educated.html)