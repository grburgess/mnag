from mnAfterglow.lcModel import lcModel
from multiFit.priorGen import *

from numpy import exp, power, zeros, log






class flare3(lcModel):


    def __init__(self):

        def m(t,A0,tauG,tauE,T0):

            val = zeros(len(t))

            A0 = power(10., A0)
            T0 = power(10., T0)
            tauG = power(10., tauG)
            tauE = power(10., tauE)
            

            
            cond = t<=T0

            val[cond] = exp(-(t[cond]-T0)**2/2*tauG**2)
            val[~cond]   = exp(-(t[~cond]-T0)/tauE)

            return A0 * val
       
    

        


        self.paramsRanges = [[1.E-20,1.E-1,"J"],[1E-3,1.E2,"J"],[1E-3,1E2,"J"],[1E0,1E7,"J"]]

        def plPrior(params, ndim, nparams):

            for i in range(ndim):
                params[i] = priorLU[self.paramsRanges[i][-1]](params[i],self.paramsRanges[i][0],self.paramsRanges[i][1])
            

        self.plOrder = -1
        self.modName = "flare3"
        self.model=m
        self.prior=plPrior
        self.n_params = 4
        self.parameters = [r"log(N$_{\rm flare2}$)",r"$\tau_{\rm g}$",r"$\tau_{\rm e}$",r"$T_{0}$"]


        self._modelDict = {"params":self.parameters,\
                         "model":m,\
                         "plOrder":self.plOrder,\
                      }
        self._composite = False
    
