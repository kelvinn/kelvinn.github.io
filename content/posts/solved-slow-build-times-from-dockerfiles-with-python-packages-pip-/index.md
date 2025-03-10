---
title: 'Solved: slow build times from Dockerfiles with Python packages (pip)'
date: 2014-07-02T18:13:00.002+10:00
draft: false
url: /2014/07/solved-slow-build-times-from.html
tags: 
- docker
- python
- howtos
---

I have recently had the opportunity to begin exploring [Docker](http://www.docker.com/), the currently hip way to build application containers, and I generally like it. It feels a bit like using Xen back in 2005, when you still had to download it from cl.cam.ac.uk, but there is _huge_ momentum right now. I like the idea of breaking down each component of your application into unique services and bundling them up - it seems clean. The next year is going to be very interesting with Docker, as I am especially looking forward to seeing how Google's App Engine allows Docker usage, or what's in store for the likes of Flynn, Deis, CoreOS, or Stackdock.  

  

One element I had been frustrated with is the build time of my image to host a Django application I'm working on. I kept hearing these crazy low rebuild times, but my container was taking ages to rebuild. I noticed that it was cached up until I re-added my code, and then pip would reinstall all my packages.

  

It appeared as though anything after I used ADD for my code was being rebuilt, and reading online seemed to confirm this. Most of the items were very quick, e.g. "EXPOSE 80", but then it hit "RUN pip -r requirements.txt"

  

There are various documented ways around this, from two Dockerfiles to just using packaged libraries. However, I found it easier to just use multiple ADD statements, and the good Docker folks have added caching for them. The idea is to ADD your requirements first, then RUN pip, and then ADD your code. This will mean that any code changes don't invalidate the pip cache.

  

For instance, I had something (abbreviated snippet) like this:

  
```
\# Set the base image to Ubuntu
FROM ubuntu:14.04

# Update the sources list
RUN apt-get update
RUN apt-get upgrade -y

# Install basic applications
RUN apt-get install -y build-essential

# Install Python and Basic Python Tools
RUN apt-get install -y python python-dev python-distribute python-pip postgresql-client

# Copy the application folder inside the container
ADD . /app

# Get pip to download and install requirements:
RUN pip install -r /app/requirements.txt

# Expose ports
EXPOSE 80 8000

# Set the default directory where CMD will execute
WORKDIR /app

VOLUME \[/app\]

CMD \["sh", "/app/run.sh"\]

```  

And it rebuild pip whenever the code changes. Just add the requirements and move the RUN pip line:

  
```
\# Set the base image to Ubuntu
FROM ubuntu:14.04

# Update the sources list
RUN apt-get update
RUN apt-get upgrade -y

# Install basic applications
RUN apt-get install -y build-essential

# Install Python and Basic Python Tools
RUN apt-get install -y python python-dev python-distribute python-pip postgresql-client

ADD requirements.txt /app/requirements.txt

# Get pip to download and install requirements:
RUN pip install -r /app/requirements.txt

# Copy the application folder inside the container
ADD . /app

# Expose ports
EXPOSE 80 8000

# Set the default directory where CMD will execute
WORKDIR /app

VOLUME \[/app\]

CMD \["sh", "/app/run.sh"\]

```  
I feel a bit awkward for having missed something that must be so obvious, so hopefully this can help somebody in a similar situation.