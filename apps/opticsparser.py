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
        """
        gets datasets from Kaggle

        :type data: dict
        :param data: analysis data
        
        :type filename: string
        :param filename: name of the data being interaced with
        """
        with open(filename,'w') as f: 
            json.dump(data, f, indent=4) 

    def createfile(self):
        """
        writes analysis data to storage
        """
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
        """
        gets datasets from Kaggle

        :type expermentname: string
        :param experimentname: the name of the experiment being analysed
        """
        self.experiment_name = experimentname
    
    def assignfilename(self, filename):
        """
        loads the name of the experiment
        
        :type filename: string
        :param filename: name of the data being interaced with
        """
        self.filename = filename
        self.data = {self.filename : {'header':{}, 'results':{} } }
        #print(filename)
        
    
    def assignsampname(self, sampname):
        """
        loads the name of the sample being examined
        
        :type sampname: string
        :param sampname: name of the sample being interaced with
        """
        self.samplename = sampname
    
    def assignsetname(self, setname):
        """
        loads the name of the set of curves being examined

        :type setname: string 
        :param setname: name of the set being examined
        """
        self.setname = setname
    


class ConvertOptics(ConvertFormat):
    def __init__(self, experiment_name=None, filename=None):
        super().__init__(experiment_name, filename)
    
    def loadheader(self, decodedfile):
        """
        load the metadata from the uploaded indentation files

        :type decodedfile: string
        :param decodedfile: raw decoded metadata from uplaoded indentation files
        """
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
        """
        loads the raw data from uploaded indentation files

        :type decodedfile: string
        :param decodedfile: raw decoded data from uploaded indentation files
        """
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
        """
        loads data for storage parser method
        
        :type filepath: string
        :param filepath: path to the uploaded indentation files within storage
        """
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
        """
        extracts data from a single line within an indentation file

        :type sentence: string
        :param sentence: line from indentation file
        """
        
        return float(re.split(r"[~\\r\\n\\t]+", sentence)[-2])
    
    def extractopenfile(self, sentence):
        """
        extracts data for storage parser method
 
        :type sentence: string
        :param sentence: line from indentation file
        """
        return float(sentence.split()[-1])

    def extractindexopenfile(self, index, head):
        """
        gets data from storage to parse
 
        :type index: int
        :param index: the number of lines the user wants to parse

        :type head: array
        :param head: data to be parsed 
        """
        temp = 0
        for i in range(index):
            temp += self.data[self.filename]['results']["Time"].index(self.extractopenfile(head[20+i]))
        return temp

        

    def openfile(self, num1, num2, decodedfile): 
        """
        extract data for the memory parser
 
        :type num1: int
        :param num1: first line tht has to be parsed

        :type num2: int
        :param num2: last line that has to be parsed

        :type decodedfile: int
        :param decodedfile: the decoded data to be parsed
        """              
        return str(decodedfile).split('\\n')[num1:num2]

    def extractindex(self, index, head):
        """
        extract data for the server parser
 
        :type index: int
        :param index: number of lines to be parsed

        :type head: int
        :param head: metadata data from the indentation file

        """          
        temp = 0
        for i in range(index):
            temp += self.data[self.filename]['results']["Time"].index(self.extractvalue(head[20+i]))
        #print(temp)
        return temp
    


    def openrealfile(self, filepath):
        """
        extract data for the memory parser
 
        :type num1: int
        :param num1: first line tht has to be parsed

        :type num2: int
        :param num2: last line that has to be parsed

        :type decodedfile: int
        :param decodedfile: the decoded data to be parsed
        """  
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
        """
        load the data from AFM formats library
 
        :type filepath: string
        :param filepath: path to the indentation files uploaded by the user

        :type filetype: string
        :param filetype: type of AFM/nanoindenter vendor files uploaded by the user

        """  
        if filetype == 'JPK Instruments':
            print('got here woooo')
            dslist = afmformats.load_data(filepath)
            print(dslist)
            fd = afmformats.afm_fdist.AFMForceDistance(dslist[0]._raw_data, dslist[0].metadata, diskcache=False)
            print(dslist[0].columns)
            self.raw_data['piezo'] = [fd.appr['height (piezo)']*1e9] + [fd.retr['height (piezo)']*1e9]
            self.raw_data['load'] = [fd.appr['force']*1e9] + [fd.retr['force']*1e9]
            self.raw_data['time'] = [fd.appr['time']] + [fd.retr['time']]

            self.metadata = fd.metadata
            print(self.metadata)
        elif filetype == 'AFM workshop':
            print(filetype)
            testing = afmformats.fmt_jpk.load_jpk(filepath)
            print(testing)

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
        
        



    


