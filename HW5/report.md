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

## Cranfield end-to-end run (included dataset)

This repository includes the Cranfield dataset under `cran/`. To run a complete Cranfield retrieval + evaluation pipeline and generate real metric numbers:

```bash
python HW5/run_cranfield.py
```

Outputs:
- `results/cranfield/*.run.txt`
- `results/cranfield/eval.json`
- `results/cranfield/eval.md`

### Cranfield evaluation results (binary relevance: grades 1–4)

| Model | MAP | R-Prec | nDCG | P@5 | P@10 |
|---|---:|---:|---:|---:|---:|
| OkapiTF | 0.6435 | 0.5480 | 0.8771 | 0.6933 | 0.4933 |
| TFIDF | 0.6379 | 0.5558 | 0.8738 | 0.6667 | 0.4933 |
| BM25 | 0.6267 | 0.5487 | 0.8624 | 0.6667 | 0.4933 |
| LM_Laplace | 0.6657 | 0.5575 | 0.8607 | 0.7200 | 0.4733 |
| LM_JM | 0.6246 | 0.5320 | 0.8330 | 0.6133 | 0.4867 |

## Results
Metric values depend on the run files provided and the qrels used.
