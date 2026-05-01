# HW2 Report — Custom Inverted Index + Stemming/Stopwords + Proximity Model

## Overview
HW2 replaces Elasticsearch (used in HW1) with a **self-designed inverted index** and re-implements retrieval models on top of that index. The homework also includes experiments comparing:
- **Stemmed vs. unstemmed** tokens
- **Stopwords removed vs. retained** (depending on script variant)
- A **proximity-based retrieval model**

## Dataset
- Primary target dataset per homework: **TREC AP89** (same as HW1)
- Queries: from `QueryUpdated.txt` (stored under `HW2/Files/`)

## Indexing variants (code)
Index building scripts:
- `Unstemmed_With_Stopwords_Index-1.py`
  - Builds an inverted index without stemming (and typically retains stopwords).
- `Stemmed_Stopwords_Removed_Index-1.py`
  - Builds an inverted index with stemming and stopword removal.

Generated index artifacts are stored under `HW2/Files/` (and subfolders), including:
- Pickled term maps / doc maps
- Catalog files (`catalogFile.txt`) for term → offsets
- Term vectors / term statistics for query processing

## Retrieval models (code)
Retrieval scripts:
- `Retrieval_Models.py` (unstemmed)
- `Retrieval_Models_Stemmed.py` (stemmed)

Implemented models:
- **Okapi TF**
- **TF‑IDF**
- **BM25**
- **Unigram LM (Laplace)**
- **Unigram LM (Jelinek–Mercer)**
- **Proximity scoring model** (minimum-span / window-based scoring)

Outputs are written in TREC format:
```
<query-number> Q0 <docno> <rank> <score> Exp
```

## Query processing
Query scripts:
- `Query_Processing.py`
- `Query_Processing_Stemmed.py`
- `Query_Processing_Stemmed_Proximity.py`
- `Query_Processing_Unstemmed_Proximity.py`

These scripts tokenize queries consistently with the index variant and generate per-query term vectors / stats used by the retrieval scripts.

## How to run (typical)
1. Build the index (choose one variant):
   - `python HW2/Unstemmed_With_Stopwords_Index-1.py`
   - `python HW2/Stemmed_Stopwords_Removed_Index-1.py`
2. Run query processing for the same variant.
3. Run retrieval models to produce run files.
4. Evaluate using `trec_eval` (or the evaluation scripts in HW5).

## Evaluation
- Use `trec_eval` with AP89 qrels (`qrels.adhoc.51-100.AP89.txt`).
- Compare retrieval effectiveness across stemming/stopword variants.
- Inspect proximity model changes compared to standard bag-of-words models.

## Notes
- This repo includes demo scripts (`Demo_Stemmed.py`, `Demo_Unstemmed.py`, `Demo_Related.py`) to illustrate usage for different variants.
- Exact results depend on local AP89 dataset placement and consistent preprocessing.
