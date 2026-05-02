# Information Retrieval
## Repository Structure

- **HW1/**
  - Elasticsearch-based indexing and classic retrieval models (Okapi TF, TF-IDF, BM25, LM).
- **HW2/**
  - Custom inverted index replacing Elasticsearch, stemming/stopword experiments, proximity model.
- **HW4/**
  - Graph-based ranking algorithms (PageRank, HITS).
- **HW5/**
  - TREC-style preparation and evaluation utilities (MAP, nDCG, P@k, etc.).
- **HW6/**
  - Feature matrix generation and ML-related scripts.
- **HW7/**
  - Feature extraction and ML/classification utilities (e.g., email filtering/tagging).
- **HW8/**
  - Unsupervised analysis (topic modeling / clustering/partitioning).
- **cran/**
  - Cranfield 1400 benchmark dataset:
    - `cran.all.1400` (documents)
    - `cran.qry` (queries)
    - `cranqrel` (relevance judgements; see below for column semantics)

## Datasets

- **AP89 / TREC AP89**
  - Used by HW1/HW2 as described below.
  - Requires downloading `AP89_DATA.zip` and running indexing + query processing.

- **Cranfield 1400 (practice benchmark)**
  - Included under `cran/`.
  - `cranqrel` uses the standard TREC-style layout: `<query_id> 0 <doc_id> <grade>`.
  - The second column is always `0` (placeholder). The **third column is `doc_id`** and the **fourth column is the relevance grade**.
  - Grades **1–4** indicate relevant documents (with 1 being highest relevance). Grade **5** (if present in other variants) indicates nonrelevant.

## High-Level Execution Process

### Cranfield end-to-end (HW1-style models + evaluation)

To run retrieval models end-to-end on the included Cranfield dataset and generate real evaluation numbers:

```bash
python HW5/run_cranfield.py
```

Outputs:
- `results/cranfield/*.run.txt`
- `results/cranfield/eval.json`
- `results/cranfield/eval.md`

### HW1 (Elasticsearch)

1. Install and start Elasticsearch.
2. Run `HW1/Create_Index.py` to index the corpus.
3. Run `HW1/Query_Processing.py` to extract TF/DF/TTF stats and create pickles.
4. Run `HW1/Retrieval_Models.py` to generate one run file per retrieval model.
5. Evaluate runs using `trec_eval` (or `HW5/Trec_Eval.py` with compatible qrels format).

### HW2 (Custom Inverted Index)

1. Build indexes:
   - `HW2/Unstemmed_With_Stopwords_Index-1.py`
   - `HW2/Stemmed_Stopwords_Removed_Index-1.py`
2. Run query processing + retrieval models for stemmed/unstemmed variants.
3. Run proximity variants if required.
4. Evaluate using `trec_eval` or the HW5 evaluation scripts.

### HW4–HW8

Each homework folder contains its own scripts. Refer to `HW*/report.md` (or the homework folder README) for what inputs are expected and what outputs are produced.

---

# Information Retrieval - HW1

Implement and compare various retrieval systems using vector space models and language models.

This assignment will also introduce elasticsearch: one of the many available commercial-grade indexes. 

This assignment involves writing two programs:

1. A program to parse the corpus and index it with elasticsearch
2. A query processor, which runs queries from an input file using a selected retrieval model

## Getting Started
* Download and install [elasticsearch](https://www.elastic.co), and the [kibana](https://www.elastic.co/products/kibana) plugin
* Download [AP89_DATA.zip](http://dragon.ischool.drexel.edu/example/ap89_collection.zip).

## Document Indexing
Create an index of the downloaded corpus (AP89_Collection). **CreateIndex.py** is a program to parse the documents and send them to my elasticsearch instance.

The corpus files are in a standard format used by TREC. Each file contains multiple documents. The format is similar to XML, but standard XML and HTML parsers will not work correctly. Instead, read the file one line at a time with the following rules:

1. Each document begins with a line containing ```<DOC>``` and ends with a line containing ```</DOC>```.
2. The first several lines of a document’s record contain various metadata. You should read the ```<DOCNO>``` field and use it as the ID of the document.
3. The document contents are between lines containing ```<TEXT>``` and ```</TEXT>```.
4. All other file contents can be ignored.  

Term positions are indexed as they are needed later. 

## Query execution
**Query_Processing.py** and **Retrieval_Models.py** are the programs that prep and run the queries in the file query_desc.51-100.short.txt, included in the data .zip file. All queries (omitting the leading number) are executed using each of the retrieval models listed below, and the top 100 results for each query is written to an output file. If a particular query has fewer than 100 documents with a nonzero matching score, then whichever documents have nonzero scores are listed.

One output file per retrieval model must be generated. Each line of an output file should specify one retrieved document, in the following format:

```<query-number> Q0 <docno> <rank> <score> Exp```  

Where:

* *query-number* is the number preceding the query in the query list
* *docno* is the document number, from the ```<DOCNO>``` field (which we asked you to index)
* *rank* is the document rank: an integer from 1-1000
* *score* is the retrieval model’s matching score for the document
* *Q0* and *Exp* are entered literally

**Query_Processing.py** will run queries against elasticsearch. Instead of using their built in query engine, the program will be retrieving information such as TF and DF scores from elasticsearch and implementing our own document ranking. 

**Retrieval_Models.py** implements the following retrieval models, using TF and DF scores from your elasticsearch index, as needed.

### ES built-in
Use ES query with the API ```"match"{"body_text":"query keywords"}```. This should be somewhat similar to BM25 scoring

### Okapi TF
This is a vector space model using a slightly modified version of TF to score documents. The Okapi TF score for term *w* in document *d* is as follows.

>![alt-text](https://latex.codecogs.com/gif.latex?okapi\\_tf(w,d)&space;=&space;\frac{tf_{w,d}}{tf_{w,d}&plus;0.5&plus;1.5(\frac{len(d)}{avg(len(d))})})


Where:

* ![alt-text](https://latex.codecogs.com/gif.latex?{tf_{w,d}})&nbsp;&nbsp;is the term frequency of term *w* in document *d*
* ![alt-text](https://latex.codecogs.com/gif.latex?{len(d)})&nbsp;&nbsp;is the length of document *d*
* ![alt-text](https://latex.codecogs.com/gif.latex?{avg(len(d))})&nbsp;&nbsp;is the average document length for the entire corpus  

The matching score for document *d* and query *q* is as follows.

>![alt-text](https://latex.codecogs.com/gif.latex?tf(d,q)=\sum_{w\in&space;q}&space;okapi\\_tf(w,d))

### TF-IDF
This is the second vector space model. The scoring function is as follows.

>![alt-text](https://latex.codecogs.com/gif.latex?tfidf(d,q)=\sum_{w\in&space;q}&space;okapi\_tf(w,d)*log&space;\frac{D}{df_w})  

Where:

* ![alt-text](https://latex.codecogs.com/gif.latex?{D})&nbsp;&nbsp;is the total number of documents in the corpus
* ![alt-text](https://latex.codecogs.com/gif.latex?{df_w})&nbsp;&nbsp;is the number of documents which contain term w

### Okapi BM25
BM25 is a language model based on a binary independence model. Its matching score is as follows.

>![alt-text](https://latex.codecogs.com/gif.latex?bm25(d,q)=\sum_{w\in&space;q}&space;\left&space;[&space;log&space;\left&space;(\frac{D&plus;0.5}{df_w&plus;0.5}&space;\right&space;)*\frac{tf_{w,d}&plus;k_1*tf_{w,d}}{tf_{w,d}&plus;k_1\left&space;(&space;(1-b)&plus;b*\frac{len(d)}{avg(len(d))}&space;\right&space;)}&space;*\frac{tf_{w,q}&plus;k_2*tf_{w,q}}{tf_{w,q}&plus;k_2}\right&space;])  

Where:
* ![alt-text](https://latex.codecogs.com/gif.latex?{tf_{w,q}})&nbsp;&nbsp;is the term frequency of term *w* in query *q*
* ![alt-text](https://latex.codecogs.com/gif.latex?{k_1})&nbsp;, ![alt-text](https://latex.codecogs.com/gif.latex?{k_2})&nbsp;, and ![alt-text](https://latex.codecogs.com/gif.latex?{b})&nbsp;&nbsp;are constants. 

### Unigram LM with Laplace smoothing
This is a language model with Laplace (“add-one”) smoothing. We will use maximum likelihood estimates of the query based on a multinomial model “trained” on the document. The matching score is as follows.

>![alt-text](https://latex.codecogs.com/gif.latex?lm\\_laplace(d,q)=\sum_{w\in&space;q}&space;log&space;(p\\_laplace(w|d))) 
>
>![alt-text](https://latex.codecogs.com/gif.latex?p\\_laplace(w|d)=\frac&space;{tf_{w,d}&plus;1}{len(d)&plus;V})  

Where:

* ![alt-text](https://latex.codecogs.com/gif.latex?{V})&nbsp;&nbsp;is the vocabulary size – the total number of unique terms in the collection.

### Unigram LM with Jelinek-Mercer smoothing
This is a similar language model, except that here we smooth a foreground document language model with a background model from the entire corpus.

>![alt-text](https://latex.codecogs.com/gif.latex?lm\\_jm(d,q)=\sum_{w\in&space;q}log(p\\_jm(w|d)))
>
>![alt-text](https://latex.codecogs.com/gif.latex?p\\_jm(w|d)=\lambda&space;\frac{tf_{w,d}}{len(d)}&space;&plus;&space;(1-\lambda)\frac{\sum_{{d}'}&space;tf_{w,{d}'}}{\sum_{{d}'}len({d}')})  

Where:

* ![alt-text](https://latex.codecogs.com/gif.latex?\lambda&space;\in&space;(0,1))&nbsp;&nbsp;is a smoothing parameter which specifies the mixture of the foreground and background distributions.  

Estimated the corpus probability using ![alt-text](https://latex.codecogs.com/gif.latex?\frac{cf_w}{V}).

## Evaluation
1. Compare manually the top 10 docs returned by ESBuilt-In, TFIDF, BM25, LMJelinek, for any 5 queries.

2. Download [trec_eval](http://www.ccs.neu.edu/home/vip/teach/IRcourse/1_retrieval_models/HW1/trec_eval) and use it to evalute the results for each retrieval model.

To perform an evaluation, run:

```$ trec_eval [-q] qrel_file results_file```

The ```-q``` option shows a summary average evaluation across all queries, followed by individual evaluation results for each query; without the ```-q``` option, you will see only the summary average. The trec_eval program provides a wealth of statistics about how well the uploaded file did for those queries, including average precision, precision at various recall cut-offs, and so on.

You should evaluate using the QREL file named qrels.adhoc.51-100.AP89.txt, included in the data .zip file.
"# ISR-SECTION-1-GRP-1" 


## Group Information

**Group:** Group-1

**Section:** Section 1

**School:** School of Information Systems

**Students**

| No. | Student Name | Student Id |
| --- | --- | --- |
| 1 | Nebiyu Gelagay | UGR/6259/17 |
| 2 | Neimah Jemal | UGR/0407/17 |
| 3 | Gashahun W/Yohannes | UGR/5241/15 |
| 4 | Fitsum Fisha | UGR/2785/17 |
| 5 | Betelhem Tadele | UGR/0716/15 |
| 6 | Abraham Kassaye | UGR/4875/17 |


