---
title: 'Using HTML in a Django form label'
date: 2010-07-11T20:30:00.002+10:00
draft: false
url: /2010/07/using-html-in-django-form-label_2240.html
tags: 
- django
- python
- howtos
- web
---

I recently had the need to add some HTML to the label for a form field using Django. The solution is pretty easy, except I didn't see it written explicitly anywhere, and I missed the memo of the function I should be using.  
My form first just had the HTML in the form label as so:  
```

from django import forms

class AccountForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(), max\_length=15, label='Your Name ([why](http://www.blogger.com/questions/whyname/)?')

```  
  
However, when I displayed it, the form was autoescaped.  
[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhvsLvb6I4SDBB3NKptLZzGLGnwUZK0KmYlx7X9UC2_fzyQCNTkeFiKz5-4_3BmKArYZhRwU8TNEIhrGAMsb039N47hxcY8BIMEJjfK1UafYCRvAPzY18c8ceq3QFOOsp_oGO6SavZ1LmGR/s800/accountsform.jpg)](http://picasaweb.google.com/lh/photo/PyGNXDrpXtrgBNnoOLlfLA?feat=embedwebsite)  
  
This is generally a good thing, except my form obviously didn't display correctly. I tried autoescaping it in the template, but that didn't work. To resolve this you'll need to mark that _individual label_ as safe. Thus:  
```

from django.utils.safestring import mark\_safe
from django import forms

class AccountForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(), max\_length=15, label=mark\_safe('Your Name ([why](http://www.blogger.com/questions/whyname/)?)'))
    
```  
  
It will now display correctly:  
```
In \[1\]: from myproject.forms import \*

In \[2\]: form = AccountForm()

In \[3\]: form.as\_ul()
Out\[3\]: u'
*   Your Name ([why](http://www.blogger.com/questions/whyname/)?): 
'
```  
  
There's maybe another easier way to do this, but this worked for me.