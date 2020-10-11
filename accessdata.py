import json
import os
from apps.opticsparser import ConvertOptics

converter = ConvertOptics()
 
class Experiment():
    def __init__(self, filepath=None, name=None):
        self.filepath = filepath
        self.name = name
        self.samples = {}
        self.data = {}
        print(self.name)

    def loadexperiment(self):
        for sample in os.scandir(self.filepath):
            if os.path.isdir(sample):
                self.samples.append(Sample(sample, sample.name))
                self.samples.append(sample.name)
    
    def addsample(self, name):
        #self.samples[name] = Sample(name, zip_obj, files)
        self.data[name] = {}
    def addset(self, samplename, setname):
        self.data[samplename][setname] = {}
    def addindent(self, samplename, setname, indentname, zipobject, files):
        self.data[samplename][setname][indentname] = Rawdata(indentname, zipobject, files)
    

        


    def assignfilepath(self, filepath):
        self.filepath = filepath

    def assignname(self, name):
        self.name = name

    def assignzipobject(self, obj):
        self.zipobject = obj
            

class Sample():
    def __init__(self, name, zipobject=None, files=None):
        self.file = files
        self.name = name
        self.sets = {}
        self.zipobject = zipobject
        #self.loadsets()
        self.loadsets2(zipobject=self.zipobject)
        self.color = None
        
    
    def loadsets(self):
        for inset in os.scandir(self.file):
            self.sets.append(Set(inset.name.split('.')[:-1][0], inset))
    
    
    def loadsets2(self, zipobject):
            setname = name.split('/')[2]
            if setname not in self.sets.keys():
                self.sets[setname] = [Set(setname, zipobject=zipobject, files=self.file)]
                print(setname)
    
            
        



    
    
class Set():
    def __init__(self, name, files=None, zipobject=None):
        self.name = name
        self.file = files
        self.indents = {}
        self.segments = []
        self.zipobject = zipobject
        #self.loadindents()
        self.loadindentszip(self.file)
        
    
    def loadindents(self):
        with open(self.file.path) as json_file:
            data = json.load(json_file)
            for element in data[self.name]:
                rawdata = Rawdata(element.split('.')[:-1][0])
                rawdata.loaddata(data[self.name][element])
                self.indents.append(rawdata)
            self.segments = self.indents[0].segments
    
    def loadindentszip(self, name):
        indentname = self.file.split('/')[3]
        if indentname not in self.indents:
            self.indents[indentname] = [Rawdata(indentname, zipobject=self.zipobject, files=self.file)]
        print(self.name)
    
    
            
                

class Rawdata():
    def __init__(self, name, zipobject=None, files=None):
        #Header Info
        self.name = name
        self.segments = [0]
        self.forwardsegment = None
        self.backwardsegment = None
        self.tipradius = None
        self.calibrationfactor = None
        self.cantileverk = None
        self.youngsprovided = None
        self.ypos = None
        self.xpos = None
        self.indexes = None 

        self.zip_obj = zipobject
        self.file = files

        #Raw Information
        self.time = []
        self.load = []
        self.indentation = []
        self.cantilever = []
        self.piezo = []
        self.auxiliary = []
        self.convertdata()
    
    def convertdata(self):
        data = b''
        for line in self.zip_obj.open(self.file):
            data += line
        self.loaddata(converter.loaddata(data))
        self.loadheader(converter.loadheader(data))
    
    
    def loaddata(self, data):
        self.time = data['results']['Time']
        self.load = data['results']['Load']
        self.indentation = data['results']['Indentation']
        self.cantilever = data['results']['Cantilever']
        self.piezo = data['results']['Piezo']
        self.auxiliary = data['results']['Auxiliary']

    def loadheader(self, data):
        self.tipradius = data['tipradius']
        self.calibrationfactor = data['calibrationfactor']
        self.cantileverk = data['cantileverk']
        self.youngsprovided = data['youngsprovided']
        self.ypos = data['ypos']
        self.xpos = data['xpos']
        self.segments += data['indexes']
        print(self.segments)
    
    def assignforward(self, forward):
        self.forwardsegment = forward

    def assignbackward(self, backward):
        self.backwardsegment = backward
    




