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
from multiprocessing.dummy import Pool as ThreadPool

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
    Class that operates radiative transfer from BifrostData simulations
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
        self.found = found

    def use_gpu(self, choice):
        self.found = choice



    def threadTask(self, task, numThreads, *args):
        # split arg arrays
        args = list(args)

        for index in range(np.shape(args)[0]):
            args[index] = np.array_split(args[index], numThreads)

        # make threadpool, task = task, with zipped args
        pool = ThreadPool(processes=numThreads)
        result = np.concatenate(pool.map(task, args)[0])
        return result


    def get_fft(self, quantity, snap, numThreads=1, numBlocks=1, iix=None, iiy=None, iiz=None):
        """
        Calculates FFT (by calling fftHelper)

        Parameters
        ----------
        quantity - string
        snap - array or list
        numThreads - number of threads, not using PyCuda
        numBlocks - for use with PyCuda when GPU memory limited
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
        print('done with loading vars')

        # gets rid of array dimensions of 1
        preTransform = np.squeeze(preTransform)
        transformed = np.empty((preTransform.shape))
        dt = self.params['dt']
        t = self.params['t']

        t0 = time.time()

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

        if self.found:
            def singleRun(arr):
                    # results = np.abs(np.fft.fftshift(
                    #     (np.fft.fft(preTransform)), axes=-1))
                    # return results
                    shape = np.shape(arr)
                    print(shape)
                    preTransform = np.complex128(arr)

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
                        self.transformed_piece_dev = self.thr.empty_like(preTransform)

                    t3 = time.time()
                    print('compile time: ', t3 - t2)

                    # sends preTransform array to device
                    t4 = time.time()
                    pre_dev = self.thr.to_device(preTransform)
                    t5 = time.time()
                    print('sending pre to dev time: ', t5 - t4)

                    # runs compiled function with output arr and input arr
                    t6 = time.time()
                    self.preCompFunc(self.transformed_piece_dev, pre_dev)
                    t7 = time.time()
                    print('function time: ', t7 - t6)

                    # retrieves and shifts transformed array
                    t8 = time.time()
                    transformed_piece = self.transformed_piece_dev.get()
                    t9 = time.time()
                    print('getting transformed from dev time: ', t9 - t8)
                    transformed_piece = np.abs(np.fft.fftshift(transformed_piece, axes=-1), dtype = np.float128)

                    return transformed_piece
            
            # splitting up calculations for memory limitations
            if numBlocks > 1:
                splitList = np.array_split(preTransform, numBlocks, axis = 0)
                result = list(singleRun(splitList[0]))
                print(len(result))

                for arr in splitList[1:]:
                    addOn = singleRun(arr)
                    addLen = addOn.shape[0]
                    result = np.concatenate((result, addOn), axis = 0)

                transformed = result

            # calculates fft using reikna if pyCuda is found but numBlocks = 1
            else:
                transformed = singleRun(preTransform)

        # no pycuda found
        else:
            # threading
            if numThreads > 1:
                def task(arr):
                    transformed_piece = np.abs(np.fft.fftshift(
                        (np.fft.fft(arr)), axes=-1))
                    return transformed_piece

                transformed = self.threadTask(task, numThreads, preTransform)

            # single thread
            else:
                # uses np fft if no pyCuda found
                transformed = np.abs(np.fft.fftshift(
                    (np.fft.fft(preTransform)), axes=-1))

        # returns dictionary of frequency & output cube
        output = {'freq': freq, 'ftCube': transformed}
        t1 = time.time()
        print(t1-t0)
        return output

