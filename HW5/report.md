# HW5 Report — TREC Preparation and Evaluation Utilities

## Overview
HW5 contains utilities for **preparing TREC-style qrels/run files** and computing evaluation metrics similar to `trec_eval`.

## Code structure
- `Trec_Prep.py`
  - Prepares qrels and a rank list from raw inputs.
  - Uses Elasticsearch to retrieve ranked results for sample queries.
- `Trec_Eval.py`
  - Reads a qrels file and a run file (rank list) in TREC format.
  - Computes:
    - Average Precision (AP) and mean AP
    - R-Precision
    - nDCG
    - Precision@k / Recall@k / F1@k for k ∈ {5, 10, 20, 50, 100}

## Input formats
### Qrels
Expected per line:
```
<query_id> 0 <doc_id> <relevance>
```
Current evaluation code treats relevance as binary where `relevance == '1'` means relevant.

### Run / Rank list
Expected per line:
```
<query_id> Q0 <doc_id> <rank> <score> Exp
```

## How to run
`Trec_Eval.py` is interactive: it expects a command similar to `trec_eval`.
Examples:
- With per-query output:
  - `trec_eval -q qrels.txt rankList.txt`
- Summary only:
  - `trec_eval qrels.txt rankList.txt`

## Notes about Cranfield
A student manual report (from `Reports/`) describes Cranfield evaluation and Cleverdon grades. This repository now includes a permanent `cran/` folder at repo root with:
- `cran.all.1400`
- `cran.qry`
- `cranqrel`

However, the **HW5 scripts in the main repo are not currently wired to Cranfield** (they reference AP89-like qrels and Elasticsearch usage). If you want HW5 evaluation on Cranfield, you would:
- parse `cranqrel` into qrels format (binary or graded), and
- generate run files for the Cranfield queries.

## Results
Metric values depend on the run files provided and the qrels used.
