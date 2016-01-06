from mnAfterglow.lcModel import lcModel
from multiFit.priorGen import *

from numpy import exp, power, zeros, logical_and






class pl5break(lcModel):


    def __init__(self):


        def pl(x, logA, i1, i2, i3,i4, i5, i6, b1, b2, b3, b4,b5):

            A = power(10., logA)
            pivot=1E3

            val = zeros(x.flatten().shape[0])

            b1=10**b1
            b2=10**b2
            b3=10**b3
            b4=10**b4
            b5=10**b5
            pl1 = x < b1 
            pl2 = logical_and( x >= b1 ,x < b2 )
            pl3 = logical_and( x >= b2 ,x < b3 )
            pl4 = logical_and( x >= b3 ,x < b4 )
            pl5 = logical_and( x >= b4 ,x < b5 )
            pl6 = x>= b5


#            x/=pivot
            norm1 = power(b1/pivot,i1-i2)
            norm2 = power(b2/pivot,i2-i3)
            norm3 = power(b3/pivot,i3-i4)
            norm4 = power(b4/pivot,i4-i5)
            norm5 = power(b5/pivot,i5-i6)

            val[pl1] = power(x[pl1]/pivot,i1)
            val[pl2] = norm1 * power(x[pl2]/pivot,i2)
            val[pl3] = norm1 * norm2  * power(x[pl3]/pivot,i3)
            val[pl4] = norm1 * norm2  * norm3  *power(x[pl4]/pivot,i4)
            val[pl5] = norm1 * norm2  * norm3 * norm4  *power(x[pl5]/pivot,i5)
            val[pl6] = norm1 * norm2  * norm3 * norm4 * norm5  *power(x[pl6]/pivot,i6)
            
            return A*val
    

        


        self.paramsRanges = [[1.E-20,1.E-1,"J"],[-8.,2,"U"],[-8.,2,"U"],[-8.,2,"U"],[-8.,2,"U"],[-8.,2,"U"],[-8.,2,"U"],[1E1,1E7,"J"],[1E1,1E7,"J"],[1E1,1E7,"J"],[1E1,1E7,"J"],[1E1,1E7,"J"]]

        def plPrior(params, ndim, nparams):

            for i in range(ndim):
                params[i] = priorLU[self.paramsRanges[i][-1]](params[i],self.paramsRanges[i][0],self.paramsRanges[i][1])
            

        self.plOrder = 5
        self.modName = "pl5break"
        self.model=pl
        self.prior=plPrior
        self.n_params = 12
        self.parameters = ["log(N)","i1","i2","i3","i4","i5","i6","b1","b2","b3","b4","b5"]

    
