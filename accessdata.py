import json
import os


class Experiment():
    def __init__(self, filepath=None, name=None):
        self.filepath = filepath
        self.name = name
        self.samples = []

    def loadexperiment(self):
        for sample in os.scandir(self.filepath):
            if os.path.isdir(sample):
                self.samples.append(Sample(sample, sample.name))

    def assignfilepath(self, filepath):
        self.filepath = filepath
        
    def assignname(self, name):
        self.name = name
            

class Sample():
    def __init__(self, files, name):
        self.file = files
        self.name = name
        self.sets = []
        self.loadsets()
        self.color = None
    
    def loadsets(self):
        for inset in os.scandir(self.file):
            self.sets.append(Set(inset.name.split('.')[:-1][0], inset))
    
    
class Set():
    def __init__(self, name, files):
        self.name = name
        self.file = files
        self.indents = []
        self.loadindents()
    
    def loadindents(self):
        with open(self.file.path) as json_file:
            data = json.load(json_file)
            for element in data[self.name]:
                rawdata = Rawdata(element.split('.')[:-1][0])
                rawdata.loaddata(data[self.name][element])
                self.indents.append(rawdata)
                

class Rawdata():
    def __init__(self, name):
        #Header Info
        self.name = name
        self.segments = []
        self.mainsegment = None

        #Raw Information
        self.time = []
        self.load = []
        self.indentation = []
        self.cantilever = []
        self.piezo = []
        self.auxiliary = []
    
    def loaddata(self, data):
        self.time = data['results']['Time']
        self.load = data['results']['Load']
        self.indentation = data['results']['Indentation']
        self.cantilever = data['results']['Cantilever']
        self.piezo = data['results']['Piezo']
        self.auxiliary = data['results']['Auxiliary']


