import time
import numpy as np
from reikna import cluda
from reikna.fft import fft
from numpy.linalg import norm

#reikna fft only works with complex numbers
dtype = np.complex64

#getting the cuda api
api = cluda.cuda_api()
thr = api.Thread.create()

shape = (100, 100, 100, 3)

#sending the array from host to array and creating result array on device
a = np.random.randn(*shape).astype(dtype)
a_dev = thr.to_device(a)
res_dev = thr.array(shape, dtype = dtype)

#reikna version of fft (compilation sends it to the thread)
lastAxis = len(shape) - 1
t0 = time.time()
fft = fft.FFT(a, axes = (lastAxis,))
fftc = fft.compile(thr)
fftc(res_dev, a_dev)
t1 = time.time()
print('Time 1: ', t1 - t0)

#tried to run compiled fft function with different input (it didn't work -- the output stayed the same)
t4 = time.time()
b = np.random.randn(*shape).astype(dtype)
b_dev = thr.to_device(a)
fftc(res_dev, b_dev)
t5 = time.time()
print('Time 1.5: ', t5 - t4)

#numpy fft to check
t2 = time.time()
res_reference = np.fft.fft(a, axis = lastAxis)
t3 = time.time()
print('Time 2: ', t3 - t2)


print(np.max(res_dev.get() - res_reference))
print(norm(res_dev.get() - res_reference) / norm(res_reference) < 1e-6)

