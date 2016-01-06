from multiFit.FitView import FitView
from astropy.table import Table
from lightCurve import lightCurve
from models.models import models
import matplotlib.pyplot as plt
from numpy import array, cumsum, linspace, sqrt, logspace, log10
from numpy import mean, meshgrid, histogram2d, zeros
from scipy.stats import ks_2samp
import json


class lcFitView(FitView):


    def _LoadData(self,data):



        f = open(data)

        fit = json.load(f)

        self.modName = fit["model"]


        self._composite = False
        #Check to see if this is a composite model

        test = self.modName.split("+")
        if len(test)>1:
            self._composite = True
            compositeModels = test
            
            for i in range(len(compositeModels)):

                tmp = compositeModels[i].split('_')[0] #Hack off the duplicate model number tag
                compositeModels[i] = tmp

        
        
        self.parameters = fit["params"]
        self.n_params = len(self.parameters)

        
        self.lcFile = fit["lightcurve"]
        self.basename = fit["basename"]
        self.stat =fit["stat"]
        self.dof = fit['dof']

        self.dataRange=logspace(log10(fit["tmin"]),log10(fit["tmax"]),1000)

        self.tmin = fit["tmin"]
        self.tmax = fit["tmax"]


        lc = lightCurve(self.lcFile)
        self.name = lc.GetName()
        self.z = lc.GetZ()
        


        if self._composite:

            thisModel = (models[compositeModels[0]])()
            for mod in compositeModels[1:]:
                
                tmp = (models[mod])()
                thisModel = thisModel + tmp
            
            self._componentLU = thisModel.componentLU
            self._componentModel = thisModel
        else:
            thisModel = (models[fit["model"]])()
        self.model = thisModel.model

                        
        #thisModel =  models[self.modName]()
        self.thisModel = thisModel

        #self.model = thisModel.model



    def _CustomInfo(self):

        print

        print "Model:\n\t%s"%self.modName

        print "TMIN: %.2f"%self.tmin
        print "TMAX: %.2f"%self.tmax

        print "\nBest Fit Parameters (1-sigma err):"

        marg = self.anal.get_stats()["marginals"]

        for params,val,err in zip(self.parameters,self.bestFit,marg):

            err = err["1sigma"]
            
            print "\t%s:\t%.2f\t+%.2f -%.2f"%(params,val,err[1]-val,val-err[0])

        print
        print "%s per d.o.f.:\n\t %.2f/%d"%(self.stat,-2.*self.loglike,self.dof)



    def PlotEvoFlares(self,fignum=1000):

        if not self._composite:
            print "This is not a composite model!"
            return

        fig = plt.figure(fignum)

        ax = fig.add_subplot(111)

        evo = lightCurve(self.lcFile)
        self.linewidth = .8
        

        contourColor = "#984ea3"
        bfColor = "k"
        flareColor = "grey"
        wtColor = "#e41a1c"
        pcColor = "#4daf4a"
        #breakColor = ["#377eb8","#ff7f00","#a65628","#377eb8","#f781bf"]
       
        components = self._componentLU.keys()

        
        yData = []
        leg = []

        for comp in components:

            thisComp = self._componentModel.SelectComponent(comp)
            
            tt = self.GetParamIndex(thisComp["params"])
            bfParams = self.bestFit[tt]

            # Plot the best fit
       
        
            yData=thisComp["model"](self.dataRange, *bfParams)

            if thisComp["plOrder"] == -1:
                color=flareColor
            else:
                color = bfColor
            
            ax.loglog(self.dataRange, yData, color=color, lw=self.linewidth,ls="-",zorder=-10)


            # Now plot the contours

            yData = [] 
            
            for params in self.anal.get_equal_weighted_posterior()[::50,:-1]:

                params = params[tt]
                
                yData.append( thisComp["model"](self.dataRange, *params) )

        

        
            #Plot the spread in data
            
            for y in yData:

                ax.loglog(self.dataRange,y,contourColor,alpha=.07,lw=self.linewidth*.8,ls="-",zorder=-32) ## modify later

   


        ax.errorbar(evo.GetWTtime(),evo.GetWTflux(),yerr=evo.GetWTerr(),fmt='.',color=wtColor,capsize=self.capsize,elinewidth=self.elinewidth,markersize=3.3,alpha=.2)
        ax.errorbar(evo.GetPCtime(),evo.GetPCflux(),yerr=evo.GetPCerr(),fmt='.',color=pcColor,capsize=self.capsize,elinewidth=self.elinewidth,markersize=3.3,alpha=.7)

        ax.set_yscale('log',nonposy='clip')
        ax.set_xlabel("Time [s]")
        ax.set_ylabel(r"Flux")
        
        # #Plot the breaks if any


        maxY =evo.GetFlux().max()
        minY = evo.GetFlux().min()

        maxY+=maxY*0.5
        minY-=minY*0.5
        # if self.thisModel.plOrder>0:
        #     cIdx=0
        #     for val,err in zip(self.bestFit[-self.thisModel.plOrder:],self.anal.get_stats()["marginals"][-self.thisModel.plOrder:]):

        #         sig = err['1sigma']
        #         up=sig[1]
        #         down=sig[0]

        #         ax.vlines([10**val,10**up,10**down],1E-20,1E-1,colors=breakColor[cIdx],linestyles=['--',':',':'],zorder=-33)
        #         ax.fill_betweenx([1E-20,1E-1],10**down,10**up,color=breakColor[cIdx],alpha=.1,zorder=-33)

                
        #         cIdx+=1
        
        # ax.text(.7,.9  ,"GRB %s"%self.name ,transform=ax.transAxes)
