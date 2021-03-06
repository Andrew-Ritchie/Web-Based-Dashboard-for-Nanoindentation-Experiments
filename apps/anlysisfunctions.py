import numpy as np
import scipy.signal
from scipy.optimize import curve_fit


class ContactPoint:
    
    def calculate(self, force, displacement, Athreshold=10, Fthreshold=100.0, deltax=2000.0):
        """
        Returns the calculated contact point

        :type force: array
        :param force: force data from FD curve

        :type displacement: array
        :param displacement: displacement data from FD curve
        
        :type Athreshold: int
        :param Athreshold: Athreshold data determined by the user

        :type Fthreshold: int
        :param Fthreshold: Fthreshold data determined by the user

        :type deltax: int
        :param deltax: deltax data determined by the user
        """
        yth = Athreshold
        x = np.array(displacement)
        y = np.array(force)
        if yth > np.max(y) or yth < np.min(y): 
            print('THIS HAPPNED')
            print(np.max(y), np.min(y), yth)
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
        #print(x[jcp], y[jcp])
        return [x[jcp], y[jcp], jcp]

class Filters:

    def savgol(self, force, displacement, zwin=21):
        """
        Returns the calculated contact point

        :type force: array
        :param force: force data from FD curve

        :type displacement: array
        :param displacement: displacement data from FD curve
        
        :type zwin: int
        :param zwin: window value of the filter determined by the user

        """
        x = np.array(displacement)
        y = np.array(force)
        zstep = (max(displacement) - min(displacement)) / (len(displacement) - 1)
        window_length = int(zwin/zstep)
        if (window_length % 2) == 0:
            window_length += 1 
        polyorder = 1

        return scipy.signal.savgol_filter(y, window_length, polyorder, deriv=0, delta=1.0, axis=- 1, mode='interp', cval=0.0)

class YoungsModulus:

    def calculate_indentation(self, force, displacement, cpindex, k=0.032):
        """
        Returns the calculated contact point

        :type force: array
        :param force: force data from FD curve

        :type displacement: array
        :param displacement: displacement data from FD curve
        
        :type cpindex: int
        :param cpindex: the index of the contact point value

        :type k: int
        :param k: the elastic constant value of the cantilever
        """
        indentation = []

        for value in range(cpindex, len(force)):
            indentation.append((displacement[value] - displacement[cpindex]) - ((force[value]/k) - (force[cpindex]/k)))
        
        print(indentation)
        return indentation
    
    def fitHertz(self, indentation, force, cpindex, tipradius=8000, fit_indentation_value=300.0):
        """
        Returns the calculated contact point

        :type indentation: array
        :param indentation: indentation data from FD curve

        :type force: array
        :param force: force data from FD curve
        
        :type cpindex: int
        :param cpindex: the index of the contact point value

        :type tipradius: int
        :param tipradius: the radius of the indenters tip

        :type fit_indentation_value: int
        :param fit_indentation_value: the size of the section of the FD curve to be analysed
        """
        contactforce = np.array(force[cpindex:]) - force[cpindex]
        print(contactforce, 'contact force')
        ind = np.array(indentation)
        seeds = [1000.0 / 1e9]
        try:
            R = tipradius

            def Hertz(x, E):
                x = np.abs(x)
                poisson = 0.5
                # Eeff = E*1.0e9 #to convert E in GPa to keep consistency with the units nm and nN
                return (4.0 / 3.0) * (E / (1 - poisson ** 2)) * np.sqrt(R * x ** 3)

            indmax = float(fit_indentation_value)
            jj = np.argmin((ind-indmax)**2)
            if jj < 5:
                return
            popt, pcov = curve_fit(Hertz, ind[:jj], contactforce[:jj], p0=seeds, maxfev=100000)



            #E_std = np.sqrt(pcov[0][0])
            #return Elatic Modulus
            return popt[0]*1e9
        except (RuntimeError, ValueError):
            return


