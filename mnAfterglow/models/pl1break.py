from mnAfterGlow.lcModel import lcModel
from multiFit.priorGen import *

from numpy import exp, power, zeros






class pl1break(lcModel):


    def __init__(self):


        def pl(x, logA, i1, i2, b1):

            A = power(10., logA)
            b1=10**b1
            pivot=1E3

            val = zeros(x.flatten().shape[0])



            pl1 = x < b1 
            pl2 = x >= b1

            #x/=pivot
            
            norm1 = power(b1/pivot,i1-i2)

            val[pl1] = power(x[pl1]/pivot,i1)
            val[pl2] = norm1 * power(x[pl2]/pivot,i2)
            
            return A*val
    

        


        self.paramsRanges = [[1.E-20,1.E-1,"J"],[-8.,2,"U"],[-8.,2,"U"],[1E1,1E7,"J"]]

        def plPrior(params, ndim, nparams):

            for i in range(ndim):
                params[i] = priorLU[self.paramsRanges[i][-1]](params[i],self.paramsRanges[i][0],self.paramsRanges[i][1])
            

        self.plOrder = 1
        self.modName = "pl1break"
        self.model=pl
        self.prior=plPrior
        self.n_params = 4
        self.parameters = ["log(N)","i1","i2","b1"]
        self._modelDict = {"params":self.parameters,\
                            "model":pl,\
                            "plOrder":self.plOrder,\
                            }
        self._composite = False
    
