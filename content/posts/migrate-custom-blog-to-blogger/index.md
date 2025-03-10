---
title: 'Migrate Custom Blog to Blogger'
date: 2013-01-10T20:14:00.000+11:00
draft: false
url: /2013/01/migrate-custom-blog-to-blogger.html
tags: 
- django
- python
- google
- howtos
---

For the last ten years I have run this website from various systems. First it was on Wordpress, then Mambo, then Joomla, and since early 2006 it has been running on custom code written using Django. I used this site as a learning tool for Django, re-wrote it after gaining more knowledge of Django, and then re-wrote it again when Google released App Engine. However, I recently realised that for the last few years I have spent more time writing little features than actually writing. I have entire trips that I never wrote because I was too busy writing code.  
  
This week it all changed. I did the unthinkable. I moved this website to Blogger.  
  
After evaluating some of the features of blogger, i.e. custom domains, location storing, ability to filter on labels, custom HTML/CSS, great integration with Picasa, and their mobile app, I realised I could virtually replace everything I had previously custom made.  
  
This post gives a technical description how to migrate a site running Django, but readily applies to any blog running on custom code. I initially spent a fair bit of time trying to figure out how to convert my existing RSS feed into something Blogger could accept, but every solution required troubleshooting. I soon remembered why I love Django so much, and that it would be trivial to generate the correct XML for import.  
  
1) **Create Blogger Template**  
I wanted to keep my design, so I hacked it to support Blogger. Take one of the existing templates, edit the HTML, and adjust it for your design. If you've worked with templates before this shouldn't be too difficult.  
  
2) **Generate Sample XML**  
The first step was to generate a sample XML file from Blogger to see what would be needed for import. Create a sample post with a unique name and a few labels, and location. In Blogger, go to Settings->Other and click Export Blog. The first 90% of the file will be for your template and other settings, but eventually you will find a section with <entry> elements in it. Copy this sample element out - this will become your template.  
  
3) **Format Template**  
Using the sample section from the blog export, format it so the view you will create populates it correctly. A note of caution: the template needs time in ISO 8601 format, you need the <id> element, and the location element needs coordinates if there is a name. It won't import later if there is a name with no coordinates. My template looks like this:  

#### feeds/rss.html

```
{%  load blog\_extras %}
{% for entry in entries %}
    tag:blogger.com,1999:blog-1700991654357243752.post-{% generate\_id %}
        {{ entry.publish\_date|date:"Y-m-d" }}T10:30:00.000123
        {{ entry.publish\_date|date:"Y-m-d" }}T10:30:00.000123
        {% for tag in entry.tags %}
            {% endfor %}

        {{ entry.title }}
        {{ entry.content }}

        

        Joe Bloggs
            https://plus.google.com/12345689843655881853
            kelvin@example.com 
{% endfor %}

```  
This isn't really RSS, so if you are pedantic you can name it something else. You will notice I loaded some template tags in there ("blog\_extras"). This is for generating the random number, as this is needed for the ID element.. Here's the template tag.  

#### blog\_extras.py

```
\# 'import random' at beginning of file
def generate\_id():
    id = ""
    for x in xrange(1, 7):
        id = id + str(int(random.uniform(400, 900)))
    id = id + "8"
    return {'obj': id}
register.inclusion\_tag('blog/generate\_id.html')(generate\_id)

```  

#### /blog/generate\_id.html

```
{{ obj }}

```  
4) **Create Code To Populate View**  
This section should be easy if you have written your blog in Django. Simply populate the template, what I have shown as "rss.html" above  

#### blog/views.py

```
def show\_rss(self):
    q = Entry.all()
    q = q.filter("genre !=", "blog")
    entries = q.fetch(500)
    return render\_to\_response("feeds/rss.html", {
        'entries': entries,
        }, mimetype='text/plain')

```  
I did a filter on the model to not include "blog" entries - these are my travel stories, and I exported them separately. Remember that this is all happening on App Engine, so you will need to adjust if using Django's normal ORM.  
  
5) **Download Entries**  
Visit the URL you mapped to the "show\_rss" function in urls.py, it should generate your list of entries. Copy and paste those entries into the exported XML from Blogger where you took out the original <entry> element.  
  
6) **Import Entries**  
Now go to Blogger and import your blog. With any luck you will have imported all your entries. You will probably need to do this a few times as you tweak the text. I had to remove some newlines from my original posts.  
  
**Optional Steps**  
  
7) **Create Redirect URLS**  
Links in Blogger appear to only end in .html, which is a problem for links coming from Django. Luckily, Blogger includes the ability to add redirects. Go to Settings->Other-Search Preferences. You can then edit redirects there. I generated a list of my old URLs and combined that with a list of the new URLs. Hint: you can use Yahoo Pipes to extract a list of URLS from a RSS feed. If you open any of the links in Excel and split on forward slashes, remember that it will cut off leading zeros. Set that field to TEXT during import.  
  
I decided not to create redirects for every entry, as I didn't really have time, and it only probably matters if somebody links directly to that page. I opened Google Analytics and looked at the Search Engine Optimisation page and sorted it by the most used inbound links. After getting down to entries that only had 1 inbound request per month I stopped creating redirects.  
  
8) **Host Stylesheets and Images Externally**  
Blogger won't host host files, so you need to work around this problem. All my images are generally from Picasa, except very specific website related ones. I moved those to Amazon's S3 and updated the links. I did the same with my CSS. You could probably store them in Google Storage, too.  
  
9) **Create Filters on Labels**  
If you had any previous groupings you can still link to them using label searches (in my case I actually added the "genre" as a label). The syntax is "/search/label/_labelname_/", as you can see in my [howtos section](http://www.kelvinism.com/search/label/howtos/) link.  
  
10) **Update Webmaster Tools**  
If your site is part of Google's Webmaster Tools, you will want to login and take a look that things are OK. You will also probably want to update your sitemap (send Google your atom.xml feed).