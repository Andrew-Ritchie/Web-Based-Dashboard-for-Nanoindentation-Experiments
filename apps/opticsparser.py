import json
import re


class ConvertFormat:
    def __init__(self, filename, experiment_name):
        self.filename = filename
        self.experiment_name = experiment_name
        self.data = {self.filename : {'header':{}, 'results':{} } }

    def write_json(self, data, filename):
        with open(filename,'w') as f: 
            json.dump(data, f, indent=4) 

    def createfile(self):
        with open('apps/converted/' + self.experiment_name + '.txt') as json_file:
            data = json.load(json_file)
            data[self.experiment_name].update(self.data)
            print(data.keys())
            print(data[self.experiment_name].keys())
            
        self.write_json(data, 'apps/converted/' + self.experiment_name + '.txt')
    


class ConvertOptics(ConvertFormat):
    def __init__(self, filename, experiment_name):
        super().__init__(filename, experiment_name)
    
    def loadheader(self, decodedfile):
        head = self.openfile(0,33,decodedfile)

        #Assign variables
        self.data[self.filename]['header'] = {
            'tipradius': self.extractvalue(head[11]),
            'calibrationfactor': self.extractvalue(head[12]),
            'cantileverk': self.extractvalue(head[9]),
            'youngsprovided': self.extractvalue(head[-2]),
            'xpos': self.extractvalue(head[3]),
            'ypos': self.extractvalue(head[4])
        }

    def loaddata(self, decodedfile):
        self.data[self.filename]['results'] ={"Time":[], "Load":[], "Indentation":[], "Cantilever":[], "Piezo":[], "Auxiliary":[]}
        rawdata = self.openfile(35,-1,decodedfile)

        for line in rawdata:
            info = re.split(r"[~\\r\\n\\t]+", line)
            
            self.data[self.filename]['results']["Time"].append(float(info[0]))
            self.data[self.filename]['results']["Load"].append(float(info[1]))
            self.data[self.filename]['results']["Indentation"].append(float(info[2]))
            self.data[self.filename]['results']["Cantilever"].append(float(info[3]))
            self.data[self.filename]['results']["Piezo"].append(float(info[4]))
            self.data[self.filename]['results']["Auxiliary"].append(float(info[5]))
            

    
    def extractvalue(self, sentence):
        return re.split(r"[~\\r\\n\\t]+", sentence)[-2]

        

    def openfile(self, num1, num2, decodedfile):        
        return str(decodedfile).split('\\n')[num1:num2]






