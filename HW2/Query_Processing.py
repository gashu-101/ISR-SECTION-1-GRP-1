from __future__ import division
import string
from stemming.porter2 import stem
from string import digits
import re
import time
import os
import importlib.util
from collections import OrderedDict
import dill


def _load_termvector_class():
    base_dir = os.path.dirname(__file__)
    target = os.path.join(base_dir, 'Stemmed_Stopwords_Removed_Index-1.py')
    spec = importlib.util.spec_from_file_location('Stemmed_Stopwords_Removed_Index_1', target)
    mod = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise ImportError('Unable to load TermVector from ' + target)
    spec.loader.exec_module(mod)
    return mod.TermVector


TermVector = _load_termvector_class()

def unpickler(file):
    f = open(file, 'rb')
    ds = dill.load(f)
    f.close()
    return ds

def parseCatalog(file):
    catalog = {}
    catalogFile = open(file, 'r')
    for line in catalogFile.readlines():
        content = line.strip().split(',')
        catalog[content[0]] = content[1:]
    return catalog

def queryMaker():
    f = open('QueryUpdated.txt', 'r')
    queries = []
    for line in f:
        queries.append(re.sub(r'[\-\.\"\s]+', ' ', line).strip().translate(str.maketrans('', '', digits)))
    return queries

def queryProcessor(query):
    base_dir = os.path.dirname(__file__)
    candidate_paths = [
        os.path.join(base_dir, 'Files', 'stoplist.txt'),
        os.path.join(base_dir, '..', 'HW2', 'Files', 'stoplist.txt'),
        os.path.join(base_dir, '..', 'AP_DATA', 'stoplist.txt'),
    ]

    stoplist_path = next((p for p in candidate_paths if os.path.exists(p)), None)
    if stoplist_path is None:
        raise FileNotFoundError('stoplist.txt not found. Expected one of: ' + ', '.join(candidate_paths))

    with open(stoplist_path, 'r', encoding='utf-8', errors='replace') as sfile:
        stopWords = sfile.readlines()
    stopWords = list(filter(None, stopWords))
    keywords = ""
    flag = 0
    for word in query.split():
        for sWord in stopWords:
            if (word == sWord.strip()):
                flag = 1
                break
        if (flag != 1):
            keywords += word + " "
        flag = 0
    keywords = keywords.translate(str.maketrans('', '', string.punctuation))
    return keywords.strip()

def getInfo(key, catalog, termMap, docMap):
    keyInfo = OrderedDict()
    invList = OrderedDict()
    docDict = OrderedDict()
    indexFile = open("Files/Unstemmed/invertedFile0.txt", 'r')
    offset = catalog.get(key)[0]
    indexFile.seek(int(offset))
    line = indexFile.readline()
    df = line.split(':')[0].split(',')[1]
    ttf = line.split(':')[0].split(',')[2]
    keyInfo[key] = [df, ttf]
    remStr = line.split(':')[1].split(';')
    for item in remStr:
        docno = item.split(',')[0]
        docID = docMap.get(int(docno))
        tf = int(item.split(',')[1])
        pos = [int(e) for e in item.split(',')[2:len(item.split(','))]]
        docDict[docID] = TermVector(tf, pos)
    invList[key] = docDict
    indexFile.close()
    return invList, keyInfo

def getParameters(query, qNo):
    keywords = queryProcessor(query)
    termVector = OrderedDict()
    termStats = OrderedDict()
    for key in keywords.split():
        key = key.lower()
        invList, keyInfo= getInfo(key, catalog, termMap, docMap)
        termVector.update(invList)
        termStats.update(keyInfo)
    f = open('Files/Unstemmed/Pickles/termStats%s.p' % qNo, 'wb')
    dill.dump(termStats, f)
    f.close()
    f = open('Files/Unstemmed/Pickles/termVector%s.p' % qNo, 'wb')
    dill.dump(termVector, f)
    f.close()

start_time = time.time()
docInfo = unpickler('Files/Unstemmed/Pickles/docInfo.p')
catalog = parseCatalog('Files/Unstemmed/catalogFile.txt')
termMap = unpickler('Files/Unstemmed/Pickles/termMap.p')
docMap = unpickler('Files/Unstemmed/Pickles/docMap.p')
# getInfo('govern', catalog, termMap, docMap)
queries = queryMaker()
qNo = 0
for query in queries:
    qNo += 1
    getParameters(query, qNo)
    print("Created %d termVector" % qNo)
temp = time.time() - start_time
print(temp)
hours = temp // 3600
temp = temp - 3600 * hours
minutes = temp // 60
seconds = temp - 60 * minutes
print('%d:%d:%d' % (hours, minutes, seconds))
