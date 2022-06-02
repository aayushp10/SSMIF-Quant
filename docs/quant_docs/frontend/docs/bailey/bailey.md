---
id: bailey
title: Bailey
sidebar_label: Bailey
slug: /bailey
---

##### Bailey Documentation By: Scott Caratozzolo
##### Spring 2020 - Present

### Preface
My name is Scott Caratozzolo and I am the current Head of Quantitative Investment Solutions for the Spring 2020 semester. I am also arguably the only
person who really understands the ins and outs of Bailey. That is why I’m writing this documentation, to try and explain/teach the different areas of Bailey
and how to continue developing it.
While writing this documentation I’ve noticed some things that could be
improved or could be fixed in Bailey, so odds are, while I’m writing this documentation under one version of Bailey, by the time you’re working on it, it
might be much different. I’ll try to keep this documentation updated, but I
can’t make any promises.
I should also make it clear that I’m by no means a teacher. I’ve always
been pretty bad at trying to teach things to people because things make sense
to me and I don’t know how to explain things in more simplistic terms. I will
try my best to explain things in simple terms, but for a lot of Bailey, simple
terms is basic HTML or basic Python. This documentation is not meant to be
a tutorial in these topics. To successfully develop Bailey I’d suggest brushing
up or learning things in these areas:
* HTML
* CSS
* Javascript
* JQuery
* Flask
* Rest API
* SQL
* Pandas - Python Package
* Git/Github
* Terminal/Command Prompt usage  

