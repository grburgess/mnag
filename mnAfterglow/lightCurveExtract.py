import numpy as np
import json



class lightCurveExtract(object):


    def __init__(self,lcObj,ext):

        self.wtFlag = True
        
        #Get the WC Mode
        self.wt = np.array(lcObj['XRT'][2])
        if lcObj['XRT'][2] == []:
            print
            print "No WT data"
            print
            self.wtFlag = False

        
        #Get the PC Mode
        self.pc = np.array(lcObj['XRT'][4])



        
        #Get the name
        self.name = lcObj["GRB"]

        self.ext = ext
        self.z = lcObj['z']

        print "Processing:\n\tGRB %s\n"%self.name
        
        self._WriteJSON()

    def _WriteJSON(self):


        if self.wtFlag:
            outdata = {"wtTime" : self.wt[:,0].tolist(),\
                       "wtFlux" : self.wt[:,3].tolist(),\
                       "wtErr"  : self.wt[:,4].tolist(),\
                       "pcTime" : self.pc[:,0].tolist(),\
                       "pcFlux" : self.pc[:,3].tolist(),\
                       "pcErr"  : self.pc[:,4].tolist(),\
                       "name"   : self.name,\
                       "z"      : self.z\
            }

        else:
            outdata = {"wtTime" : [],\
                       "wtFlux" : [],\
                       "wtErr"  : [],\
                       "pcTime" : self.pc[:,0].tolist(),\
                       "pcFlux" : self.pc[:,3].tolist(),\
                       "pcErr"  : self.pc[:,4].tolist(),\
                       "name"   : self.name,\
                       "z"      : self.z\
            }

            
        f = open("%s%s_xrt_save.json"%(self.ext,self.name),'w')

        json.dump(outdata,f)

        f.close()
