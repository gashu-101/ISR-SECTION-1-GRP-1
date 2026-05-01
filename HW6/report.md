# HW6 Report — Feature Matrix Generation and Learning-to-Rank Style Pipeline

## Overview
HW6 focuses on generating a **feature matrix** for query-document pairs based on retrieval model scores, then applying a simple ML regression pipeline.

## Inputs
- Qrels: `qrels.adhoc.51-100.AP89.txt` (AP89)
- Retrieval model run files (TREC format), e.g.:
  - `OkapiBM25_Results_File.txt`
  - `OkapiTF_Results_File.txt`
  - `TF-IDF_Results_File.txt`
  - `UnigramLMLaplace_Results_File.txt`
  - `UnigramLMJM_Results_File.txt`
- Collection term frequencies pickle: `totalTF.p`
- Stoplist: resolved via repo-relative lookup (fixed for portability)

## Feature generation (`Feature_Matrix.py`)
- Loads relevance judgments and retrieval model scores.
- Aligns scores to a consistent set of (query, doc) pairs.
- Produces a CSV feature matrix:
  - Columns include: TF-IDF, Okapi TF, BM25, Laplace, Jelinek–Mercer, Label

## Learning script
- `ML_Learning Algorithms.py`
  - Reads the generated feature matrix.
  - Runs k-fold cross validation with a linear regression model.
  - Outputs a training performance file in TREC-like ranking format.

## How to run (high level)
1. Ensure retrieval model run files exist (from HW1/HW2).
2. Generate feature matrix:
   - `python HW6/Feature_Matrix.py`
3. Train/evaluate:
   - `python "HW6/ML_Learning Algorithms.py"`

## Notes / fixes
- `Feature_Matrix.py` previously had a hardcoded absolute stoplist path; it was updated to search repo-relative stoplist locations so it works on Windows.

## Results
Results depend on the underlying retrieval runs and qrels used for labeling.
