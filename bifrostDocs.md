bifrost.py
==========

bifrost.py is a set of tools to read and interact with output from Bifrost simulations.

Installation
------------

bifrost.py is part of the helita library. Helita documentation can be found here: 

&nbsp;&nbsp;&nbsp; http://helita.readthedocs.io/en/latest/index.html

To install helita:

  &nbsp;&nbsp;&nbsp; git clone https://github.com/ITA-solar/helita.git <br />
  &nbsp;&nbsp;&nbsp; cd helita <br />
  &nbsp;&nbsp;&nbsp; python setup.py install

In .cshrc add a path for helita: <br />

  &nbsp;&nbsp;&nbsp; setenv HELITA "~/helita-master/helita"

Basics
------

bifrost.py uses BifrostData objects. To make a BifrostData object:

&nbsp;&nbsp;&nbsp; >>> from helita.sim import bifrost as br <br />
&nbsp;&nbsp;&nbsp; >>> dd = br.BifrostData('file root name', fdir = 'directory path')
