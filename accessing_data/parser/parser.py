import re

class CollateInformation:
    def __init__(self, filepath):
        self.filepath = filepath
        self.tipradius = None
        self.calibrationfactor = None
        self.cantileverk = None
        self.delay = None
        self.youngsprovided = None
        self.xpos = None
        self.ypos = None
        self.xposition = None
    
class NewOptics(CollateInformation):
    def __init__(self, filepath):
        super().__init__(filepath)
    
    def loadheader(self):
        #Load header information
        data_file = open(self.filepath, "r")
        head = [next(data_file) for x in range(33)]
        data_file.close()
        #Assign variables
        self.tipradius = self.extractvalue(head[11])
        self.calibrationfactor = self.extractvalue(head[12])
        self.cantileverk = self.extractvalue(head[9])
        self.youngsprovided = self.extractvalue(head[-2])
        self.xpos = self.extractvalue(head[3])
        self.ypos = self.extractvalue(head[4])
    
    def extractvalue(self, sentence):
        return float(re.split("[\n\t]", sentence)[-2])
        
        




