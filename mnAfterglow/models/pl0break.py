from mnAfterGlow.lcModel import lcModel
from multiFit.priorGen import *

from numpy import exp, power, zeros






class pl0break(lcModel):


    def __init__(self):


        def pl(x, logA, i1,):

            A = power(10., logA)
            pivot=1E3
            
            val = power(x/pivot,i1)

            
            return A*val
    

        


        self.paramsRanges = [[1.E-20,1.E-1,"J"],[-8.,2,"U"]]

        def plPrior(params, ndim, nparams):

            for i in range(ndim):
                params[i] = priorLU[self.paramsRanges[i][-1]](params[i],self.paramsRanges[i][0],self.paramsRanges[i][1])
            

        self.plOrder = 0
        self.modName = "pl0break"
        self.model=pl
        self.prior=plPrior
        self.n_params = 2
        self.parameters = ["log(N0)","i1"]

        self._modelDict = {"params":self.parameters,\
                            "model":pl,\
                            "plOrder":self.plOrder,\
                            }
        self._composite = False
