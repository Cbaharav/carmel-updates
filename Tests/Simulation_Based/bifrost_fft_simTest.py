import numpy as np
import helita.sim.cstagger
from helita.sim.bifrost import BifrostData, Rhoeetab, read_idl_ascii
from helita.sim.bifrost_fft import FFTData
import matplotlib.pyplot as plt

snaps = np.arange(280, 360)
v = 'bx'

dd = FFTData(file_root='l2d90x40r_it',
             fdir='/net/opal/Volumes/Amnesia/mpi3drun/2Druns/genohm/rain/l2d90x40r/', verbose=True)

# getting ft
transformed = dd.get_fft(v, snaps)
print('got fft')
ft = transformed['ftCube']
freq = transformed['freq']
zaxis = dd.z
print(np.shape(ft))
# making empty array to later contain the avergaes for each z position
zstack = np.empty([np.size(freq), np.shape(ft)[1]])
# filling ztack with average ft for each (x,y) in each z level
for k in range(0, np.shape(ft)[1]):
    avg = np.average(ft[:, k, :], axis=(0))
    zstack[:, k] = avg

# preparing plots
fig = plt.figure()
numC = 2
numR = 1

# ploting freq vs amp with multiple lines (1 for each z position)
ax0 = fig.add_subplot(numC, numR, 1)
ax0.plot(freq, zstack)
ax0.set_xlabel('Frequency')
ax0.set_ylabel('Amplitude')
ax0.set_title(
    'Average Amplitude of FT Frequencies at Different Z Positions (1)')
ax0.set_aspect('auto')

# plotting amp at different freq & z with image
ax1 = fig.add_subplot(numC, numR, 2)
ax1.imshow(zstack.transpose(), extent=[freq[0], freq[-1], zaxis[0], zaxis[-1]])
ax1.set_xlabel('Frequency')
ax1.set_ylabel('Z Position')
ax1.set_title(
    'Average Amplitude of FT Frequencies at Different Z Positions (2)')
ax1.set_aspect('auto')
plt.tight_layout()
plt.show()
