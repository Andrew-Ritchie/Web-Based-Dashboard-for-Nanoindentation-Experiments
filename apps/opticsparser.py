import json
import re
import os
import afmformats
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


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
        #print(filename)
        
    
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
        #print(self.filename, 'filename')
        self.data[self.filename]['header'] = {
            'tipradius': self.extractvalue(head[11]),
            'calibrationfactor': self.extractvalue(head[12]),
            'cantileverk': self.extractvalue(head[9]),
            'youngsprovided': self.extractvalue(head[-2]),
            'xpos': self.extractvalue(head[3]),
            'ypos': self.extractvalue(head[4]),
            'indexes': [self.extractindex(1,head), self.extractindex(2,head), self.extractindex(3,head), self.extractindex(4,head), self.extractindex(5,head)]
        }
        return self.data[self.filename]['header']

    def loaddata(self, decodedfile):
        self.data[self.filename]['results'] ={"Time":[], "Load":[], "Indentation":[], "Cantilever":[], "Piezo":[], "Auxiliary":[]}
        rawdata = self.openfile(35,-1,decodedfile)

        for line in rawdata:
            info = re.split(r"[~\\r\\n\\t]+", line)
            
            self.data[self.filename]['results']["Time"].append(float(info[0]))
            self.data[self.filename]['results']["Load"].append(float(info[1])*1000)
            self.data[self.filename]['results']["Indentation"].append(float(info[2]))
            self.data[self.filename]['results']["Cantilever"].append(float(info[3]))
            self.data[self.filename]['results']["Piezo"].append(float(info[4]))
            self.data[self.filename]['results']["Auxiliary"].append(float(info[5]))
        return self.data[self.filename]

    def realdata(self, filepath):
        self.data[self.filename]['results'] ={"Time":[], "Load":[], "Indentation":[], "Cantilever":[], "Piezo":[], "Auxiliary":[]}
        with open(filepath) as myfile:
            rawdata = myfile.readlines()[35:-1] 

        for line in rawdata:
            info = re.split(r'\t+', line)
            
            self.data[self.filename]['results']["Time"].append(float(info[0]))
            self.data[self.filename]['results']["Load"].append(float(info[1])*1000)
            self.data[self.filename]['results']["Indentation"].append(float(info[2]))
            self.data[self.filename]['results']["Cantilever"].append(float(info[3]))
            self.data[self.filename]['results']["Piezo"].append(float(info[4]))
            self.data[self.filename]['results']["Auxiliary"].append(float(info[5][:-2]))
        return self.data[self.filename]
            

    
    def extractvalue(self, sentence):
        
        return float(re.split(r"[~\\r\\n\\t]+", sentence)[-2])
    
    def extractopenfile(self, sentence):
        return float(sentence.split()[-1])

    def extractindexopenfile(self, index, head):
        temp = 0
        for i in range(index):
            temp += self.data[self.filename]['results']["Time"].index(self.extractopenfile(head[20+i]))
        return temp

        

    def openfile(self, num1, num2, decodedfile):        
        return str(decodedfile).split('\\n')[num1:num2]

    def extractindex(self, index, head):
        temp = 0
        for i in range(index):
            temp += self.data[self.filename]['results']["Time"].index(self.extractvalue(head[20+i]))
        #print(temp)
        return temp
    


    def openrealfile(self, filepath):
        with open(filepath) as myfile:
            head = myfile.readlines()[0:33]
        
        #Assign variables
        #print(self.filename, 'filename')
        self.data[self.filename]['header'] = {
            'tipradius': self.extractopenfile(head[11]),
            'calibrationfactor': self.extractopenfile(head[12]),
            'cantileverk': self.extractopenfile(head[9]),
            'youngsprovided': self.extractopenfile(head[-2]),
            'xpos': self.extractopenfile(head[3]),
            'ypos': self.extractopenfile(head[4]),
            'indexes': [self.extractindexopenfile(1,head), self.extractindexopenfile(2,head), self.extractindexopenfile(3,head), self.extractindexopenfile(4,head), self.extractindexopenfile(5,head)]
        }
        #print(self.data[self.filename]['header'])
        return self.data[self.filename]['header']



class ConvertRangeAFM(ConvertFormat):
    def __init__(self, experiment_name=None, filename=None):
        super().__init__(experiment_name, filename)
        self.raw_data = {'load': None, 'peizo': None, 'time': None}
        self.metadata = None

    def loaddata(self, filepath, filetype):
        if filetype == 'JPK Instruments':
            dslist = afmformats.load_data(filepath)
            fd = afmformats.afm_fdist.AFMForceDistance(dslist[0]._raw_data, dslist[0].metadata, diskcache=False)
            print(dslist[0].columns)
            self.raw_data['piezo'] = [fd.appr['height (piezo)']*1e9] + [fd.retr['height (piezo)']*1e9]
            self.raw_data['load'] = [fd.appr['force']*1e9] + [fd.retr['force']*1e9]
            self.raw_data['time'] = [fd.appr['time']] + [fd.retr['time']]

            self.metadata = fd.metadata
        elif filetype == 'AFM workshop':
            print(filetype)
            dslist = afmformats.load_data(filepath)
            fd = afmformats.afm_fdist.AFMForceDistance(dslist[0]._raw_data, dslist[0].metadata, diskcache=False)
            print(dslist[0].columns)
            print(dslist[0].column_units)
            self.raw_data['piezo'] = [np.abs(fd.appr['height (measured)'])] + [np.abs(fd.retr['height (measured)'])]
            self.raw_data['load'] = [fd.appr['force']] + [fd.retr['force']]
            self.raw_data['time'] = [fd.appr['index']] + [fd.retr['index']]

            self.metadata = fd.metadata
        else:
            print(filetype)
            dslist = afmformats.load_data(filepath)
            fd = afmformats.afm_fdist.AFMForceDistance(dslist[0]._raw_data, dslist[0].metadata, diskcache=False)
            print(dslist[0].columns)
            self.raw_data['piezo'] = [np.abs(fd.appr['height (measured)'])] + [np.abs(fd.retr['height (measured)'])]
            self.raw_data['load'] = [fd.appr['force']] + [fd.retr['force']]
            self.raw_data['time'] = [fd.appr['index']] + [fd.retr['index']]

            self.metadata = fd.metadata            

        return self.raw_data, self.metadata
        
        



    


