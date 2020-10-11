import json
import os
from apps.opticsparser import ConvertOptics

converter = ConvertOptics()
 
class Experiment():
    def __init__(self, filepath=None, name=None):
        self.filepath = filepath
        self.name = name
        self.samples = {}
        self.samplenames = []

    def loadexperiment(self):
        for sample in os.scandir(self.filepath):
            if os.path.isdir(sample):
                self.samples.append(Sample(sample, sample.name))
                self.samples.append(sample.name)
    
    def loadsamples(self, name, zipobject):
        samplename = name.split('/')[1]
        if samplename not in self.samples:
            self.samples[samplename] = [Sample(samplename, zipobject=zipobject, files=name)]
        else:
            self.samples[samplename].append(Sample(samplename, zipobject=zipobject, files=name))


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
        self.loadsets2(name, zipobject=self.zipobject)
        self.color = None
        print(self.name)
    
    def loadsets(self):
        for inset in os.scandir(self.file):
            self.sets.append(Set(inset.name.split('.')[:-1][0], inset))
    
    def loadsets2(self, name, zipobject):
        setname = self.file.split('/')[2]
        if setname not in self.sets:
            self.sets[setname] = [Set(setname, zipobject=zipobject, files=self.file)]
        else:
            self.sets[setname].append(Set(setname, zipobject=zipobject, files=self.file))
        



    
    
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
        print(self.time[0:100])
    
    def convertdata(self):
        data = b''
        for line in self.zip_obj.open(self.file):
            data += line
        self.loaddata(converter.loaddata(data))
    
    def loaddata(self, data):
        self.time = data['results']['Time']
        self.load = data['results']['Load']
        self.indentation = data['results']['Indentation']
        self.cantilever = data['results']['Cantilever']
        self.piezo = data['results']['Piezo']
        self.auxiliary = data['results']['Auxiliary']
        #self.segments += data['header']['indexes']
    
    def assignforward(self, forward):
        self.forwardsegment = forward

    def assignbackward(self, backward):
        self.backwardsegment = backward
    




