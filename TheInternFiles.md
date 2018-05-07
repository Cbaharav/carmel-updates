# The Intern Files

Welcome to The Intern Files! Congratulations on getting the Lockheed Internship. 

At this point you may be slightly overwhelmed, confused, excited, or all of the above. This is meant to hopefully help in getting you started, and can be updated for future generations of interns.

#### Table of Contents
* [Installations and Setting Up](#installations-and-setting-up)
  * [Anaconda and Jupyter Notebook](#anaconda-and-jupyter-notebook)
  * [Helita](#helita)
  * [Kyoto](#kyoto)
  * [Pycuda](#pycuda)
  * [Sublime](#sublime)
* [Stuff to Know](#stuff-to-know)
  * [Basic Unix](#basic-unix)
  * Python
  * Numpy (& Matplotlib)
* More to come...


## Installations and Setting Up

Setting up software, paths, environments, etc. is inherently a fairly time-consuming and frustrating process. Good luck!

---
#### Anaconda and Jupyter Notebook:
Jupyter Notebook is a very useful, commonly used application in which you can easily run your code (especially useful for plotting and images). You will likely use it frequently in the beginning of your internship and later on as a good starting place for new ideas.

To install:
* Download the Python 3.6 version (can also download 2.7 version if necessary) of the Graphical Installer from this website: https://www.continuum.io/downloads
* Launch Jupyter Notebook from terminal by typing "jupyter notebook"

---
#### Helita:
This houses a lot of important stuff, including the almighty bifrost.py and bq_t5_look.py (I may or may not be biased).

To install:
* Using Terminal, clone the latest version of helita from Juan's branch on Github:
 ```
 git clone https://github.com/jumasy/helita.git
 cd helita
 python setup.py install
 ```
* Open helita/helita/io/`__init__`.py (either through Terminal with the "open" command, or by manually opening the file through finder if you are new to Terminal), and change it to read:
 ``` python
 
"""
Set of tools to interface with different file formats.
"""

__all__ = ["crispex", "fio", "lp"] #, "ncdf", "sdf"]

from . import crispex
from . import lp
# from . import ncdf
 ```
* Open .cshrc (by typing ".cshrc" in Terminal) and add a path for helita:
```
setenv HELITA "~/helita-master/helita"
```
* To update helita later on, cd into the helita directory and use "git pull"
* If this does not work, you may have to do a hard pull to override all of your local changes. **WARNING:** *Do this only if you are aware that you will be losing ALL of your changes to every file within helita and if you have copies of changes you want to save elsewhere!!!*
```
cd helita
git fetch origin master
git reset --hard FETCH_HEAD
```
---
#### Kyoto:
This is a server which you have access to, and which has a graphics card. This is useful for running code that has several threads running in parallel (your machine can't handle that).

To login to kyoto:
* In Terminal, type "ssh -y kyoto"
* When prompted for a password, enter the password that allows you to log on to your computer

To install Anaconda in kyoto:
* Copy the file from /sanhome/juanms to your Kyoto home directory
```
cp /sanhome/juanmsAnaconda3-4.4.0-Linux-x86_64.sh
```
* Then run:
```
bash Anaconda3-4.4.0-Linux-x86_64.sh 
```
* **I don’t remember how I opened a .cshrc file in kyoto, permission currently denied**
* Inside the .cshrc file in kyoto, copy these lines **(the first line is missing a /usr/bin somewhere, but I'm not sure where because I can't see my .cshrc file)**:
```
setenv PATH ~/anaconda3/bin:/usr/bin:~/bin/:/usr/local/bin:/usr/local/cuda/bin:/usr/texbin/:$PATH
setenv http_proxy http://proxy-ics.external.lmco.com:80
setenv https_proxy http://proxy-ics.external.lmco.com:80
setenv ALL_PROXY http://proxy-ics.external.lmco.com:80
#CUDA: 
setenv PATH /usr/local/cuda7-5/bin:$PATH
setenv LD_LIBRARY_PATH /usr/local/cuda-7.5/lib64 
setenv CUDA_LIB $BIFROST/CUDA/
setenv DYLD_LIBRARY_PATH /usr/local/cuda/lib

```
* Enter "csh" into the command line
* Enter "python" into the command line, and check that the version being used is 3.6, if this is not the case, seek help from a trained professional
* To leave kyoto and return to your home machine, enter "exit()"

---

#### PyCuda:
This is a python wrapper for cuda, and it is useful for parallelization (breaking up big tasks into smaller ones that are run simultaneously, and therefore finish faster than if the calculation was run linearly). It can only be run on a GPU (like the one that Kyoto has).

To install:
* Make sure you are in kyoto (if not, see [Kyoto](#kyoto) for log-in instructions)
* Copy the file pycuda-2017.1.tar.gz from sanhome into your kyoto home directory:
```
cp /sanhome/juanms/pycuda-2017.1.tar.gz ~
```
* Uncompress the folder by typing: tar xfz pycuda-2017.1.tar.gz
* Then, following the instructions in the README_SETUP file, type:
```
./configure.py
make
make install
```
---

#### Sublime:
This is a fairly standard text editor that I like, feel free to install a different one if you have a preference. You can download it from their website: https://www.sublimetext.com

Pro tip: I was going to suggest changing the color theme to limit the strain on your eyes, but as I was trying to figure out how I changed the preference, I accidentally changed the theme and now I can't find the one I liked. So don't do that.

---

## Stuff to Know
Please change this title if you think of a better one. This section includes languages and applications that you should probably get to know, because they'll be pretty helpful. I'll try to attach cheat sheets and highlight the important points of each one.

---

#### Basic Unix:
Maybe you are more prepared than I was, and you already know how to navigate unix commands like a pro. If so, good for you! If all you've seen is a cool wizard-like person quickly navigating through the computer and you have no idea what this sorcery is, don't worry-- that was me.

Here is a pretty standard cheat sheet: http://cheatsheetworld.com/programming/unix-linux-cheat-sheet/

The commands you'll use frequently: cd, open, python (if you want to run a file with python), and maybe ls & pwd if you get lost a lot (no shame).

Another useful part of terminal is iPython! Type in "ipython" to get an exciting python interface to test some of your code (like if you're working with bifrost.py).

---

#### Python:

Good course for the basics (feel free to skip around): https://www.edx.org/course/python-data-science-uc-san-diegox-dse200x
This is the cheat sheet I made based off of the course, **figure out how to attach file**: http://localhost:8888/notebooks/AnacondaProjects/Python%20Basics.ipynb





