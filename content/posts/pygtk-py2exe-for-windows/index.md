---
title: 'PyGTK + py2exe for Windows'
date: 2008-11-02T21:30:00.009+11:00
draft: false
url: /2008/11/pygtk-py2exe-for-windows_8282.html
tags: 
- windows
- python
- howtos
---

I'm writing down these quick notes so I can remember the steps for getting py2exe to work with GTK.

*   Download the GTK+ runtime
*   Download py2exe
*   Copy over your project into the windows box
*   Create a setup.py file (see below)
*   Run "c:\\Python25\\python.exe setup.py py2exe"
*   Copy over the lib, etc, and share folder from C:\\Program Files\\GTK2-Runtime into the dist folder
*   Run app!

  

setup.py:

```python
from distutils.core import setup
import py2exe

setup(
    name = 'ploteq',
    description = 'Bunnys Plotting Tool',
    version = '1.0',

    windows = [
        {
        'script': 'ploteq.py',
        }
    ],

    options = {
        'py2exe': {
        'packages':'encodings',
        'includes': 'cairo, pango, pangocairo, atk, gobject', 
        }
    },

    data_files=[
        'ploteq.glade',
    ]
)

```