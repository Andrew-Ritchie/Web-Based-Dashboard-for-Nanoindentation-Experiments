
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
        #print(subprocess.getoutput("kaggle datasets list -s AFM"))
        #os.system("kaggle datasets metadata -p kaggledatasets/ "+ os.environ['KAGGLE_USERNAME']+ "/ andrewritchie98/afm-testdata")
        #os.system("kaggle datasets metadata -p kaggledatasets/ andrewritchie98/afm-testthis2")



    #This method requires names to have no spaces to work without global varibles, this should be returned into a div
    def get_datasets(self):
        #os.system("kaggle datasets download andrewritchie98/afmapplicationtest")
        #print(subprocess.getoutput("kaggle datasets list -m"))
        datalist = subprocess.getoutput("kaggle datasets list -s AFM").split('\n')

        mydatalist = subprocess.getoutput("kaggle datasets list -m").split('\n')

        '''
        print(datalist)
        for element in mydatalist:
            if element not in datalist:
                datalist.append(element)
        '''

        available_datasets = []
        for element in datalist[3:]:
            available_datasets.append(' '.join(s for s in element.split(' ') if s).split(' '))
        
        myavailable_datasets = []
        for element in mydatalist[3:]:
            myavailable_datasets.append(' '.join(s for s in element.split(' ') if s).split(' '))

        for element in myavailable_datasets:
            if element not in available_datasets:
                available_datasets.append(element)

        print(available_datasets, 'test')
        return available_datasets


    def download_data(self, dataset, username):
        if username in os.listdir("kaggledatasets/"):
            shutil.rmtree("kaggledatasets/" + os.environ['KAGGLE_USERNAME'])
        #once implementated use -q to make it quiet
        os.system("kaggle datasets download -p kaggledatasets/" + os.environ['KAGGLE_USERNAME'] + "/ --unzip " + dataset)

    def upload_dataset(self, path, title, slug, username, privateorpublic):

        os.system("kaggle datasets init -p " + path)
        self.edit_metadata(path, title, slug, username)
        if privateorpublic == 'public':
            os.system("kaggle datasets create -u -p " + path)
        else:
            os.system("kaggle datasets create -p " + path)
        print(path, title, slug, username)
        #print(subprocess.getoutput("kaggle datasets files andrewritchie98/afm-" + title))
        #delete the folder your working in 
        shutil.rmtree(path)
        #print(subprocess.getoutput("kaggle datasets files andrewritchie98/afm-testthis2"))


    
    def edit_metadata(self, path, title, slug, username):
        with open(path + 'dataset-metadata.json') as json_file:
            data = json.load(json_file)
        data['title'] = 'AFM-' + title
        data['id'] = username + '/' + 'AFM-' + slug
        json.dump(data, open(path + 'dataset-metadata.json',"w"))







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
    

                


