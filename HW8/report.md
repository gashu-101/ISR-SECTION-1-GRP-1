# HW8 Report — Unsupervised Analysis (Topic Modeling / Clustering)

## Overview
HW8 implements unsupervised analysis over a document collection using:
- **Topic modeling** with LDA (Latent Dirichlet Allocation)
- **Partitioning / clustering** with KMeans on LDA topic vectors

## Dataset
- Code expects the AP89 collection under `AP_DATA/ap89_collection/`.
- Uses qrels and BM25 run files to build sets of documents per query in part A.

## Part A — LDA on top documents (`clustering.py`)
Pipeline:
1. Load top documents from:
   - `qrels.adhoc.51-100.AP89.txt` (QREL docs)
   - `OkapiBM25_Results_File.txt` (retrieved docs)
2. For each query (up to a limit), take the union of retrieved docs and relevant docs.
3. Read document text from AP89 files.
4. Fit an LDA model and output:
   - topic top words
   - per-document topic distributions

Outputs are written into `partA_topics/` and `partA_docs/`.

## Part B — Full collection clustering (`partition.py`)
Pipeline:
1. Read all AP89 documents.
2. Fit LDA to obtain a topic vector per document.
3. Cluster topic vectors using KMeans.
4. Evaluate clustering quality using a pairwise agreement measure based on shared relevance judgments.

Outputs are written into `partB_clusterTopics/` and `partB_clusters/`.

## Notes / fixes
- Fixed a logic bug in `clustering.py` where the QREL branch was always taken (`elif 'QREL':`). Now it correctly checks `model == 'QREL'`.

## How to run (high level)
1. Ensure AP89 files exist under `AP_DATA/ap89_collection/` and required run/qrels files exist.
2. Run topic modeling:
   - `python HW8/clustering.py`
3. Run partitioning/clustering:
   - `python HW8/partition.py`

## Results
Topic coherence, discovered topics, and clustering accuracy depend on:
- number of topics (`T` / `topicThreshold`)
- number of clusters
- corpus size used