These are all things that are needed to work on Bailey. You, specifically, may
not need to know everything. Quant is a team, after all. If you are to have a
good understanding of Bailey, it would be good to know a lot of these.
I pieced together a lot of Bailey, and wrote a lot of the infrastructure, but
there is still a decent amount of code that was written by other people, and our
main goal was to get things up and running as fast as possible which means
there are inconsistencies between code. I’ve tried fixing that, but it’s always
a work in progress. Furthermore, a lot of the work I did happened while I
was slightly intoxicated. Hell, I’m writing this a couple of Twisted Teas in.
Due to the fact that I know Bailey best, and because some code could be
confusing, I invite anyone reading this to reach out to me. My personal email is
[scaratozzolo12@gmail.com](mailto:scaratozzolo12@gmail.com), or you can contact me on [LinkedIn](https://www.linkedin.com/in/scaratozzolo/), [Instagram](https://www.instagram.com/svcaratozzolo/), or
[Github](https://github.com/scaratozzolo)
Bailey is my baby, and I want it to be the best possible. My time in SSMIF
might be over, but I will try to leave Bailey in the best shape possible, even if
that means working on it after I’m gone.
To recap, I made Bailey, it might not be as straight forward to understand.
This documentation is meant to help with learning how to working on Bailey,
but these docs might not be so easy to understand either. If you need help, just
reach out. Enjoy your time in SSMIF. It’ll be over before you know it.

### Chapter 1: Introduction
**1.1 What is Bailey?**  
Bailey is a Flask-backed web app being hosted at here. It is maintained and
developed by the Quantitative Investment Solutions (QIS) team of the Stevens
Student Managed Investment Fund (SSMIF). Being a Flask app makes Bailey
written completely in Python. This allows for quicker and easier development
by QIS members who may not have experience in other languages such as R,
which the previous risk screen was written in.    
**1.2 Why was Bailey Created?**  
Bailey was created during the Fall 2019 semester as a way of simplifying the
risk screen process for Equity members and allow for better maintenance and
development by the QIS team. The Head of Quant during the Fall 2019 semester
was Greg Giordano, who thought of transferring the team’s code base from R
to Python. He also thought of making the risk screen into a web app, which is
where I came in. I converted our R based risk screen and developed the Python
Flask app, with support of other QIS members. By doing this, we’ve been
able to make a ton of bug fixes and overall improvements due to the simplicity
of Python. Originally Bailey was just the risk screen, but it is continuing to
expand and has recently gotten early factor model integration. In the Fall of
2020 we’re hoping to integrate a portfolio stress test. Overall, Bailey’s main
goal is to become a hub for fund information and data, that can be accessed via
the website or by the API we’ve developed.

**1.3 Where Did the Name Come From?**  
QIS was pretty close during the Fall 2019 semester and we would constantly
joke around and would have an occasional meme war. Greg used to call us 4
clowns. What also has a lot of clowns? Ringling Bros. and Barnum & Bailey.
This is important as it shows the culture of the Quant team. We are able to
get our work done, but we’re also able to make new connections and have fun.
Yes, SSMIF is a professional fund, however, it’s important to live a little, too.

### Chapter 2: Getting Started with Bailey
**2.1 Python**  
This should go without saying, but in order to work with Bailey you are going to
need Python installed on your machine. We’ve been using Python 3.7.6 which
has gotten the job done. I don’t know how forward or backward compatible the
different versions of Python are with Bailey, but it shouldn’t be too drastic.   

**2.2 Text Editor**  
In order to do any programming or web development you should have a proper
text editor. Over the last two semesters we’ve started using [Atom](https://atom.io/) as it is
developed by GitHub which means it has git and GitHub support. It also has a
ton of useful packages to make developing in Python and web development easy
to do. You could also use Notepad if you really wanted to, but this is just my
suggestion as it’s what I’ve used and might reference throughout these docs.

**2.3 Github**  
In previous semesters, a lot of code was lost during transitioning to the next
team. When we moved to Python we made sure to start keeping code in one
location versus having a project on one member’s local machine. The obvious
choice was Github. For that reason, in order to start your development on
Bailey you must have a Github account. The Github is currently controlled
by me as Head of Quant, but with the introduction of the Head of Front End
Development position this could change in the future. Once you have a Github
account you can be added as a collaborator to the repository (repo). Being
a collaborator will allow you commit and push directly to the repo instead of
having to fork it, make changes, and then merge it in. Our Github can be found
[here](https://github.com/SSMIF-Quant).  

**2.3.1 Git**  
As we are using Github, you are going to need git installed on your machine
also. You can download git [here](https://git-scm.com/downloads). Git will require you to set your email and
author name before you can make any commits, but Atom will tell you how to
do this when you start working with it. Git is used through the command line,
but like I said, Atom will tell you what to write. Alternatively, you can Google
how to do it as it’s a pretty standard thing to do.

**2.3.2 Learning Git**  
Git can seem kind of scary, but it’s really not that bad. Most of us didn’t
have a lot of Git experience prior to Bailey. I understood the basics of pushing
and pulling, but the idea of branches didn’t really make sense and scared me
because I didn’t want to break anything. If you don’t know any Git, I suggest
you learn how to commit, push, and pull along with learning how branches work
and making pull requests.  

**2.4 Required Python Packages**  
There are various Python packages that are required for Bailey to run. Most of
these are documented in the requirements.txt file in the repo. We try to keep
the list updated, but sometimes a package will slip through the cracks. As of
right now, this file has the following required packages that you need to install
prior to working on Bailey:  
* flask  
* numpy  
* pandas  
* pandas-datareader
* scikit-learn
* matplotlib
* plotly
* ipywidgets
* requests
* bs4  

As Bailey is a Flask app, I highly encourage you to look through the Flask
documentation and look at some tutorials. Furthermore, you should also look
into web development and learning HTML/CSS/Bootstrap/Javascript. I’ll try
to explain as much as possible what things are doing, but I can’t explain everything.   

**2.5 Getting Bailey**  
Find where you want the files for Bailey to be stored locally on your machine.
You are going to clone the repo using git. As Bailey was originally just the risk
screen, the repo on our Github is called "quant". When
you clone a repo, it will create a folder with the name of the repo. All files and
folders in this folder will reflect what you would see if you were browsing the
repo on Github.  
To clone the repo, run the following command from a command prompt or
terminal from the location you want the repo to be downloaded:

```bash
git clone https://github.com/SSMIF-Quant/quant.git --recurse-submodules
```

By running this command, git will download a copy of the repo to your machine
along with any dependencies, like the Factor Model repo. By default, you will
see the master branch [^1].  
While you could download and extract the zip file from Github, it’s important to know some basic terminal commands as it’s the best way to update Bailey on Pythonanywhere, which is where Bailey is hosted. I’ll go over using
Pythonanywhere later.  

**2.6 Running Bailey**   
Inside the repo there is a file called ”run bailey dev.bat” which is used to start
a local flask server on a Windows machine. If you’re on another OS I’m sure the
process of starting the server is similar, the bat file is just a way to quickly start
it instead of running everything through the command line. More information
can probably be found [here](https://flask.palletsprojects.com/en/master/server/).  

### Chapter 3: Bailey Overview  
The goal for Bailey is to become a hub for fund information and host the backend to some of our applications. As such, Bailey can be broken down into
multiple facets. I am going to go over each of these, however, as Bailey is
constantly being updated, code and line numbers may not be exact to what you
see.  

**3.1 \__init__.py**  
This is the brains of the whole operation. This file is located at SSMIF-QuantRisk-Screen\flaskr\ init .py. This file is where all the links for Bailey are
defined. With each link definition comes a function definition that tells Flask
what to do when that link is visited by a user. Many of the functions and scripts
that we have written are imported into this file and are used throughout.   
Just to show some of the stuff that’s in this file, here’s our ssmif.pythonanywhere.com/login
definition:

```python
# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    session.pop('username', None)
    session.pop('perms', (0, 0, 0))
    if request.method == 'POST':
        authenticated, perms = accounts.auth(request.form['username'], request.form['password'])
        if not authenticated:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['username'] = request.form['username']
            session['perms'] = perms
            return redirect(url_for('screen'))
    return render_template('login.html', error=error)

```










[^1]: Note- if you’re on a Windows machine, here’s a tip. Let’s say you have a folder on your
desktop called ”SSMIF”. If you double click that folder, the file explorer will open up to that
folder location. If you click the file address bar (the thing that says something like ”This
PC > C: > Users > blah blah...”) and type ”cmd” and press enter, a command prompt will
open with the current directory. You can then run the command above and the repo will be
downloaded to that location.
If you’re on Linux I assume you know your way around a terminal and directories. If you’re
on a Mac, well Mac is Whack.
