import re
import plotly.express as px


class DataSet:
    def __init__(self, filepath):
        self.filepath = filepath
        self.tipradius = None
        self.calibrationfactor = None
        self.cantileverk = None
        self.delay = None
        self.youngsprovided = None
        self.xpos = None
        self.ypos = None
        self.xposition = None
        self.results = None



    
class NewOptics(DataSet):
    def __init__(self, filepath):
        super().__init__(filepath)
    
    def loadheader(self):
        #Load header information
        head = self.openfile(0,33)
        #Assign variables
        self.tipradius = self.extractvalue(head[11])
        self.calibrationfactor = self.extractvalue(head[12])
        self.cantileverk = self.extractvalue(head[9])
        self.youngsprovided = self.extractvalue(head[-2])
        self.xpos = self.extractvalue(head[3])
        self.ypos = self.extractvalue(head[4])
    
    def loaddata(self): 
        
        self.results ={"Time":[], "Load":[], "Indentation":[], "Cantilever":[], "Piezo":[], "Auxiliary":[]}
        rawdata = self.openfile(35, None)

        for line in rawdata:
            info = re.split("[\n\t]", line)
            self.results["Time"].append(float(info[0]))
            self.results["Load"].append(float(info[1]))
            self.results["Indentation"].append(float(info[2]))
            self.results["Cantilever"].append(float(info[3]))
            self.results["Piezo"].append(float(info[4]))
            self.results["Auxiliary"].append(float(info[5]))
    

    def extractvalue(self, sentence):
        return float(re.split("[\n\t]", sentence)[-2])
    
    def openfile(self, num1, num2):
        data_file = open(self.filepath, "r")
        rawdata = data_file.readlines()[num1:num2]
        data_file.close()
        return rawdata

        
        


test = NewOptics("../data/matrix_scan01/2NapFF 16mgmL GdL S-1 X-9 Y-9 I-1.txt")
test.loaddata()

fig = px.line(x=test.results['Time'], y=test.results['Indentation'], title='Life expectancy in Canada')
fig.show()
#for i in range(1900,2000):
#    x = test.results['Load'][i-1]
#    print(test.results['Load'][i] , i)
x = []
for i in range(len(test.results['Load'])):
    x.append(abs(test.results['Load'][i] - test.results['Load'][i-1]))
print(x[max(test.results['Load'])])
print(max(x))


