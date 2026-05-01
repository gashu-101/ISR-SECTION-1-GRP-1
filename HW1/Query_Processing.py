from __future__ import division
from elasticsearch import Elasticsearch
import re
from elasticsearch_dsl import Search
from collections import defaultdict
from string import digits
import string
import dill
import os

es = Elasticsearch()

s = Search().using(es).query("match_all")
s.aggs.bucket("avg_size", "avg", field="doc_len")
s.aggs.bucket("vocabSize", "cardinality", field="text")
res = s.execute()
D = 84678
total_TF = []


def getTermVector(keyword, a, key):
    tf = a[keyword]["term_freq"]
    docLen = len(a.keys())
    total_TF.append([key.lower(), a[keyword]["ttf"]])
    return tf, docLen


def queryProcessor(query):
    base_dir = os.path.dirname(__file__)
    candidate_paths = [
        os.path.join(base_dir, "..", "HW2", "Files", "stoplist.txt"),
        os.path.join(base_dir, "..", "AP_DATA", "stoplist.txt"),
        os.path.join(base_dir, "stoplist.txt"),
    ]
    stoplist_path = next((p for p in candidate_paths if os.path.exists(p)), None)
    if stoplist_path is None:
        raise FileNotFoundError(
            "stoplist.txt not found. Expected one of: " + ", ".join(candidate_paths)
        )

    with open(stoplist_path, "r", encoding="utf-8", errors="replace") as sfile:
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


def getDocInfo(key, docFreq):
    s = Search().using(es).query("match", text=key)
    docInfo = [h.meta.id for h in s.scan()]
    docFreq.append([key.lower(), len(docInfo)])
    return docInfo, docFreq


def getParameters(query, qNo):
    docFreq = []
    keywords = queryProcessor(query)
    termVector = defaultdict(lambda: defaultdict(list))
    for key in keywords.split():
        docInfo, docFreq = getDocInfo(key, docFreq)
        print(docFreq)
        for docid in docInfo:
            stemKey = es.indices.analyze(index='index1', analyzer='my_english', text=key)
            a = es.termvectors(index="index1", doc_type="document", id=docid, term_statistics=True)["term_vectors"] \
                ["text"]["terms"]

            tf, docLen = getTermVector(stemKey["tokens"][0]["token"], a, key)
            termVector[docid][key.lower()].append(tf)
            termVector[docid][key.lower()].append(docLen)
    f = open('Pickles/docFreq%s.p' % qNo, 'wb')
    dill.dump(docFreq, f)
    f.close()
    f = open('Pickles/termVector%s.p' % qNo, 'wb')
    dill.dump(termVector, f)
    f.close()
    return termVector


def queryMaker():
    f = open('Files/QueryUpdated.txt', 'r')
    queries = []
    for line in f:
        queries.append(re.sub('\\s+', ' ', line).strip().translate(str.maketrans('', '', digits)))
    return queries


queries = queryMaker()
qNo = 0
for query in queries:
    qNo += 1
    termVector = getParameters(query, qNo)
    print("Created %d termVector" % qNo)

unique_TTF = []
for item in total_TF:
    if sorted(item) not in unique_TTF:
        unique_TTF.append(sorted(item))

print(unique_TTF)
f = open('Pickles/totalTF.p', 'wb')
dill.dump(unique_TTF, f)
f.close()

