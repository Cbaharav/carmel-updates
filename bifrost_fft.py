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

    def __init__(self, verbose=False, *args, **kwargs):
        print(kwargs)
        print(verbose)

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
        self.verbose = verbose

    def run_gpu(self, choice=True):
        '''
        activates the module that uses CUDA
        '''
        if self.found:
            self.use_gpu = choice
        else:
            self.use_gpu = False

    def singleCudaRun(self, arr):

        shape = np.shape(arr)
        if self.verbose:
            print(shape)
        preTransform = np.complex128(arr)

        t2 = time.time()
        # sets api & creates thread if not preloaded
        if self.api is None:
            if self.verbose:
                print('api is None')
            self.api = cluda.cuda_api()
            self.thr = self.api.Thread.create()

        # creates new computation & recompiles if new input shape
        # if same as previous input shape, uses the stored function
        if not self.preCompShape == shape:
            if self.verbose:
                print('shape is new')
            self.preCompShape = shape
            lastAxis = len(shape) - 1
            fft1 = fft.FFT(preTransform, axes=(lastAxis, ))
            self.preCompFunc = fft1.compile(self.thr)
            self.transformed_piece_dev = self.thr.empty_like(preTransform)

        # sends preTransform array to device
        t3 = time.time()
        pre_dev = self.thr.to_device(preTransform)
        t4 = time.time()

        # runs compiled function with output arr and input arr
        self.preCompFunc(self.transformed_piece_dev, pre_dev)
        t5 = time.time()

        # retrieves and shifts transformed array
        transformed_piece = self.transformed_piece_dev.get()
        t6 = time.time()

        if self.verbose:
            print('compile time: ', t3 - t2)
            print('sending pre to dev time: ', t4 - t3)
            print('function time: ', t5 - t4)
            print('getting transformed from dev time: ', t6 - t5)
        transformed_piece = np.abs(np.fft.fftshift(
            transformed_piece, axes=-1), dtype=np.float128)

        return transformed_piece

    def pre_fft(self, quantity, snap, iix=None, iiy=None, iiz=None):

        self.preTransform = self.get_varTime(quantity, snap, iix, iiy, iiz)
        if self.verbose:
            print('done with loading vars')

        # gets rid of array dimensions of 1
        self.preTransform = np.squeeze(self.preTransform)
        dt = self.params['dt']
        t = self.params['t']

        # checking to see if time gap between snaps is consistent
        uneven = False
        for i in range(1, np.size(dt) - 1):
            if abs((t[i] - t[i - 1]) - (t[i+1] - t[i])) > 0.02:
                uneven = True
                break

        # interpolates data if time gaps are uneven
        if uneven:
            if self.verbose:
                print('uneven dt')
            evenTimes = np.linspace(t[0], t[-1], np.size(dt))
            interp = sp.interpolate.interp1d(t, self.preTransform)
            self.preTransform = interp(evenTimes)
            evenDt = evenTimes[1] - evenTimes[0]
        else:
            evenDt = dt[0]

        # finds frequency with evenly spaced times
        self.freq = np.fft.fftshift(np.fft.fftfreq(np.size(dt), evenDt * 100))

    def get_fft(self, quantity, snap, numThreads=1, numBlocks=1,
                iix=None, iiy=None, iiz=None, test=False):
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
        if not (test and self.hasattr(preTransform)):
            self.pre_fft(quantity, snap, iix, iiy, iiz)

        t0 = time.time()

        if self.use_gpu:
            # splitting up calculations for memory limitations
            if numBlocks > 1:
                splitList = np.array_split(
                    self.preTransform, numBlocks, axis=0)
                result = list(self.singleCudaRun(splitList[0]))
                if self.verbose:
                    print(len(result))

                for arr in splitList[1:]:
                    addOn = self.singleCudaRun(arr)
                    addLen = addOn.shape[0]
                    result = np.concatenate((result, addOn), axis=0)

                transformed = result

            # calculates fft using reikna if pyCuda is found but numBlocks = 1
            else:
                transformed = self.singleCudaRun(self.preTransform)

        # no pycuda found
        else:
            # threading
            if numThreads > 1:
                def task(arr):
                    transformed_piece = np.abs(np.fft.fftshift(
                        (np.fft.fft(arr)), axes=-1))
                    return transformed_piece

                transformed = threadTask(task, numThreads, self.preTransform)

            # single thread
            else:
                # uses np fft if no pyCuda found
                transformed = np.abs(np.fft.fftshift(
                    (np.fft.fft(self.preTransform)), axes=-1))

        # returns dictionary of frequency & output cube
        output = {'freq': self.freq, 'ftCube': transformed}
        t1 = time.time()
        if self.verbose:
            print('total time: ', t1-t0)
        return output


def threadTask(task, numThreads, *args):
    # split arg arrays
    args = list(args)

    for index in range(np.shape(args)[0]):
        args[index] = np.array_split(args[index], numThreads)

    # make threadpool, task = task, with zipped args
    pool = ThreadPool(processes=numThreads)
    result = np.concatenate(pool.map(task, args)[0])
    return result