#        ax.text(.7,.8  ,"z: %.2f"%self.z ,transform=ax.transAxes)
        ax.set_ylim(bottom=minY,top=maxY)
        return ax






    def PlotEvo(self,fignum=1000):


        fig = plt.figure(fignum)

        ax = fig.add_subplot(111)

        evo = lightCurve(self.lcFile)
        self.linewidth = .8
        

        contourColor = "#984ea3"
        bfColor = "k"
        wtColor = "#e41a1c"
        pcColor = "#4daf4a"
        breakColor = ["#377eb8","#ff7f00","#a65628","#377eb8","#f781bf"]
       

        yData = []


        for params in self.anal.get_equal_weighted_posterior()[::50,:-1]:
            yData.append(self.model(self.dataRange, *params))

        

        
        #Plot the spread in data
            
        for y in yData:

            ax.loglog(self.dataRange,y,contourColor,alpha=.07,lw=self.linewidth*.8,ls="-",zorder=-32) ## modify later

   


        # Plot the best fit
       
        
        bfModel=self.model(self.dataRange, *self.bestFit)
        

        ax.loglog(self.dataRange,bfModel,bfColor,lw=self.linewidth,ls="-",zorder=-10) #modify later


        ax.errorbar(evo.GetWTtime(),evo.GetWTflux(),yerr=evo.GetWTerr(),fmt='.',color=wtColor,capsize=self.capsize,elinewidth=self.elinewidth,markersize=3.3,alpha=.2)
        ax.errorbar(evo.GetPCtime(),evo.GetPCflux(),yerr=evo.GetPCerr(),fmt='.',color=pcColor,capsize=self.capsize,elinewidth=self.elinewidth,markersize=3.3,alpha=.7)

        ax.set_yscale('log',nonposy='clip')
        ax.set_xlabel("Time [s]")
        ax.set_ylabel(r"Flux")
        
        #Plot the breaks if any


        maxY =evo.GetFlux().max()
        minY = evo.GetFlux().min()

        maxY+=maxY*0.5
        minY-=minY*0.5
        if self.thisModel.plOrder>0:
            cIdx=0
            for val,err in zip(self.bestFit[-self.thisModel.plOrder:],self.anal.get_stats()["marginals"][-self.thisModel.plOrder:]):

                sig = err['1sigma']
                up=sig[1]
                down=sig[0]

                ax.vlines([10**val,10**up,10**down],1E-20,1E-1,colors=breakColor[cIdx],linestyles=['--',':',':'],zorder=-33)
                ax.fill_betweenx([1E-20,1E-1],10**down,10**up,color=breakColor[cIdx],alpha=.1,zorder=-33)

                
                cIdx+=1
        
        ax.text(.7,.9  ,"GRB %s"%self.name ,transform=ax.transAxes)
#        ax.text(.7,.8  ,"z: %.2f"%self.z ,transform=ax.transAxes)
        ax.set_ylim(bottom=minY,top=maxY)
        return ax

        
