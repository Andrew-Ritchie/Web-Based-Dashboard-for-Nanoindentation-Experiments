
import json
import os
import subprocess

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




    #This method requires names to have no spaces
    def get_datasets(self):
        datalist = subprocess.getoutput("kaggle datasets list -s afm").split('\n')
        available_datasets = []
        for element in datalist[2:]:
            available_datasets.append(' '.join(s for s in element.split(' ') if s).split(' '))
        print(available_datasets, 'test')
        return available_datasets



