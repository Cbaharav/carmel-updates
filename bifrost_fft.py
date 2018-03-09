"""
Set of programs to read and interact with output from BifrostData simulations focusing on Fourier transforms
"""
import time
import numpy as np
import os
from .bifrost import BifrostData, Rhoeetab, read_idl_ascii, subs2grph, bifrost_units
from . import cstagger
import imp

# from glob import glob
# import scipy as sp
# import scipy.ndimage as ndimage

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
        self.preCompFunc = None
        self.preCompShape = None
        self.transformed_dev = None
        self.api = None
        self.thr = None


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

            if found:
                shape = np.shape(preTransform)
                preTransform = np.complex128 (preTransform)

                tr = time.time()
                if self.api is None:
                    print('api is None')
                    self.api = cluda.cuda_api()
                    self.thr = self.api.Thread.create()

                if not self.preCompShape == shape:
                    print('shape is new')
                    self.preCompShape = shape
                    lastAxis = len(shape) - 1
                    fft1 = fft.FFT(preTransform, axes = (lastAxis, ))
                    self.preCompFunc = fft1.compile(self.thr)
                    self.transformed_dev = self.thr.array(shape, dtype = np.complex128)                 
                    # self.preCompFunc(transformed_dev, pre_dev)
                tl = time.time()
                print('compile time: ', tl - tr)

                tz = time.time()
                pre_dev = self.thr.to_device(preTransform)
                ty = time.time()
                print('pre_dev time: ', ty - tz)

                tq = time.time()
                self.preCompFunc(self.transformed_dev, pre_dev)
                tw = time.time()
                print('function time: ', tw - tq)

                th = time.time()
                transformed = self.transformed_dev.get()
                tp = time.time()
                print('getting transformed time: ', tp - th)
                transformed = np.abs(np.fft.fftshift(transformed, axes = -1))

                # shows that fft with reikna returns the same values as the numpy fft
                # transformed2 = np.abs(np.fft.fftshift(np.fft.fft(preTransform), axes = -1))
                # print(np.allclose(transformed, transformed2, atol = 1e-15))

            else:
                transformed = np.abs(np.fft.fftshift((np.fft.fft(preTransform)), axes = -1))
            output = {'freq': freq, 'ftCube': transformed}
            t1 = time.time()
            print(t1-t0)
            return output

        return fftHelper(preTransform, transformed, dt, t)
