

from multiFit.priorGen import *

class lcModel(object):


    def __init__(self):





        self.prior = None
        self.n_params = None
        self.likelihood = None
        self.plOrder = None


    def __add__(self,other):
        '''
        Overloads the + operator for adding models.
        The user does't actaully need this functionality
        because it is handled in mnSpecFit when a list of models
        is passed
        
        '''



        #Instantiate a new Model()
        NewModel = lcModel()
        NewModel._composite = True #This will be a composite model so flag it

        duplicate = False #So far we don't know if the two models we are adding together are the same
        
        

        
        #Check if the current model is a composite
        if self._composite: #If it is then we can simply add the added models dictionary to this model

            NewModel.componentLU = self.componentLU

            #Need to check of this model already exists in the LU
            newKey = other.modName
            dupes = 0
            for key in NewModel.componentLU.keys():
                if newKey in key:
                    dupes+=1

            if dupes>0:
                newKey+="_%d"%(dupes+1)
                duplicate = True
                dupeParams = map(lambda x: x+"_%d"%(dupes+1),other.parameters)
                newOtherDict = other._modelDict
                newOtherDict["params"] = dupeParams
                NewModel.componentLU[newKey] = newOtherDict
            else:
                NewModel.componentLU[newKey]=other._modelDict
            

        
        else: #If not then we will have to create one

            if self.modName == other.modName:

                
                dupes=1
                newKey=self.modName+"_%d"%(dupes+1)
                dupeParams = map(lambda x: x+"_%d"%(dupes+1),other.parameters)
                
                newOtherDict = other._modelDict
                newOtherDict["params"] = dupeParams
                
                
                NewModel.componentLU={self.modName:self._modelDict,\
                                      other.modName+"_%d"%(dupes+1):other._modelDict\
                                  }
                NewModel.componentLU[newKey] = newOtherDict
                duplicate = True
            
            else:
                NewModel.componentLU={self.modName:self._modelDict,\
                                      other.modName:other._modelDict\
                                  }
                


        
        self.orig_n_params = self.n_params
        NewModel.modName=self.modName+"+"+other.modName
        NewModel.paramsRanges = self.paramsRanges +other.paramsRanges
        NewModel.n_params =  self.n_params + other.n_params

        if duplicate:
            dupeParams = map(lambda x: x+"_%d"%(dupes+1),other.parameters)
            
            NewModel.parameters = self.parameters + dupeParams
        else:
            NewModel.parameters = self.parameters + other.parameters
        def newPrior(params,ndim,nparams):
            for i in range(ndim):
                params[i] = priorLU[NewModel.paramsRanges[i][-1]](params[i],NewModel.paramsRanges[i][0],NewModel.paramsRanges[i][1])

        NewModel.prior = newPrior
        NewModel.origMod = self.model
        NewModel.otherMod = other.model
        def newModel(*args):

#            print self.orig_n_params
#            print NewModel.n_params
#            print args
            ene = args[0]
            thisParam = args[1:self.orig_n_params+1]
            otherParam = args[1+self.orig_n_params:]
#            print thisParam
#            print otherParam
            val = NewModel.origMod(ene,*thisParam)
            val +=NewModel.otherMod(ene,*otherParam)
            return val

        NewModel.model = newModel

        return NewModel        


        

    def SetTimes(self,times):

        self.timebins = times

    def SetParams(self, params):
        '''
        Pass the parameters to the model
        and then evaluate it
        '''

        self.params = params


        self._EvaluateModel()


    def GetModelCounts(self):

        return self.modelCounts
        
    def _EvaluateModel(self):
        '''
        Evaluate the model at its timebins
        
        '''


        self.modelCounts = self.model(self.timebins,*self.params)


    def SelectComponent(self,comp):
        '''
        Grabs the component parameters from the component
        dictionary that must be created in subclasses

        '''

        comp = self.componentLU[comp]

        return comp
