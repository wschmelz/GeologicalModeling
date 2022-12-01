##define moving average algorithm

import numpy

def m_avg(x_new,x_orig,y_orig,span):
	output = numpy.zeros(len(x_new))*numpy.nan
	for n in range(0,len(x_new)):
		#set interpolation value
		t_interp = x_new[n]
		
		#find all data values where data is within specified "window" relative to interpolation value
		w1 = numpy.where(numpy.absolute(x_orig - t_interp) < span)[0]
		
		output[n] = numpy.mean(y_orig[w1])
	
	return output