# The Intern Files

Welcome to The Intern Files! Congratulations on getting the Lockheed Internship. 

At this point you may be slightly overwhelmed, confused, excited, or all of the above. This is meant to hopefully help in getting you started, and can be updated for future generations of interns.

#### Table of Contents
* [Installations and Setting Up](#installations-and-setting-up)
  * [Anaconda and Jupyter Notebook](#anaconda-and-jupyter-notebook)
  * [Helita](#helita)


## Installations and Setting Up

Setting up software, paths, environments, etc. is inherently a fairly time-consuming and frustrating process. Good luck!

#### Anaconda and Jupyter Notebook:
Jupyter Notebook is a very useful, commonly used application in which you can easily run your code (especially useful for plotting and images). You will likely use it frequently in the beginning of your internship and later on as a good starting place for new ideas.

To install:
* Download the Python 3.6 version (can also download 2.7 version if necessary) of the Graphical Installer from this website: https://www.continuum.io/downloads
* Launch Jupyter Notebook from terminal:
 ```
 jupyter notebook
 ```

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
