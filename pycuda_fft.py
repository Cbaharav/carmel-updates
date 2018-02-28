import numpy as np
from reikna import cluda
from reikna.core import Transformation, Parameter, Annotation, Type
from reikna.cluda import dtypes
from reikna.fft import fft
from reikna.cluda.tempalloc import TrivialManager
import pyopencl as cl

tr = Transformation(
	[
		Parameter('in_re', Annotation(Type(np.float64))),
		Parameter('out_c', Annotation(Type(np.complex64)))
	],
	"""
	derive_o_from_is = lambda in_re:dtypes.complex_for(in_re);
	${out_c.store}(COMPLEX_CTR(${out_c.ctype})(${in_re.load}, 0));)
	"""
	)

# def main():
platforms = cl.get_platforms()
ctx = cl.Context(dev_type = cl.device_type.GPU, properties=[(cl.context_properties.PLATFORM, platforms[0])])
api = cluda.ocl_api()
thr = api.Thread.create(temp_alloc = dict(cls = TrivialManager), device_type = cl.device_type.GPU)

N = 256
M = 10000

data_in = np.random.rand(N)
data_in = data_in.astype(np.float32)

cl_data_in = thr.to_device(data_in)
cl_data_out = thr.array(data_in.shape, np.complex64)

fft = FFT(thr)
fft.connect(tr, 'input', ['input_re'])
fft.prepare_for(cl_data_out, cl_data_in, -1, axes = (-1,))