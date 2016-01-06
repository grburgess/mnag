from multiFit.mnfit import mnfit
from multiFit.likelihood.chi2 import chi2
#from multiFit.likelihood.chi2_sys import chi2_sys

from lightCurve import lightCurve


from numpy import array
#from astropy.table import Table
import json

class mnAfterglow(mnfit):


    def LoadData(self,lightCurveFile,sys=False):
        '''
        An EpEvofile is read in. It is JSON file containing the Ep and time
        derived from either an SCAT or in the future, an mnSpecFit file

        '''

        
        self.lightcurve = lightCurve(lightCurveFile)
        self.sys = sys
        if sys:
            self.stat = chi2_sys()
        else:
            self.stat = chi2() #Will always be using chi2
    
        
        self._dataLoaded = True #Mark that data are loaded

                    


        

    def SetSaveFile(self,savefile):
        '''
        Set the name of the json file to be created
        after the fit is made

        ____________________________________________________________
        arguments:
        savefile: str() file name


        '''
        self.savefile = savefile
        self._saveFileSet = True

    def SetAgModel(self, model):
        '''
        Pass a model class which will be instantiated
        

        _____________________________________________________________
        arguments:
        model: a derived Model class

        '''

        # Check if a list of models was passed
        if type(model) == list:

            listModels = True
        else:
            listModels = False
            
        # Create a list to hold the models
        self.models = []

        
        if listModels:
            # If we have multi models then add them up
            tmp1 = model[0]()
            for mod in model[1:]:
                tmp2 = mod()
                tmp1 = tmp1+tmp2

            self.lightCurveModel = tmp1
        else:
            # Otherwise we are just going to make a model
            self.lightCurveModel = model()



        
        self.n_params = self.lightCurveModel.n_params


        # In this case I can go ahead and construct
        # the likelihood... because I'm fucking awesome!
        self.ConstructLikelihood()

    
        pass


        

    def ConstructLikelihood(self):
        '''
        Provides a likelihood function based off the data and
        model provided. This function is fed to MULTINEST.

        '''

        # The Likelihood function for MULTINEST


        #if self.sys:
        #    self.n_params+=1
        
        def likelihood(cube, ndim, nparams):




#            if not self.sys:

            params = array([cube[i] for i in range(ndim)])
            logL = 0. # This will be -2. * log(L)

            #Get the time intervals
            self.lightCurveModel.SetTimes(self.lightcurve.GetTimeBins())
    
            
            #Calculates the model counts based off the params
            self.lightCurveModel.SetParams(params)

            self.stat.SetModelCounts(self.lightCurveModel.GetModelCounts())



            self.stat.SetCounts(self.lightcurve.GetFlux())
            self.stat.SetErrors(self.lightcurve.GetErr())

            logL = self.stat.ComputeLikelihood()



            #calculate the statistic




            jointLH = -0.5*(logL)

            return jointLH
        
        # Becuase this is inside a class we want to create a
        # likelihood function that does not have an object ref
        # as an argument, so it is created here as a callback

        self.likelihood = likelihood  #likelihood callback
        self.prior = self.lightCurveModel.prior  #prior callback



    def _WriteFit(self):
        '''
        Private function that is called after running MULTINEST.
        It saves relevant information from the fits

        '''
        dof = len(self.lightcurve.GetTimeBins())-self.n_params




        # Construct the dictionary that will be read by
        # SpecFitView.
        out = {"outfiles":self.outfilesDir,\
               "basename":self.basename,\
               "params":self.lightCurveModel.parameters,\
               "lightcurve":self.lightcurve.fileName,\
               "model":self.lightCurveModel.modName,\
               "stat":self.stat.statName,\
               "dof":dof,\
               "tmin":self.lightcurve.GetTimeBins()[0],\
               "tmax":self.lightcurve.GetTimeBins()[-1]\
        }

        f = open(self.outfilesDir+self.savefile,'w')
        
        json.dump(out,f) # Write to a JSON file
        print
        print "Wrote "+self.outfilesDir+self.savefile
        print
        print
        
        f.close()

       

        

    def _PreFitInfo(self):

        print "Starting fit of model:"
        print "\t%s"%self.lightCurveModel.modName
        print

