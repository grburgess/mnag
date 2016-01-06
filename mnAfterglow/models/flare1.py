from mnAfterGlow.lcModel import lcModel
from multiFit.priorGen import *

from numpy import exp, power, zeros, log






class flare1(lcModel):


    def __init__(self):


        def fl(x, logA, S,M):

            M = power(10.,M)
            A = power(10., logA)
            M = log(M)
            
            val = (1./(S*x)) * exp( -(log(x) - M)* (log(x) - M) / (2*S*S)  )

            
            return A*val
    

        


        self.paramsRanges = [[1.E-20,1.E-1,"J"],[1E-2,1.E2,"J"],[1E1,1E7,"J"]]

        def plPrior(params, ndim, nparams):

            for i in range(ndim):
                params[i] = priorLU[self.paramsRanges[i][-1]](params[i],self.paramsRanges[i][0],self.paramsRanges[i][1])
            

        self.plOrder = -1
        self.modName = "flare1"
        self.model=fl
        self.prior=plPrior
        self.n_params = 3
        self.parameters = [r"log(N$_{\rm flare}$)","S","M"]


        self._modelDict = {"params":self.parameters,\
                         "model":fl,\
                         "plOrder":self.plOrder,\
                      }
        self._composite = False
    
