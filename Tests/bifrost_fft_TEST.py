from bifrost_fft import FFTData
import numpy as np
#does not work, issue with relative imports in bifrost_fft and bifrost

dd = FFTData(file_root = 'cb10f', fdir = '/net/opal/Volumes/Amnesia/mpi3drun/Granflux')
x = np.linspace(-np.pi, np.pi, 201)
dd.preTransform = np.sin(x)
dd.freq = np.fft.fftshift(np.fft.fftfreq(np.size(x)))
dd.run_gpu(False)
print(dd.get_fft('o', snap = 2))