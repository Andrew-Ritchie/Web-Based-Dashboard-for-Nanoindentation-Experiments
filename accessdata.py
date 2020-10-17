import json
import os
from apps.opticsparser import ConvertOptics

converter = ConvertOptics()
 
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
        self.availablecolors = [dict(color="#BB2CD9"), dict(color='#C7980A'), dict(color='#F4651F'), dict(color='#82D8A7'), dict(color='#CC3A05'), dict(color='#575E76'), dict(color='#156943'), dict(color='#0BD055'), dict(color='#ACD338')]

    def addsample(self, name):
        #self.samples.append(Sample(name))
        #self.samplenames.append(name)
        self.samples[name] = Sample(name)


    def assignname(self, name):
        self.name = name


            

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
    




