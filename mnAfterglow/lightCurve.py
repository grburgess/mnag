from numpy import array, concatenate
import json


class lightCurve(object):


    def __init__(self,lightCurveFile):


        f = open(lightCurveFile) # Open the file
        self.fileName = lightCurveFile
        
        jsonFile = json.load(f)


        self._pcflux       = array(jsonFile['pcFlux'])
        self._pcfluxErr    = array(jsonFile['pcErr'])
        self._pctimebins = array(jsonFile['pcTime'])
        self._wtflux       = array(jsonFile['wtFlux'])
        self._wtfluxErr    = array(jsonFile['wtErr'])
        self._wttimebins = array(jsonFile['wtTime'])
        self._name = jsonFile["name"]
        self._z = jsonFile["z"]


        self._allTime = concatenate((self._wttimebins,self._pctimebins))
        self._allFlux = concatenate((self._wtflux,self._pcflux))
        self._allErr  = concatenate((self._wtfluxErr,self._pcfluxErr))
        
        self._offset   = 0.0  #This sets a shift in the times if the time bin is not zero 


    def GetName(self):
        return self._name
    def GetZ(self):
        return self._z

    
    def SetOffset(self,offset):


        self._offset = offset

    def GetTimeBins(self):

        return self._allTime


    def GetFlux(self):


        return self._allFlux

    def GetErr(self):


        return self._allErr

    def GetWTtime(self):

        return self._wttimebins

    def GetWTflux(self):

        return self._wtflux

    def GetWTerr(self):

       return self._wtfluxErr


    def GetPCtime(self):

        return self._pctimebins

    def GetPCflux(self):

        return self._pcflux

    def GetPCerr(self):

       return self._pcfluxErr
