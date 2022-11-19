def corr_coeff(x1,x2):
	import numpy
	N = len(x1)	mean_x1 = numpy.mean(x1)	mean_x2 = numpy.mean(x2)	stdev_x1 = numpy.std(x1)	stdev_x2 = numpy.std(x2)
	cov_tmp = (1./(N-1)) * numpy.sum((x1-mean_x1)*(x2-mean_x2))	r_tmp = cov_tmp/(stdev_x1*stdev_x2)
	return r_tmp