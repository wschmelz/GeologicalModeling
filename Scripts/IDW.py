##define inverse distance weighted algorithm

import numpy

def IDW(x_new,x_orig,y_orig,span,factor):
    
    #pre-allocate memory
    output = numpy.zeros(len(x_new))*numpy.nan
    
    for n in range(0,len(x_new)):
        x_interp_val = x_new[n]
        w1 = numpy.where((numpy.absolute(x_orig - x_interp_val)<span)&(numpy.absolute(x_orig - x_interp_val)>0.))[0]
        output[n] = numpy.sum(y_orig[w1]/(numpy.absolute(x_orig[w1] - x_interp_val)**factor))/numpy.sum(1./(numpy.absolute(x_orig[w1] - x_interp_val)**factor))
   
    return output