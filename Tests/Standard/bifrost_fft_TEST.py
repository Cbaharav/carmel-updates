import numpy as np
import helita.sim.cstagger
from helita.sim.bifrost import BifrostData, Rhoeetab, read_idl_ascii
from helita.sim.bifrost_fft import FFTData
import matplotlib.pyplot as plt

# note: this calls bifrost_fft from user, not /sanhome

dd = FFTData(file_root='cb10f',
             fdir='/net/opal/Volumes/Amnesia/mpi3drun/Granflux')

# test 1: ft of y = sin(8x)
x = np.linspace(-np.pi, np.pi, 201)
dd.preTransform = np.sin(8 * x)
dd.freq = np.fft.fftshift(np.fft.fftfreq(np.size(x)))
dd.run_gpu(False)
# preTransform is already set
tester = dd.get_tfft('not a real var', snap='test')
fig = plt.figure()

numC = 3
numR = 2

# plotting original sin signal
ax0 = fig.add_subplot(numC, numR, 1)
ax0.plot(x, dd.preTransform)
ax0.set_title('original signal' + '\n\nsine wave')

# plotting transformation sin  signal
ax1 = fig.add_subplot(numC, numR, 2)
ax1.plot(tester['freq'], tester['ftCube'])
ax1.set_title('bifrost_fft get_fft() of signal' + '\n\n ft of sine wave')
ax1.set_xlim(-.2, .2)

# test 2: ft of gaussian curve
n = 30000  # Number of data points
dx = .01  # Sampling period (in meters)
x = dx*np.linspace(-n/2, n/2, n)  # x coordinates

stanD = 2  # standard deviation
dd.preTransform = np.exp(-0.5 * (x/stanD)**2)

# plotting original gaussian signal
ax2 = fig.add_subplot(numC, numR, 3)
ax2.plot(x, dd.preTransform)
ax2.set_xlim(-25, 25)
ax2.set_title('gaussian curve')

# plotting transformation of gaussian signal
dd.freq = np.fft.fftshift(np.fft.fftfreq(np.size(x)))
ft = dd.get_tfft('not a real var', snap='test')  # preTransform is already set
ax3 = fig.add_subplot(numC, numR, 4)
ax3.plot(ft['freq'], ft['ftCube'])
ax3.set_xlim(-.03, .03)
ax3.set_title('ft of gaussian curve')

# test 3: ft of y = 0
# plotting original horizontal line
x = np.linspace(-20, 20, 50)
dd.preTransform = [0] * 50
ax4 = fig.add_subplot(numC, numR, 5)
ax4.plot(x, dd.preTransform)
ax4.set_title('y = 0')

# plotting transformed signal
dd.freq = np.fft.fftshift(np.fft.fftfreq(np.size(x)))
ft = dd.get_tfft('not a real var', snap='test')  # preTransform is already set
ax5 = fig.add_subplot(numC, numR, 6)
ax5.plot(ft['freq'], ft['ftCube'])
ax5.set_title('ft of y = 0')

plt.tight_layout()
plt.show()
