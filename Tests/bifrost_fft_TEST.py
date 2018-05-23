import numpy as np
import sys
# sys.path.append('/sanhome/baharav/helita/helita/sim')
import helita.sim.cstagger
from helita.sim.bifrost import BifrostData, Rhoeetab, read_idl_ascii
from helita.sim.bifrost_fft import FFTData
import matplotlib.pyplot as plt
from scipy import signal

# note: this calls bifrost_fft from user, not /sanhome

dd = FFTData(file_root = 'cb10f', fdir = '/net/opal/Volumes/Amnesia/mpi3drun/Granflux')
x = np.linspace(-np.pi, np.pi, 201)
dd.preTransform = np.sin(x)
dd.freq = np.fft.fftshift(np.fft.fftfreq(np.size(x)))
dd.run_gpu(False)
tester = dd.get_fft('not a real snap', snap = 0)
fig = plt.figure()

ax0 = fig.add_subplot(221)
ax0.plot(x, dd.preTransform)
ax0.set_title('original signal' + '\n\nsine wave')

ax1 = fig.add_subplot(222)
ax1.plot(tester['freq'], tester['ftCube'])
ax1.set_title('bifrost_fft get_fft() of signal' + '\n\n ft of sine wave')
ax1.set_xlim(-.2, .2)

n = 30000 # Number of data points
dx = .01 # Sampling period (in meters)
x2 = dx*np.linspace(-n/2 , n/2, n) # x coordinates

stanD = 2 # standard deviation
dd.preTransform = np.exp(-0.5 * (x2/stanD)**2)

# dd.preTransform = signal.gaussian(sampleSize, std = 7)
# f = signal.gaussian(n, std = stanD)
ax2 = fig.add_subplot(223)
ax2.plot(x2, dd.preTransform)
ax2.set_xlim(-25, 25)
ax2.set_title('gaussian curve')

dd.freq = np.fft.fftshift(np.fft.fftfreq(np.size(x2)))
ft = dd.get_fft('fake snap', snap = 0)
ax3 = fig.add_subplot(224)
ax3.plot(ft['freq'], ft['ftCube'])
ax3.set_xlim(-.03, .03)
ax3.set_title('ft of gaussian curve')

plt.tight_layout()
plt.show()
