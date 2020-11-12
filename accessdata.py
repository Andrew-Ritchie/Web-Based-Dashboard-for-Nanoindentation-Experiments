import json
import os
from apps.opticsparser import ConvertOptics

converter = ConvertOptics()

class Data():
    def __init__(self):
        self.exps = {}
    
    def add_exp(self,id, exp):
        self.exps[id] = exp



class Experiment():
    def __init__(self, filepath=None, name=None):
        self.filepath = filepath
        self.name = name
        self.samples = {}
        self.segments = None
        self.forwardseg = None
        self.backwardseg = None
        self.data = {}
        self.displaypaths = [[],[],[],[]]
        self.flag = False
        #dict(color="rgba(255,0,0,0.2)", width=1)
        self.availablecolors = [dict(color='#575E76', width=1), dict(color='#C7980A', width=1), dict(color='#F4651F', width=1), dict(color='#82D8A7', width=1), dict(color='#CC3A05', width=1), dict(color='#575E76', width=1), dict(color='#156943',width=1), dict(color='#0BD055',width=1), dict(color='#ACD338',width=1)]

    def addsample(self, name):
        #self.samples.append(Sample(name))
        #self.samplenames.append(name)
        self.samples[name] = Sample(name)


    def assignname(self, name):
        self.name = name

    def outputdata(self):
        outexperiment = {self.name: {}}
        
        for sample in self.samples.values():
            outexperiment[self.name][sample.name] = {}
            for sets in sample.sets.values():
                outexperiment[self.name][sample.name][sets.name] = {}
                for indent in sets.indents.values():
                    outexperiment[self.name][sample.name][sets.name][indent.name] = {'time':indent.time, 'load':indent.load, 'indentation': indent.indentation, 'cantilever': indent.cantilever, 'piezo': indent.piezo, 'auxiliary': indent.auxiliary}

        with open('example.json','w') as f: 
            json.dump(outexperiment, f, indent=4) 



            

class Sample():
    def __init__(self, name, zipobject=None, files=None):
        self.file = files
        self.name = name
        self.sets = {}
        self.zipobject = zipobject
        #self.loadsets()
        #self.loadsets2(zipobject=self.zipobject)
        self.color = None
        
    def addset(self, setname):
        #self.sets.append(Set(setname))
        #self.setnames.append(setname)
        self.sets[setname] = Set(setname)

    
            
        



    
    
class Set():
    def __init__(self, name, files=None, zipobject=None):
        self.name = name
        self.file = files
        self.indents = {}
        self.segments = []
        self.zipobject = zipobject
        #self.loadindents()
        #self.loadindentszip(self.file)
    
    def addindent(self, name, zip_obj, filepath):
        #self.indentnames.append(name)
        #self.indents.append(Rawdata(name, zipobject=zip_obj, files=filepath))
        self.indents[name] = Rawdata(name, zipobject=zip_obj, files=filepath)
    
    
            
                

class Rawdata():
    def __init__(self, name, zipobject=None, files=None):
        self.zip_obj = zipobject
        self.file = files
        self.displayflag = False
        
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
    




