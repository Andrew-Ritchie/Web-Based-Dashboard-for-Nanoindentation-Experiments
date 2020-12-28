import json
import os
from apps.opticsparser import ConvertOptics
from apps.opticsparser import ConvertRangeAFM

converter = ConvertOptics()
AFMformats = ConvertRangeAFM()

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
        self.numsegs = None
        #dict(color="rgba(255,0,0,0.2)", width=1)
        self.availablecolors = [dict(color='#575E76', width=1), dict(color='#C7980A', width=1), dict(color='#F4651F', width=1), dict(color='#82D8A7', width=1), dict(color='#CC3A05', width=1), dict(color='#575E76', width=1), dict(color='#156943',width=1), dict(color='#0BD055',width=1), dict(color='#ACD338',width=1)]

    def addsample(self, name):
        #self.samples.append(Sample(name))
        #self.samplenames.append(name)
        self.samples[name] = Sample(name)


    def assignname(self, name):
        self.name = name

    def outputdata(self, sessionid):
        outexperiment = {self.name: {}}
        
        for sample in self.samples.values():
            outexperiment[self.name][sample.name] = {}
            for sets in sample.sets.values():
                outexperiment[self.name][sample.name][sets.name] = {}
                for indent in sets.indents.values():
                    if indent.filtered == True:
                        outexperiment['metadata'] = {'tipradius' : (indent.tipradius*1000), 'cantileverk':indent.cantileverk}
                        outexperiment[self.name][sample.name][sets.name][indent.name] = {'time':indent.time[1], 'load':indent.load[1], 'piezo': indent.piezo[1]}
                    else:
                        print('hello OIOIOIOI')
        os.mkdir(sessionid)
        with open(sessionid + '/example.json','w') as f: 
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
    
    def addindent(self, name, zip_obj, filepath, afmformat):
        #self.indentnames.append(name)
        #self.indents.append(Rawdata(name, zipobject=zip_obj, files=filepath))
        self.indents[name] = Rawdata(name, zipobject=zip_obj, files=filepath, fileformat=afmformat )
    
    
            
                

class Rawdata():
    def __init__(self, name, zipobject=None, files=None, fileformat=None):
        self.zip_obj = zipobject
        self.file = files
        self.displayflag = False
        self.filtered = True
        
        #Header Info
        self.name = name
        self.segments = None
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
        #self.convertdata()
        #print('hehehehehehehehehehehehehehehe')
        #print(afmformat, 'formmattt')
        if fileformat == 'Optics11':
            self.loaddataoptics(converter.realdata(self.file))
            self.loadheader(converter.openrealfile(self.file))
        else:
            self.loaddatafull(AFMformats.loaddata(self.file, fileformat))



     
    
    def convertdata(self):
        data = b''
        for line in self.zip_obj.open(self.file):
            data += line
        #print(data, 'IS BInary')
        self.loaddataoptics(converter.loaddata(data))
        self.loadheader(converter.loadheader(data))
    
    
    def loaddataoptics(self, data):
        #get index here and split up data
        test = [0]
        

        self.time = data['results']['Time']
        #print(len(self.time), 'This is length of time')
        self.load = data['results']['Load']
        self.indentation = data['results']['Indentation']
        self.cantilever = data['results']['Cantilever']
        self.piezo = data['results']['Piezo']
        self.auxiliary = data['results']['Auxiliary']
        

    def loaddatafull(self, fulldata):

        raw_data = fulldata[0]
        self.time = raw_data['time']
        self.piezo = raw_data['piezo']
        self.load = raw_data['load']
        metadata = fulldata[1]
        print(metadata)
        #self.cantileverk = metadata['spring constant']
        self.segments = len(self.load)



    def loadheader(self, data):
        self.tipradius = data['tipradius']
        self.calibrationfactor = data['calibrationfactor']
        self.cantileverk = data['cantileverk']
        self.youngsprovided = data['youngsprovided']
        self.ypos = data['ypos']
        self.xpos = data['xpos']
        segi = [0]
        segi += data['indexes']
        self.piezo = [self.piezo[segi[0]:segi[1]]] + [self.piezo[segi[1]:segi[2]]] + [self.piezo[segi[2]:segi[3]]] + [self.piezo[segi[3]:segi[4]]] + [self.piezo[segi[4]:segi[5]]] 
        self.time = [self.time[segi[0]:segi[1]]] + [self.time[segi[1]:segi[2]]] + [self.time[segi[2]:segi[3]]] + [self.time[segi[3]:segi[4]]] + [self.time[segi[4]:segi[5]]] 
        self.load = [self.load[segi[0]:segi[1]]] + [self.load[segi[1]:segi[2]]] + [self.load[segi[2]:segi[3]]] + [self.load[segi[3]:segi[4]]] + [self.load[segi[4]:segi[5]]] 
        self.segments = len(self.load)

    def assignforward(self, forward):
        self.forwardsegment = forward

    def assignbackward(self, backward):
        self.backwardsegment = backward
    




