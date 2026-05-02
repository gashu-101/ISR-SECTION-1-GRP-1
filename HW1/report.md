# HW1 Report — Retrieval Models with Elasticsearch (AP89)

## Overview
HW1 implements classic ad‑hoc retrieval models on the **TREC AP89** newswire collection using **Elasticsearch (ES)** as the index. Instead of relying on ES scoring, the system extracts term/document statistics (TF/DF/TTF, doc length) and computes ranking scores in Python.

## Dataset
- **Collection**: AP89 (from `AP89_DATA.zip`)
- **Queries**: `query_desc.51-100.short.txt` (as referenced in the homework description)
- **Qrels**: `qrels.adhoc.51-100.AP89.txt`

## Models implemented
- **ES built-in** (baseline via `match` query)
- **Okapi TF**
- **TF‑IDF** (Okapi TF * log(D/df))
- **BM25**
- **Unigram LM (Laplace smoothing)**
- **Unigram LM (Jelinek–Mercer smoothing)**

## Code structure (main scripts)
- `Create_Index.py`
  - Parses TREC documents and indexes into ES (`index1`, `doc_type=document`).
- `Query_Processing.py`
  - For each query term, retrieves matching documents from ES and builds per-query pickles:
    - `Pickles/docFreq{q}.p`
    - `Pickles/termVector{q}.p`
    - `Pickles/totalTF.p` (collection term frequencies used by LM)
- `Retrieval_Models.py`
  - Loads pickles and writes one TREC-format run file per model.

## Execution process (typical)
1. Start Elasticsearch locally.
2. Index the AP89 collection:
   - Run `python HW1/Create_Index.py`
3. Build per-query statistics (pickles):
   - Run `python HW1/Query_Processing.py`
4. Run ranking models:
   - Run `python HW1/Retrieval_Models.py`
5. Evaluate with `trec_eval`:
   - `trec_eval qrels.adhoc.51-100.AP89.txt <run_file>`

## Cranfield end-to-end (no Elasticsearch)

This repository includes the Cranfield dataset under `cran/`. To run HW1-style retrieval models end-to-end on Cranfield and generate real evaluation numbers:

```bash
python HW5/run_cranfield.py
```

Outputs:
- `results/cranfield/*.run.txt` (TREC-format run files)
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

## Output format
All run files follow TREC format:
```
<query-number> Q0 <docno> <rank> <score> Exp
```

## Evaluation
Recommended metrics (via `trec_eval`):
- MAP
- P@k
- R-Precision

## Notes / fixes applied in this codebase
To make the provided HW1 code runnable on Windows/Python 3, the following were fixed in the main code:
- Removed hardcoded absolute macOS paths in output.
- Updated Python 2-only constructs (`print`, `translate(None, ...)`, `dict.keys()[0]`, `filter()[0]`) to Python 3 equivalents.
- Made stoplist lookup portable (checks repo-relative locations).

## Results
This repository does not ship the AP89 dataset and qrels, so exact numeric results depend on local setup and are produced by running `trec_eval` on generated run files.
