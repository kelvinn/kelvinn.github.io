---
title: AI as Maintainer
date: 2026-07-20T21:30:00.002+10:00
draft: false
url: /2026/07/ai-as-maintainer.html
tags:
  - articles
  - ai
  - github
  - web
---
For many years this website ran on Django. It worked well, and at the time it made sense. I wanted to learn Django, run the application myself, and generally understand every part of the stack.

Last year I moved the site to [Hugo](https://gohugo.io/), hosted on GitHub Pages, with GitHub Actions handling the build and deployment. I had been wishing to move to a static site for ages, and Copilot made that much easier.

Recently I noticed that I'm able to do everything I did previously with Django, but with Hugo + Codex. Similar to what Yegge says about the [AI Vampire](https://steve-yegge.medium.com/the-ai-vampire-eda6e4f07163) I've been having lots of fun extending all the little things that I have wanted to do, but never had time.
### The workflow

Today the workflow is simple, and follows what we would do with a static site normally:

- Write or edit content locally.
- Ask Codex to make a specific change, e.g. creating a custom sidebar.
- Review the diff.
- Commit the change to GitHub.
- Let GitHub Actions build and validate the site.
- Publish through GitHub Pages.

There is nothing especially clever about this. That is partly why it works so well.

Instead of thinking about which files need to be opened, edited, renamed, or checked, I can describe the outcome I want.

For example:

- Review every draft post and make the writing more professional.
- Find every travel post and standardise the heading structure.
- Read the old technical posts and improve grammar without changing the original intent.
- Check for broken image references after moving a folder.
- Add a Hugo template that lists posts in a different way.

Most of these are not difficult tasks. They are just tedious.

Previously I might have ignored them, or spent an hour manually fixing a pattern across dozens of Markdown files. Now I can ask for the change, review the result, and move on.

### Old content is easier to fix

Some posts on this site were written 20 years ago. They are snapshots of who I was at the time, which is part of why I keep them, but they were not always written with the future me in mind. For many years I left these as private.

The problem with old content is that improving it rarely feels urgent. A stale phrase, inconsistent heading, missing image, or awkward paragraph is not enough to justify spending a Saturday afternoon cleaning up a blog archive.

AI changes that equation.

It has made it practical to review old posts in bulk and:

- fix grammar
- improve readability
- modernise formatting
- remove outdated wording
- preserve the point of the original post

That last point matters. I do not want to rewrite everything into generic AI prose. I still want the posts to have my voice and overall original story, including the occasional awkward sentence or opinion I might phrase differently today.
### CI is still the safety net

One thing I have not automated away is quality control.

Every change still goes through GitHub Actions before it is published. The pipeline checks for things like Markdown issues, broken internal links, missing images, invalid references, build failures, and Hugo warnings.

That pairing is the important part. I am much more comfortable letting AI touch a large number of files because every change is visible in Git, and the site has to build before it is deployed.

### Final thoughts

I originally started this website to learn Django, and then to explore any new emerging technology. Now that I've stripped everything back to the most basic version possible, the purpose has likely changed: to leave a collection of stories for others - in particular my daughter when she's older - to read through. I'll do my best to avoid contaminating these stories with AI slop.