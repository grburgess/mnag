from mnAfterGlow.lcModel import lcModel
from multiFit.priorGen import *

from numpy import exp, power, zeros, logical_and






class pl3break(lcModel):


    def __init__(self):


        def pl(x, logA, i1, i2, i3,i4 ,b1, b2, b3):

            A = power(10., logA)
            pivot=1E3

            b1=10**b1
            b2=10**b2
            b3=10**b3
            val = zeros(x.flatten().shape[0])



            pl1 = x < b1 
            pl2 = logical_and( x >= b1 ,x < b2 )
            pl3 = logical_and( x >= b2 ,x < b3 )
            pl4 = x>= b3

#            x/=pivot
            
            norm1 = power(b1/pivot,i1-i2)
            norm2 = power(b2/pivot,i2-i3)
            norm3 = power(b3/pivot,i3-i4)

            val[pl1] = power(x[pl1]/pivot,i1)
            val[pl2] = norm1 * power(x[pl2]/pivot,i2)
            val[pl3] = norm1 * norm2  * power(x[pl3]/pivot,i3)
            val[pl4] = norm1 * norm2  * norm3  *power(x[pl4]/pivot,i4)
            
            return A*val
    

        


        self.paramsRanges = [[1.E-20,1.E-1,"J"],[-8.,2,"U"],[-8.,2,"U"],[-8.,2,"U"],[-8.,2,"U"],[1E1,1E7,"J"],[1E1,1E7,"J"],[1E1,1E7,"J"]]

        def plPrior(params, ndim, nparams):

            for i in range(ndim):
                params[i] = priorLU[self.paramsRanges[i][-1]](params[i],self.paramsRanges[i][0],self.paramsRanges[i][1])
            

        self.plOrder = 3
        self.modName = "pl3break"
        self.model=pl
        self.prior=plPrior
        self.n_params = 8
        self.parameters = ["log(N)","i1","i2","i3","i4","b1","b2","b3"]

        self._modelDict = {"params":self.parameters,\
                            "model":pl,\
                            "plOrder":self.plOrder,\
                            }
        self._composite = False

    
