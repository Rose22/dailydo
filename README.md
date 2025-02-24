# dailydo
the self-cleaning daily todo list!

the idea is that you start with a blank new todo list every day, and you can just write down whatever tasks you need to throughout the day, cross them off, and then never see them again! 

this avoids many pitfalls of pretty much every todo system out there: they are overly complicated, have a lot of features, and it can be easy to get lost in organising it all. 

instead, this is just a simple list: no due dates, no categories, no priorities. therefore it's even simpler than todo.txt!

it gets stored as a simple text file. it's human-readable. no vendor lock-in, and fully open source. easy!

i made it as a modular python library so that it can be implemented in other projects and user interfaces can easily be made for it

# why?
i've tried so many different todo systems, and most of them didn't work for me. until one day, i built myself pretty much the perfect one in Notion: a todo list that starts out blank every day! for me, todo lists become unusable once they start becoming too overwhelming, and a todo list that just keeps growing every day has that problem. i could let the undone tasks sit in a backlog, nagging me every day that they weren't done yet (which is what most popular todo apps do), but this just leads to me not using them. if instead a task that wasn't done for the day just... disappears forever, then the list can never get too big!

but Notion is cumbersome. the website is slow, the desktop app is basically just the website, the data is in the hands of a corporation, the phone app is horrible to use. 

so here's my attempt to recreate this system, but as an actual application!

# how to use
you can either just run the web interface (web.py), or create your own interface for it!

to run the web interface, you'll have to install Flask. just run:
```pip install flask```

then:
```python web.py```

if you want to use it as a python library, check out `help(dailydo)` in python for more information on how to use it.
