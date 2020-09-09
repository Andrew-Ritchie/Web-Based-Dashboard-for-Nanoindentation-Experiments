import os


class Node:
    def __init__(self, name, filepath=None):
        self.name = name
        self.filepath = filepath
        self.data = None
        self.children = []

    
    def printchildren(self, node):
        for element in node.children:
            print(element.name)


class Experiment(Node):
    
    def __init__(self, name, filepath):
        super().__init__(name, filepath) 
        self.loadexperiment()
        
    def loadexperiment(self):                

        dirlist = os.listdir(self.filepath)
        for name in dirlist:
            path = self.filepath + name
            if os.path.isdir(path):
                self.children.append(Node(name, path))
        for element in self.children:
            test = os.listdir(element.filepath)
            for name in test:
                path = element.filepath + '/' + name
                if os.path.isfile(path) and name != '.DS_Store':
                    element.children.append(Node(name, path))
    
    

        

tree = Node("first Tree")
rootdir = '../data/'


test = Experiment("test", rootdir)
test.printchildren(test.children[1])
