"""
Set of programs to read and interact with output from BifrostData simulations focusing on Fourier transforms
"""
import time
import numpy as np
import os
from .bifrost import BifrostData, Rhoeetab, read_idl_ascii, subs2grph, bifrost_units
from . import cstagger

# from glob import glob
# import scipy as sp
# import imp
# import scipy.ndimage as ndimage

# try:
#     imp.find_module('pycuda')
#     found = True
# except ImportError:
#     found = False

class FFTData(BifrostData):

    """
    Class that operates radiative transfer form BifrostData simulations
    in native format.
    """

    def __init__(self, *args, **kwargs):
        super(FFTData, self).__init__(*args, **kwargs)


    def get_fft(self, quantity, snap, iix = None, iiy = None, iiz = None):

        preTransform = self.get_varTime(quantity, snap, iix, iiy, iiz)
        print(np.shape(preTransform))
        arrShape = preTransform.shape
        indexes = []

        for num in arrShape:
            if num == 1:
                indexes.append(0)
            else:
                indexes.append(slice(None))

        preTransform = preTransform[indexes[0], indexes[1], indexes[2], indexes[3]]
        transformed = np.empty((preTransform.shape))
        dt = self.params['dt']
        t = self.params['t']

        t0 = time.time()
        # @numba.jit(['float64[:, :, ::1](float64[:, :, ::1], float64[:, :, ::1], float64[::1], float64[::1])'])
        def fftHelper(preTransform, transformed, dt, t):

            uneven = False
            for i in range(1, np.size(dt) - 1):
                if abs((t[i] - t[i -1]) - (t[i+1] - t[i])) > 0.02:
                    uneven = True
                    break

            if uneven:
                print('uneven dt')
                evenTimes = np.linspace(t[0], t[-1], np.size(dt))
                interp = sp.interpolate.interp1d(t, preTransform)
                preTransform = interp(evenTimes)
                evenDt = evenTimes[1] - evenTimes[0]
            else:
                evenDt = dt[0]

            freq = np.fft.fftshift(np.fft.fftfreq(np.size(dt), evenDt * 100))
            transformed = np.abs(np.fft.fftshift((np.fft.fft(preTransform)), axes = -1))
            output = {'freq': freq, 'ftCube': transformed}
            t1 = time.time()
            print(t1-t0)
            return output

        return fftHelper(preTransform, transformed, dt, t)
