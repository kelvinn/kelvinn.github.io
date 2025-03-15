---
title: 'Django Newforms Usage in Colddirt'
date: 2007-06-01T20:30:00.004+10:00
draft: false
url: /2007/06/django-newforms-usage-in-colddirt_1103.html
tags: 
- django
- articles
- colddirt
- newforms
---

I hear many complaints and questions about newforms, but I've personally found it rather easy and logical to use. There are numerous ways for you to use do forms in Django, and most likely the best way to see them all is to [read the docs](http://www.djangoproject.com/documentation/newforms/). On the Colddirt demo site, this is how I used newforms. I'll take the index page as an example.  
I've accessed the newforms module like so:  
```bash
from django import newforms as forms
```  
  
The next thing to look at is the actual creation of the form. You can keep your forms in models.py, although there is a trend going to keep them in a forms.py file. That is they are for Colddirt.  

#### forms.py

  
  
```python
attrs_dict = { 'class': 'norm_required' }
tag_dict = { 'class': 'tag_required' }

class DirtyForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea(attrs=textbox_dict), label='What\'s your cold dirt?')
    tag_list = forms.CharField(max_length=150, widget=forms.TextInput(attrs=tag_dict), label='Tags')

```  
  
I'm keeping it simple for now. Some key things to note is the field type (CharField) and the widget type (Textarea/TextInput). You can guess what each means. Here's a gem for your tool chest: how do you apply CSS to the forms? That is what the 'attrs=' part is about -- that will put in a class for you to assign CSS to. Nifty. The label creates a 'label' element that you can access. Let's render the form and send it to the template.  
To get a form displayed we need to generate the form, and send it to the template.  

#### views.py

  
```python
dirt_form = DirtyForm() 
```  
  
Send it to the template.  

#### views.py

  
```python
    return list_detail.object_list(
           request,
           queryset = Dirt.objects.order_by('?')[:100],
           template_name = "dirty/dirt_list.html",
           template_object_name = "dirty",
           paginate_by = 10,
           extra_context = {'form': dirt_form.as_ul()}
        )
```  
  
That's it, although we will revisit this index view shortly. One important thing to note is the .as_ul() appended to the form element. This tells the template to encapsulate the form elements as list elements (as opposed to say, a table). Now, let's display the form.  

#### templates/dirt_list.html

  
```python
{% if form %}
        

{{ form }}

{% endif %}
```  
  
The form thus appears because of the block, {{ form }}. You can see in the action type that it will post the data to the index page->view. Let's revisit the entire index view now.  

#### views.py

  
  
```bash
def index(request):
    import re
    from django.template.defaultfilters import slugify
    dirt_form = DirtyForm()
    if request.method == 'POST':
        dirt_form = DirtyForm(request.POST)
        if dirt_form.is_valid():
            # I opted not to create an m2m relationship for several
            # reasons. Note: the latest_word is some random word.
            latest_word = Word.objects.filter(is_taken__exact=False).order_by('?')[:1]            
            latest_word[0].is_taken=True
            latest_word[0].save()
            new_dirt = Dirt(description=dirt_form.clean_data['description'],
                            dirtword=latest_word[0].dirtyword)
            new_dirt.save()
            # Credit for the tag parsing goes to Ubernostrum (James B)
            # from the Cab (great for learning!) project
            # I opted to not store tag_list in each entry
            # Splitting to get the new tag list is tricky, because people
            # will stick commas and other whitespace in the darndest places.
            new_tag_list = [t for t in re.split('[\s,]+', dirt_form.clean_data['tag_list']) if t]
            # Now add the tags
            for tag_name in new_tag_list:
                tag, created = Tagling.objects.get_or_create(name=slugify(tag_name), slug=slugify(tag_name))
                new_dirt.tags.add(tag)
            return HttpResponseRedirect(new_dirt.get_absolute_url())
    return list_detail.object_list(
           request,
           queryset = Dirt.objects.order_by('?')[:100],
           template_name = "dirty/dirt_list.html",
           template_object_name = "dirty",
           paginate_by = 10,
           extra_context = {'form': dirt_form.as_ul()}
        )
```  
  
Let me pretend I am the form and have just been submitted to the view. First I'm tested if I'm a POST. Next, my data is dumped into the dirt_form variable. I'm then tested if I'm valid data or not (validation explanation next). Since I'm valid data, stuff happens. In the instance of Colddirt, a random word is taken from the Word database. The word is then updated as is_taken, and saved. Then the dirt is actually created. One thing to notice is how we access form data:  
```python
description=dirt_form.clean_data['description']
```  
  
So, the new dirt (with description and new word) is saved. Next, let's deal with the tags. Credit goes to [James](http://www.b-list.org/) for parsing the tag_list.  
```python
            new_tag_list = [t for t in re.split('[\s,]+', dirt_form.clean_data['tag_list']) if t]
            # Now add the tags
            for tag_name in new_tag_list:
                tag, created = Tagling.objects.get_or_create(name=slugify(tag_name), slug=slugify(tag_name))
                new_dirt.tags.add(tag)
```  
  
You can see dirt_form.clean_data used again. Another neat trick is to use slugify to make sure your tags are lowercase and aren't all weirdo like. The user is then redirected to the absolute url of the dirt the just created.  
So what about validation? Don't think I forgot this one. Validation (from what I have seen) is actually really easy. I'm going to first display the _entire_ form.  

#### forms.py

  
```bash
class DirtyForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea(attrs=textbox_dict), label='What\'s your cold dirt?')
    tag_list = forms.CharField(max_length=150, widget=forms.TextInput(attrs=tag_dict), label='Tags')
 
    def clean_description(self):
        import re
        if self.clean_data.get('description'):
            value = self.clean_data['description']
            if len(value) > 20 and not re.search('[<>]', value):
                try: 
                    hasNoProfanities(value, None)
                    return value
                except:
                    raise forms.ValidationError(u'Extremily dirty words, racial slurs and random characters are not allowed in dirt.') 
            else:
                raise forms.ValidationError(u'A little more detail please. No HTML.')
               
    def clean_tag_list(self):
        if self.clean_data.get('tag_list'):
            value = self.clean_data['tag_list']
            try: 
                hasNoProfanities(value, None)
                return value
            except:
                raise forms.ValidationError(u'Extremily dirty words or racial slurs are not allowed!')

```  
  
There is a fair amount of normal validation that occurs in the is_valid process, but here is some extra validation I added. Inside the DirtyForm class (as you can see) simply add a test for if the data is 'clean' or not (I don't know how to beter phrase this -- "send the data to the cleaners"). I'm testing the description to make sure it is long enough, and to make sure it doesn't have <>'s in it (to prevent XSS and odd stuff). If it detects them, the lower error is displayed. I've also tied in the hasNoProfanities validation, which pulls the words from my settings file. Not that I care if people swear or not, I'm mainly using this to prevent racial slurs, which I do care about.  
So, there you have it, one example of how newforms is used in a 'live' site. I hope this is helpful for somebody, I wish I could have seen more newforms examples when I started learning. If you are truly stumped on something, take a look inside the django source (/tests/regressiontests/forms/tests.py) for a **lot** of examples of every way you could use newforms.