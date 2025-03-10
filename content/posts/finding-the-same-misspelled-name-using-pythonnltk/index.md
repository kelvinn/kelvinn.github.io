---
title: 'Finding The Same (Misspelled) Name Using Python/NLTK'
date: 2013-09-13T17:24:00.000+10:00
draft: false
url: /2013/09/finding-same-misspelled-name-using.html
tags: 
- python
- howtos
---

I have been meaning to play around with the [Natural Language Toolkit](http://nltk.org/) for quite some time, but I had been waiting for a time when I could experiment with it and actually create some value (as opposed to just play with it). A suitable use case appeared this week: matching strings. In particular, matching two different lists of many, many thousands of names.  
  
To give you an example, let's say you had two lists of names, but with the name spelled incorrectly in one list:  
  
List 1:  
Leonard Hofstadter  
Sheldon Cooper  
Penny  
Howard Wolowitz  
Raj Koothrappali  
Leslie Winkle  
Bernadette Rostenkowski  
Amy Farrah Fowler  
Stuart Bloom  
Alex Jensen  
Barry Kripke  
  
List 2:  
Leonard Hofstadter  
Sheldon Coopers  
Howie Wolowits  
Rav Toothrapaly  
Ami Sarah Fowler  
Stu Broom  
Alexander Jensen  
  
This could easily occur if somebody was manually typing in the lists, dictating names over the phone, or spell their name differently (e.g. Phil vs. Phillip) at different times.  
  
If we wanted to match people on List 1 to List 2, how could we go about that? For a small list like this you can just look and see, but with many thousands of people, something more sophisticated would be useful. One tool could be NLTK's edit\_distance function. The following Python script displays how easy this is:  
  
```
import nltk

list\_1 = \['Leonard Hofstadter', 'Sheldon Cooper', 'Penny', 'Howard Wolowitz', 'Raj Koothrappali', 'Leslie Winkle', 'Bernadette Rostenkowski', 'Amy Farrah Fowler', 'Stuart Bloom', 'Alex Jensen', 'Barry Kripke'\]

list\_2 = \['Leonard Hofstadter', 'Sheldon Coopers', 'Howie Wolowits', 'Rav Toothrapaly', 'Ami Sarah Fowler', 'Stu Broom', 'Alexander Jensen'\]

for person\_1 in list\_1:
    for person\_2 in list\_2:
        print nltk.metrics.edit\_distance(person\_1, person\_2), person\_1, person\_2

```  
0 Leonard Hofstadter Leonard Hofstadter  
15 Leonard Hofstadter Sheldon Coopers  
14 Leonard Hofstadter Howie Wolowits  
15 Leonard Hofstadter Rav Toothrapaly  
14 Leonard Hofstadter Ami Sarah Fowler  
16 Leonard Hofstadter Stu Broom  
15 Leonard Hofstadter Alexander Jensen  
14 Sheldon Cooper Leonard Hofstadter  
1 Sheldon Cooper Sheldon Coopers  
13 Sheldon Cooper Howie Wolowits  
13 Sheldon Cooper Rav Toothrapaly  
12 Sheldon Cooper Ami Sarah Fowler  
11 Sheldon Cooper Stu Broom  
12 Sheldon Cooper Alexander Jensen  
16 Penny Leonard Hofstadter  
13 Penny Sheldon Coopers  
13 Penny Howie Wolowits  
14 Penny Rav Toothrapaly  
16 Penny Ami Sarah Fowler  
9 Penny Stu Broom  
13 Penny Alexander Jensen  
11 Howard Wolowitz Leonard Hofstadter  
13 Howard Wolowitz Sheldon Coopers  
4 Howard Wolowitz Howie Wolowits  
15 Howard Wolowitz Rav Toothrapaly  
13 Howard Wolowitz Ami Sarah Fowler  
13 Howard Wolowitz Stu Broom  
14 Howard Wolowitz Alexander Jensen  
16 Raj Koothrappali Leonard Hofstadter  
14 Raj Koothrappali Sheldon Coopers  
16 Raj Koothrappali Howie Wolowits  
4 Raj Koothrappali Rav Toothrapaly  
14 Raj Koothrappali Ami Sarah Fowler  
14 Raj Koothrappali Stu Broom  
16 Raj Koothrappali Alexander Jensen  
14 Leslie Winkle Leonard Hofstadter  
13 Leslie Winkle Sheldon Coopers  
11 Leslie Winkle Howie Wolowits  
14 Leslie Winkle Rav Toothrapaly  
14 Leslie Winkle Ami Sarah Fowler  
12 Leslie Winkle Stu Broom  
12 Leslie Winkle Alexander Jensen  
17 Bernadette Rostenkowski Leonard Hofstadter  
18 Bernadette Rostenkowski Sheldon Coopers  
18 Bernadette Rostenkowski Howie Wolowits  
19 Bernadette Rostenkowski Rav Toothrapaly  
20 Bernadette Rostenkowski Ami Sarah Fowler  
20 Bernadette Rostenkowski Stu Broom  
17 Bernadette Rostenkowski Alexander Jensen  
15 Amy Farrah Fowler Leonard Hofstadter  
14 Amy Farrah Fowler Sheldon Coopers  
15 Amy Farrah Fowler Howie Wolowits  
14 Amy Farrah Fowler Rav Toothrapaly  
3 Amy Farrah Fowler Ami Sarah Fowler  
14 Amy Farrah Fowler Stu Broom  
13 Amy Farrah Fowler Alexander Jensen  
15 Stuart Bloom Leonard Hofstadter  
12 Stuart Bloom Sheldon Coopers  
12 Stuart Bloom Howie Wolowits  
14 Stuart Bloom Rav Toothrapaly  
13 Stuart Bloom Ami Sarah Fowler  
4 Stuart Bloom Stu Broom  
14 Stuart Bloom Alexander Jensen  
15 Alex Jensen Leonard Hofstadter  
12 Alex Jensen Sheldon Coopers  
13 Alex Jensen Howie Wolowits  
15 Alex Jensen Rav Toothrapaly  
13 Alex Jensen Ami Sarah Fowler  
10 Alex Jensen Stu Broom  
5 Alex Jensen Alexander Jensen  
15 Barry Kripke Leonard Hofstadter  
13 Barry Kripke Sheldon Coopers  
13 Barry Kripke Howie Wolowits  
12 Barry Kripke Rav Toothrapaly  
13 Barry Kripke Ami Sarah Fowler  
10 Barry Kripke Stu Broom  
14 Barry Kripke Alexander Jensen  
  
As you can see, this displays the [Levenstein distance](http://en.wikipedia.org/wiki/Levenshtein_distance) of the two sequences. Another option we have is to look at the ratio.  
  
```
len1 = len(list\_1)
len2 = len(list\_2)
lensum = len1 + len2
for person\_1 in list\_1:
    for person\_2 in list\_2:
        levdist = nltk.metrics.edit\_distance(person\_1, person\_2)
        nltkratio = (float(lensum) - float(levdist)) / float(lensum)
        if nltkratio > 0.70:
            print nltkratio, person\_1, person\_2

```  
1.0 Leonard Hofstadter Leonard Hofstadter  
0.944444444444 Sheldon Cooper Sheldon Coopers  
0.777777777778 Howard Wolowitz Howie Wolowits  
0.777777777778 Raj Koothrappali Rav Toothrapaly  
0.833333333333 Amy Farrah Fowler Ami Sarah Fowler  
0.777777777778 Stuart Bloom Stu Broom  
0.722222222222 Alex Jensen Alexander Jensen