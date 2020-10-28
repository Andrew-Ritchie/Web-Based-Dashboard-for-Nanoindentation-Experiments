
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

#This method requires names to have no spaces
def get_datasets(name, key):
    os.environ['KAGGLE_USERNAME'] = name
    os.environ['KAGGLE_KEY'] = key
    datalist = subprocess.getoutput("kaggle datasets list -s afm").split('\n')
    available_datasets = []
    for element in datalist[2:]:
        available_datasets.append(' '.join(s for s in element.split(' ') if s).split(' '))
    print(available_datasets)





