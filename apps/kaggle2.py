
import json
import os
import subprocess
import shutil

#Users credentials for Kaggle
#os.environ['KAGGLE_USERNAME'] = "andrewritchie98"
#os.environ['KAGGLE_KEY'] = "018ef7f68c1e348d245126dfd127abd3"
#set proxy so that we can deploy to python anywhere
#os.environ['KAGGLE_PROXY'] = "http://proxy.server:3128"

#example download command
#test = os.system("kaggle datasets download andrewritchie98/afmfirstfile")


#datalist = subprocess.getoutput("kaggle datasets list -s afm").split('\n')




class KaggleAPI():

    def __init__(self):
        self.username = None
        self.key = None
        self.available_datasets = None
    
    #Assign the API details for current user and set up enviroment varibles
    def assign_details(self, username, key):
        self.username = username
        self.key = key
        os.environ['KAGGLE_USERNAME'] = username
        os.environ['KAGGLE_KEY'] = key
        #os.environ['KAGGLE_PROXY'] = "http://proxy.server:3128" -- this will be used if deploying on pythonanywhere
        self.available_datasets = self.get_datasets()
        #print(subprocess.getoutput("kaggle datasets list -s nuclei-afm-finaltest"))
        print(subprocess.getoutput("kaggle datasets list -m"))




    #This method requires names to have no spaces to work without global varibles, this should be returned into a div
    def get_datasets(self):
        #os.system("kaggle datasets download andrewritchie98/afmapplicationtest")
        #datalist = subprocess.getoutput("kaggle datasets list -s nuclei-afm-newfile").split('\n')
        datalist = subprocess.getoutput("kaggle datasets list -m").split('\n')
        available_datasets = []
        for element in datalist[2:]:
            available_datasets.append(' '.join(s for s in element.split(' ') if s).split(' '))
        print(available_datasets, 'test')
        return available_datasets


    def download_data(self, dataset, username):
        if username in os.listdir("kaggledatasets/"):
            shutil.rmtree("kaggledatasets/" + os.environ['KAGGLE_USERNAME'])
        #once implementated use -q to make it quiet
        os.system("kaggle datasets download -p kaggledatasets/" + os.environ['KAGGLE_USERNAME'] + "/ --unzip " + dataset)

    def upload_dataset(self, path):
        #os.system("kaggle datasets init -p " + path)
        os.system("kaggle datasets create -u -p " + path)
        #print(subprocess.getoutput("kaggle datasets list -m"))
        #print(subprocess.getoutput("kaggle datasets list -s nuclei-afm-test2"))






class DataProcessor():

    def getsets(self, username):
        files = os.listdir('kaggledatasets/' + username + '/')
        paths = [os.path.join('kaggledatasets/' + username + '/', basename) for basename in files]
        latest_file = max(paths, key=os.path.getctime)
        print(latest_file)

        treeinfo = {}
        with open(latest_file) as json_file:
            data = json.load(json_file)
            exp = list(data.keys())[0]
            treeinfo = {exp: {} }
            for sample in data[exp].keys():
                treeinfo[exp][sample] = list(data[exp][sample].keys())
        return treeinfo

    def uploadrawdata(self, username):
        files = os.listdir('kaggledatasets/' + username + '/')
        paths = [os.path.join('kaggledatasets/' + username + '/', basename) for basename in files]
        latest_file = max(paths, key=os.path.getctime)
        print(latest_file)

        with open(latest_file) as json_file:
            data = json.load(json_file)
        return data
    

                


