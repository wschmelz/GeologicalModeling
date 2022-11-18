##define LOESS algorithm

def loess(x_interp,t_series_x,t_series_z,pt_min_r,dist_r,factor):
    import sys
    import numpy
    output = numpy.zeros(len(x_interp))
    
    for location in range(0,len(output)):
        new_z = "nan"
        x_est = x_interp[location]
        x_dists = x_est - t_series_x
        dists_all = numpy.absolute(x_dists)
        
        dist_sorted = numpy.argsort(dists_all)

        dist_indices = numpy.where((dists_all<dist_r))[0]
        dists_max = dist_r
        if dists_all[dist_sorted][pt_min_r] > dist_r :
            dist_indices = dist_sorted[0:pt_min_r]
            dists_max = numpy.max(dists_all[dist_indices])
            
        x_reg = x_dists[dist_indices]
        z_reg = t_series_z[dist_indices]

        dists = dists_all[dist_indices] 
                
        dists_norm = dists/dists_max
        
        ones = numpy.ones(len(dist_indices))
        if factor == 1:
            A = numpy.transpose(numpy.reshape(numpy.array([(ones), (x_reg)]),(2,-1)))
            w = ((1.0-(dists_norm**3.))**3.)
            w = numpy.reshape(w,(-1,1))
            A = A * numpy.repeat(w,2,1)
            
        if factor == 2:       
            A = numpy.transpose(numpy.reshape(numpy.array([(ones), (x_reg**2.), (x_reg)]),(3,-1)))
            w = ((1.0-(dists_norm**3.))**3.)
            w = numpy.reshape(w,(-1,1))
            A = A * numpy.repeat(w,3,1)
            
        b = numpy.reshape(w[:,0]*z_reg,(-1,1))

        new_x = numpy.linalg.lstsq(A, b,rcond=None)[0]

        new_z = numpy.reshape(numpy.array([new_x[0]]),(-1,1))

        output[location] = float(new_z)

        sys.stdout.write("\rLOESS Regression %i of %i complete:           " % (location+1,len(output)))
    
    sys.stdout.write("\rLOESS Regression complete                     ")
    print("")
    return output
