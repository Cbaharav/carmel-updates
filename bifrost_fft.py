"""
Set of programs to read and interact with output from BifrostData
simulations focusing on Fourier transforms
"""
import time
import numpy as np
import os
from .bifrost import BifrostData, Rhoeetab, read_idl_ascii
from . import cstagger
import imp

try:
    imp.find_module('pycuda')
    found = True
except ImportError:
    found = False

if found:
    from reikna import cluda
    from reikna.fft import fft


class FFTData(BifrostData):

    """
    Class that operates radiative transfer form BifrostData simulations
    in native format.
    """

    def __init__(self, *args, **kwargs):

        super(FFTData, self).__init__(*args, **kwargs)
        """
        sets all stored vars to None
        """
        self.preCompFunc = None
        self.preCompShape = None
        self.transformed_dev = None
        self.api = None
        self.thr = None

    def get_fft(self, quantity, snap, iix=None, iiy=None, iiz=None):
        """
        Calculates FFT (by calling fftHelper)

        Parameters
        ----------
        quantity - string
        snap - array or list
        iix, iiy, and iiz - ints, lists, arrays, or Nones
            slices data cube

        Returns
        -------
        dictionary -
        {'freq': 1d array of frequencies,
        'ftCube': array of results (dimensions vary based on slicing)}

        Notes
        -----
            uses reikna (cuda & openCL) if available
        """

        # gets data cube, already sliced with iix/iiy/iiz
        preTransform = self.get_varTime(quantity, snap, iix, iiy, iiz)

        # gets rid of array dimensions of 1
        preTransform = np.squeeze(preTransform)
        transformed = np.empty((preTransform.shape))
        dt = self.params['dt']
        t = self.params['t']

        t0 = time.time()

        def fftHelper(preTransform, transformed, dt, t):

            # checking to see if time gap between snaps is consistent
            uneven = False
            for i in range(1, np.size(dt) - 1):
                if abs((t[i] - t[i - 1]) - (t[i+1] - t[i])) > 0.02:
                    uneven = True
                    break

            # interpolates data if time gaps are uneven
            if uneven:
                print('uneven dt')
                evenTimes = np.linspace(t[0], t[-1], np.size(dt))
                interp = sp.interpolate.interp1d(t, preTransform)
                preTransform = interp(evenTimes)
                evenDt = evenTimes[1] - evenTimes[0]
            else:
                evenDt = dt[0]

            # finds frequency with evenly spaced times
            freq = np.fft.fftshift(np.fft.fftfreq(np.size(dt), evenDt * 100))

            # calculates fft using reikna if pyCuda is found
            if found:
                shape = np.shape(preTransform)
                preTransform = np.complex128(preTransform)

                t2 = time.time()
                # sets api & creates thread if not preloaded
                if self.api is None:
                    print('api is None')
                    self.api = cluda.cuda_api()
                    self.thr = self.api.Thread.create()

                # creates new computation & recompiles if new input shape
                # if same as previous input shape, uses the stored function
                if not self.preCompShape == shape:
                    print('shape is new')
                    self.preCompShape = shape
                    lastAxis = len(shape) - 1
                    fft1 = fft.FFT(preTransform, axes=(lastAxis, ))
                    self.preCompFunc = fft1.compile(self.thr)
                    self.transformed_dev = self.thr.empty_like(preTransform)

                t3 = time.time()
                print('compile time: ', t3 - t2)

                # sends preTransform array to device
                t4 = time.time()
                pre_dev = self.thr.to_device(preTransform)
                t5 = time.time()
                print('sending pre to dev time: ', t5 - t4)

                # runs compiled function with output arr and input arr
                t6 = time.time()
                self.preCompFunc(self.transformed_dev, pre_dev)
                t7 = time.time()
                print('function time: ', t7 - t6)

                # retrieves and shifts transformed array
                t8 = time.time()
                transformed = self.transformed_dev.get()
                t9 = time.time()
                print('getting transformed from dev time: ', t9 - t8)
                transformed = np.abs(np.fft.fftshift(transformed, axes=-1))

                # checks reikna fft with numpy
                # transformed2 = np.abs(np.fft.fftshift(
                #     (np.fft.fft(preTransform)), axes=-1))
                # print(np.allclose(transformed, transformed2, atol = 1e-15))

            else:
                # uses np fft if no pyCuda found
                transformed = np.abs(np.fft.fftshift(
                    (np.fft.fft(preTransform)), axes=-1))

            # returns dictionary of frequency & output cube
            output = {'freq': freq, 'ftCube': transformed}
            t1 = time.time()
            print(t1-t0)
            return output

        return fftHelper(preTransform, transformed, dt, t)
