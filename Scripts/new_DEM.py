import numpy
import scipy
from scipy import interpolate

def new_DEM(x,y,z,cellsize):
	x_max = numpy.max(x)
	x_min = numpy.min(x)
	y_max = numpy.max(y)
	y_min = numpy.min(y)
	new_x = numpy.arange(x_min,x_max+cellsize,cellsize)
	new_y = numpy.arange(y_min,y_max+cellsize,cellsize)
	xy_array = numpy.append(numpy.reshape(new_x,(1,-1)),numpy.reshape(new_y,(1,-1)),axis=1)
	X, Y = numpy.meshgrid(new_x, new_y)
	Z = interpolate.griddata(xy_array, z, (X, Y), method='linear')
	return X,Y,Z