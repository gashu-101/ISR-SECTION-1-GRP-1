import dill
import os

def unpickler(file):
    f = open(file, 'rb')
    ds = dill.load(f)
    f.close()
    return ds
docInfo = unpickler(os.path.join('Files', 'Stemmed', 'Pickles', 'docInfo.p'))

print(len(docInfo))