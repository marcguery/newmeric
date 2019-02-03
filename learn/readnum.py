import numpy as np
import pandas as pd
from tabulate import tabulate as tab

class Reader(object):
    def __init__(self):
        self.data=None
        self.matrices=None
    
    def read_csv(self, file):
        with open(file, 'r') as f:
            self.data=pd.read_csv(f, sep=",", header=None)
        f.close
    
    def __repr__(self):
        return tab(self.data,tablefmt="grid")
    
    def __str__(self):
        return tab(self.data,tablefmt="grid")
    
    def split(self, sep="#"):
        idxs=self.data[0].str.contains(sep)
        assert len(idxs)>0
        idxSep=self.data.index[idxs].values
        assert int(len(self.data[0])%len(idxs))==0
        idxSep+=1
        idxSep = np.insert(idxSep, 0, 0)
        self.matrices = [self.data.iloc[idxSep[n]:idxSep[n+1]] for n in range(len(idxSep)-1)]
    
    def __getitem__(self, key):
        return self.matrices[key]