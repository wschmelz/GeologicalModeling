def corr_coeff(x1,x2):
	import numpy
	N = len(x1)
	cov_tmp = (1./(N-1)) * numpy.sum((x1-mean_x1)*(x2-mean_x2))
	return r_tmp