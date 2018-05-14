bifrost.py
==========

bifrost.py is a set of tools to read and interact with output from Bifrost simulations.

Installation
------------

bifrost.py is part of the helita library. Helita documentation can be found here: 

&nbsp;&nbsp;&nbsp; http://helita.readthedocs.io/en/latest/index.html

To install helita:

  ```
  git clone https://github.com/ITA-solar/helita.git
  cd helita
  python setup.py install
  ```

BifrostData Class
-------------------

bifrost.py includes the BifrostData class (among others). The following allows to create the class for snapshot number 430 from simulation 'cb10f' from directory '/net/opal/Volumes/Amnesia/mpi3drun/Granflux':

```python
from helita.sim import bifrost as br
dd = br.BifrostData('cb10f', snap = 430, fdir = '/net/opal/Volumes/Amnesia/mpi3drun/Granflux')
```
The snapshot(s) being read can be defined when creating the object, or set/changed anytime later. Snaps can be ints, arrays, or lists. 

Getting Variables & Quantities
------------------------------

get_var and get_varTime can be used to read variables as well as to calculate quantities (with a call to _get_quantity). iix, iiy, and iiz can be specified to slice the return array (they can be ints, arrays, or lists). If no snapshot is specified, the current snap value will be used (either the initialized one, which is the first in the series, or the most recent snap used in set_snap or in a call to get_var). To get variable 'r' at snap 430 with only values at y = 200, z = 5, and z = 7:

```python
var1 = dd.get_var('r', snap = 430, iiy = 200, iiz = [5, 7])
```

get_varTime can be used in the same fashion, with the added option of reading a specific variable or quantity from many snapshots at once. Its return arrays have an added dimension for time.
