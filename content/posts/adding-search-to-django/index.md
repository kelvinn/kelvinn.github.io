---
title: 'Adding Search to Django'
date: 2007-06-03T20:30:00.008+10:00
draft: false
url: /2007/06/adding-search-to-django_6300.html
tags: 
- search
- django
- articles
---

This is fairly well documented in the Django docs, so I'll be brief. This is the the bit of search code I use in almost all of my Django sites, and it works great:  
```

def search(request):
    from django.db.models import Q
    q = request.GET.get("q", "")
    if q and len(q) >= 3:
        clause = Q(dirtword\_\_icontains=q)               \\
               | Q(description\_\_icontains=q)       \\
               | Q(tags\_\_name\_\_icontains=q)        
        site\_search = Dirt.objects.filter(clause).distinct()
    else:
        site\_search = Dirt.objects.order\_by('?')\[:100\]
    return list\_detail.object\_list(
        request              = request,
        queryset             = site\_search,
        template\_name        = "dirty/search.html",
        template\_object\_name = "dirty",
        paginate\_by          = 20,
        extra\_context        = {"q" : q},
    )  

```  
  
While this should be pretty self-explanatory, the process goes like this: q is taken from the GET request and if it is over three characters long, it is searched for in the dirtword column, through the description and also through the m2m relationship of tags\_\_name. Yup, it is pretty nifty to be able to access relationship in this way (tags\_\_name). You will notice that at the end of each search it says "\_\_icontains" -- this simply does a fuzzy search for the word. Once the queryset is created (the filter) I've added a .distinct() on the end --this prevents multiple rows from being returned to the template. If there isn't a search, or it isn't long enough, a random list will be returned.  
One thing I like to do is include the search as extra\_context -- this allows you to say something like "you've searched for..." at the top of your search. I couldn't imagine implementing a search feature as being any easier.