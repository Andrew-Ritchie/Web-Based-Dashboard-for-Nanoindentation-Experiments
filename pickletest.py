import base64
from collections import MutableMapping
import json
import pickle

class PythonObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        return {'_python_object': 
                base64.b64encode(pickle.dumps(obj)).decode('utf-8') }

def as_python_object(dct):
    if '_python_object' in dct:
        return pickle.loads(base64.b64decode(dct['_python_object']))
    return dct

# based on AttrDict -- https://code.activestate.com/recipes/576972-attrdict
class TreeNode(MutableMapping):
    """ dict-like object whose contents can be accessed as attributes. """
    def __init__(self, name, children=None):
        self.name = name
        self.children = list(children) if children is not None else []
    def __getitem__(self, key):
        return self.__getattribute__(key)
    def __setitem__(self, key, val):
        self.__setattr__(key, val)
    def __delitem__(self, key):
        self.__delattr__(key)
    def __iter__(self):
        return iter(self.__dict__)
    def __len__(self):
        return len(self.__dict__)

tree = TreeNode('Parent')
tree.children.append(TreeNode('Child 1'))
child2 = TreeNode('Child 2')
tree.children.append(child2)
child2.children.append(TreeNode('Grand Kid'))
child2.children[0].children.append(TreeNode('Great Grand Kid'))

json_str = json.dumps(tree, cls=PythonObjectEncoder, indent=4)
print('json_str:', json_str)
pyobj = json.loads(json_str, object_hook=as_python_object)
print(type(pyobj))