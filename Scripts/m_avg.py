##define moving average algorithm

import numpy

def m_avg(x,y,span):
	output = numpy.zeros(len(x))*numpy.nan
	for n in range(0,len(x)):
		#set interpolation value
		t_interp = x[n]
		
		#find all data values where data is within specified "window" relative to interpolation value
		w1 = numpy.where(numpy.absolute(x - t_interp) < span)[0]
		
		output[n] = numpy.mean(y[w1])
	
	return output