from multiFit.FitCompare import FitCompare
from models.models import models
import json


class lcCompare(FitCompare):
    '''
    Subclass of FitCompare that is will performs model selection 
    for spectral fits made with mnSpecFit.
    '''

    def _LoadData(self, data):

        f = open(data)

        fit = json.load(f)

        self.modName = fit["model"]
        self.parameters = fit["params"]
        self.n_params = len(self.parameters)
        self.tmin = fit["tmin"]
        self.tmax = fit["tmax"]
        

        self.basename = fit["basename"]
        self.meanChan = []
        self.chanWidths = []


        

        self.stat = fit["stat"]
        self.dof = fit["dof"]

        self.n_data = self.dof + self.n_params



        

        


    def _CustomInfo(self):
        pass

