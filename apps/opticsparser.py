import json
import re
import os


class ConvertFormat:
    def __init__(self, experiment_name=None, filename=None, samplename=None, setname=None):
        self.filename = filename
        self.experiment_name = experiment_name
        self.data = {self.filename : {'header':{}, 'results':{} } }
        self.samplename = samplename
        self.setname = setname


    def write_json(self, data, filename):
        with open(filename,'w') as f: 
            json.dump(data, f, indent=4) 

    def createfile(self):
        if os.path.isfile('apps/converted/' + self.experiment_name + '/' + self.samplename + '/' + self.setname + '.txt'):
            with open('apps/converted/' + self.experiment_name + '/' + self.samplename + '/' + self.setname + '.txt') as json_file:
                data = json.load(json_file)
                data[self.setname].update(self.data)       
            self.write_json(data, 'apps/converted/' + self.experiment_name + '/' + self.samplename + '/' + self.setname + '.txt')       
        else:
            #os.makedirs(os.path.dirname('apps/converted/' + self.experiment_name + '/' + self.samplename + '/' + self.setname + '.txt'))
            with open('apps/converted/' + self.experiment_name + '/' + self.samplename + '/' + self.setname + '.txt', 'w+') as json_file:
                data = {self.setname: {}}
                data[self.setname].update(self.data)
            self.write_json(data, 'apps/converted/' + self.experiment_name + '/' + self.samplename + '/' + self.setname + '.txt')
    
    def assignexperiment(self, experimentname):
        self.experiment_name = experimentname
    
    def assignfilename(self, filename):
        self.filename = filename
        self.data = {self.filename : {'header':{}, 'results':{} } }
        
    
    def assignsampname(self, sampname):
        self.samplename = sampname
    
    def assignsetname(self, setname):
        self.setname = setname
    


class ConvertOptics(ConvertFormat):
    def __init__(self, experiment_name=None, filename=None):
        super().__init__(experiment_name, filename)
    
    def loadheader(self, decodedfile):
        head = self.openfile(0,33,decodedfile)
        

        #Assign variables
        self.data[self.filename]['header'] = {
            'tipradius': self.extractvalue(head[11]),
            'calibrationfactor': self.extractvalue(head[12]),
            'cantileverk': self.extractvalue(head[9]),
            'youngsprovided': self.extractvalue(head[-2]),
            'xpos': self.extractvalue(head[3]),
            'ypos': self.extractvalue(head[4]),
            'indexes': [self.extractindex(1,head), self.extractindex(2,head), self.extractindex(3,head), self.extractindex(4,head), self.extractindex(5,head)]
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
        return float(re.split(r"[~\\r\\n\\t]+", sentence)[-2])

        

    def openfile(self, num1, num2, decodedfile):        
        return str(decodedfile).split('\\n')[num1:num2]

    def extractindex(self, index, head):
        temp = 0
        for i in range(index):
            temp += self.data[self.filename]['results']["Time"].index(self.extractvalue(head[20+i]))
        return temp






