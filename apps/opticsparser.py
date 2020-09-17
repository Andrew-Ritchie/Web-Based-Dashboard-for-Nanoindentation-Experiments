import json
import re


class ConvertFormat:
    def __init__(self, filename):
        self.filename = filename
        self.name = None
        self.data = {self.name : {'header':{}, 'results':{} } }


    
class ConvertOptics(ConvertFormat):
    def __init__(self, filename):
        super().__init__(filename)
        self.name = None
    
    def loadheader(self, decodedfile):
        #Load header information
        #we dont use open file here :)
        head = self.openfile(0,33,decodedfile)
        print(head[11])
        print(head[11][-2])

        #Assign variables
        self.data[self.name]['header'] = {
            'tipradius': self.extractvalue(head[11][-2]),
            'calibrationfactor': self.extractvalue(head[12]),
            'cantileverk': self.extractvalue(head[9]),
            'youngsprovided': self.extractvalue(head[-2]),
            'xpos': self.extractvalue(head[3]),
            'ypos': self.extractvalue(head[4])
        }

    def loaddata(self):
        self.data[self.name]['results'] ={"Time":[], "Load":[], "Indentation":[], "Cantilever":[], "Piezo":[], "Auxiliary":[]}
        rawdata = ""

        for line in rawdata:
            info = re.split("[\n\t]", line)
            self.data[self.name]['results']["Time"].append(float(info[0]))
            self.data[self.name]['results']["Load"].append(float(info[1]))
            self.data[self.name]['results']["Indentation"].append(float(info[2]))
            self.data[self.name]['results']["Cantilever"].append(float(info[3]))
            self.data[self.name]['results']["Piezo"].append(float(info[4]))
            self.data[self.name]['results']["Auxiliary"].append(float(info[5]))

    
    def extractvalue(self, sentence):
        return [(re.split(r"[~\\r\\n\\t]+", sentence))]

        

    def openfile(self, num1, num2, decodedfile):        
        return str(decodedfile).split('\\n')[num1:num2]






