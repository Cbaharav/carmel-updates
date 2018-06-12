
FFT Data Demo
=============

.. code:: ipython3

    from helita.sim import bifrost_fft as brft

.. code:: ipython3

    dd = brft.FFTData(file_root = 'cb10f', fdir = '/net/opal/Volumes/Amnesia/mpi3drun/Granflux')

.. code:: ipython3

    transformed = dd.get_tfft('r', snap = [430, 431, 432], iiy = 20)


.. parsed-literal::

    (512, 544, 3)


.. code:: ipython3

    transformed.keys()




.. parsed-literal::

    dict_keys(['freq', 'ftCube'])


