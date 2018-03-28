import time
import numpy as np
from multiprocessing.dummy import Pool as ThreadPool

def proj_quant(arr1, arr2, proj):

	# the task that gets called by each thread
	def task(arr1, arr2):
		# print('calling task', arr1, arr2)
		x1 = arr1[:, :, :, 0]
		y1 = arr1[:, :, :, 1]
		z1 = arr1[:, :, :, 2]
		x2 = arr2[:, :, :, 0]
		y2 = arr2[:, :, :, 1]
		z2 = arr2[:, :, :, 2]

		v2Mag = np.sqrt(x2**2 + y2**2 + z2**2)
		v2x, v2y, v2z = x2 / v2Mag, y2 / v2Mag, z2 / v2Mag
		parScal = x1 * v2x + y1 * v2y + z1 * v2z
		parX, parY, parZ = parScal * v2x, parScal * v2y, parScal * v2z
		results = np.abs(parScal)

		if proj == 'per':
			perX = x1 - parX
			perY = y1 - parY
			perZ = z1 - parZ

			v1Mag = np.sqrt(perX**2 + perY**2 + perZ**2)
			result = v1Mag

		print('results shape: ', np.shape(results))
		return results

	# creating thread pool
	nofThreads = 10
	pool = ThreadPool(processes = nofThreads)

	# splitting arrays up into number of chunks of threads
	arrChunks1 = np.array_split(arr1, nofThreads)
	arrChunks2 = np.array_split(arr2, nofThreads)

	# putting together results of threads to get the total result
	t0 = time.time()
	results1 = np.concatenate(pool.starmap(task, zip(arrChunks1, arrChunks2)))
	t1 = time.time()
	print('starmap time: ', t1 - t0)
	results3 = task(arr1, arr2)
	t2 = time.time()
	print('regular time: ', t2 - t1)

	# comparing the multithreading result to the single thread result
	print('results1 is correct: ', np.all(results1 == results3))

arr1 = np.arange(375000000).reshape(500, 500, 500, 3)
arr2 = np.arange(375000000, 750000000).reshape(500, 500, 500, 3)

proj_quant(arr1, arr2, 'per')


