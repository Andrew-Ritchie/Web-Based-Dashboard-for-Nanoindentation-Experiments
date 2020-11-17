import numpy as np
import scipy.signal

class ContactPoint:
    
    def calculate(self, force, displacement, Athreshold=0, Fthreshold=0, deltax=2000.0):
        yth = Athreshold
        x = np.array(displacement)
        y = np.array(force)
        if yth > np.max(y) or yth < np.min(y): 
            return None
        jrov = 0
        for j in range(len(y)-1,1,-1): 
            if y[j]>yth and y[j-1]<yth: 
                jrov = j 
                break
        x0 = x[jrov]
        dx = deltax
        ddx = Fthreshold 
        if ddx <= 0: 
            jxalign = np.argmin((x - (x0 - dx)) ** 2)
            f0 = y[jxalign] 
        else:
            jxalignLeft = np.argmin( (x-(x0-dx-ddx))**2 )
            jxalignRight = np.argmin( (x-(x0-dx+ddx))**2 )
            f0 = np.average(y[jxalignLeft:jxalignRight])
        jcp = jrov
        for j in range(jrov,1,-1):
            if y[j]>f0 and y[j-1]<f0:
                jcp = j
                break
        return [x[jcp], y[jcp]]

class Filters:

    def savgol(self, force, displacement, zwin=30):
        x = np.array(displacement)
        y = np.array(force)
        zstep = (max(displacement) - min(displacement)) / (len(displacement) - 1)
        window_length = int(zwin/zstep)
        if (window_length % 2) == 0:
            window_length += 1 
        polyorder = 1

        return scipy.signal.savgol_filter(y, window_length, polyorder, deriv=0, delta=1.0, axis=- 1, mode='interp', cval=0.0)