import numpy

def lag1_cov(y):
    cov = (1./(len(y)-1.))*numpy.sum(((y[0:-1]-numpy.mean(y[0:-1]))*(y[1:]-numpy.mean(y[1:])))/numpy.var(y))
    return cov
	
def red_noise(y):
			
	red_noise_tmp = numpy.zeros(len(y))
	r = lag1_cov(y)

	white_noise = numpy.random.normal(0.,numpy.std(y),len(y))#* numpy.std(y)
	red_noise_tmp[0] =white_noise[0]
	for index_n in range(0,len(red_noise_tmp)-1):
		red_noise_tmp[index_n+1] =  r * red_noise_tmp[index_n] + numpy.sqrt(1.-(r**2.))*white_noise[index_n+1]

	return red_noise_tmp 
