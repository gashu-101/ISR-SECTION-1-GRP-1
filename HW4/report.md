# HW4 Report — Graph-Based Ranking (PageRank, HITS)

## Overview
HW4 implements **graph-based ranking algorithms** used in information retrieval:
- **PageRank** (global prestige)
- **HITS** (query-dependent authority/hub)

## Dataset / inputs
Two sources appear in this codebase:
- **WT2G in-link graph** style file (for PageRank): the script reads `wt2g_inlinks.txt`.
- **Elasticsearch crawl index** (for Graph/HITS): scripts reference ES index `hw3_crawl` and read/write `linkgraph.txt`.

Because the required input files / ES index are not shipped here, running HW4 requires you to supply:
- a link graph file (in-links format), and/or
- an ES index containing documents with `outlinks`.

## Code structure
- `Graph.py`
  - Builds an in-link graph from an Elasticsearch crawl index (`hw3_crawl`) by reading each document’s `outlinks`.
  - Writes `linkgraph.txt`.
- `PageRank.py`
  - Loads an in-link graph file and iteratively computes PageRank.
  - Uses perplexity-based convergence (change < 1 for 4 consecutive rounds).
  - Writes ranked pages to `wt2g_rank.txt`.
- `HITS.py`
  - Builds a root/base set using an Elasticsearch query and the link graph.
  - Runs HITS updates (authority/hub) for a fixed number of iterations.
  - Writes `hub.txt` and `authority.txt`.

## Algorithms
### PageRank
- Damping factor `d = 0.85`
- Sink PR redistribution
- Convergence via perplexity

### HITS
- Builds root set from ES results of a query
- Base set expansion via outlinks/inlinks
- Iterative authority/hub updates (50 iterations in current script)

## How to run (high level)
1. Prepare data:
   - Ensure ES is running and `hw3_crawl` exists with `outlinks` field, OR provide a link graph file in the expected format.
2. Build `linkgraph.txt` (if using ES crawl):
   - `python HW4/Graph.py`
3. Run PageRank:
   - `python HW4/PageRank.py`
4. Run HITS:
   - `python HW4/HITS.py`

## Outputs
- `linkgraph.txt`
- `wt2g_rank.txt`
- `hub.txt`
- `authority.txt`

## Notes
A student manual report in `Reports/` referenced Cranfield-based experiments for HW4/HW5; however, the **main repo HW4 scripts are currently wired to WT2G / ES crawl inputs**, not Cranfield. If you want Cranfield-based HW4, the HW4 scripts would need to be adapted to a Cranfield citation graph input.
