**********
bifrost.py
**********
bifrost.py is a set of tools to read and interact with output from Bifrost simulations.

BifrostData Class
=================
bifrost.py includes the BifrostData class (among others). The following allows to create the class for snapshot number 430 from simulation 'cb10f' from directory '/net/opal/Volumes/Amnesia/mpi3drun/Granflux'::

	from helita.sim import bifrost as br
	dd = br.BifrostData('cb10f', snap = 430, fdir = '/net/opal/Volumes/Amnesia/mpi3drun/Granflux')

The snapshot(s) being read can be defined when creating the object, or set/changed anytime later. Snaps can be ints, arrays, or lists. 

Getting Variables & Quantities
==============================
get_var and get_varTime can be used to read variables as well as to calculate quantities (with a call to _get_quantity). iix, iiy, and iiz can be specified to slice the return array (they can be ints, arrays, or lists). If no snapshot is specified, the current snap value will be used (either the initialized one, which is the first in the series, or the most recent snap used in set_snap or in a call to get_var). To get variable 'r' at snap 430 with only values at y = 200, z = 5, and z = 7::

	var1 = dd.get_var('r', snap = 430, iiy = 200, iiz = [5, 7])

get_varTime can be used in the same fashion, with the added option of reading a specific variable or quantity from many snapshots at once. Its return arrays have an added dimension for time.

FFTData Class
==============
This class can be found within bifrost_fft.py. It performs operations on Bifrost simulation data in its native format. After creating a class for a specific snap root name and directory (much like with BifrostData), one can get a dictionary of the frequency and amplitude of the Fourier Transform for a certain quantity over a range of snapshots.

#.. ipython::

   In [1]: x = 2

   In [2]: from helita.sim import bifrost_fft as brft

   In [3]: dd = brft.FFTData(file_root = 'cb10f', fdir = '/net/opal/Volumes/Amnesia/mpi3drun/Granflux')

   In [4]: transformed = dd.get_fft('ux', snap = [430, 431, 432, 433])

   In [5]: transformed.keys()