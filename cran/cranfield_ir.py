import math
import os
import re
from collections import Counter, defaultdict


_STOPWORDS = {
    "a","about","above","after","again","against","all","am","an","and","any","are","as","at",
    "be","because","been","before","being","below","between","both","but","by",
    "can","could",
    "did","do","does","doing","down","during",
    "each",
    "few","for","from","further",
    "had","has","have","having","he","her","here","hers","herself","him","himself","his","how",
    "i","if","in","into","is","it","its","itself",
    "just",
    "me","more","most","my","myself",
    "no","nor","not","now",
    "of","off","on","once","only","or","other","our","ours","ourselves","out","over","own",
    "s","same","she","should","so","some","such",
    "than","that","the","their","theirs","them","themselves","then","there","these","they","this","those",
    "through","to","too",
    "under","until","up",
    "very",
    "was","we","were","what","when","where","which","while","who","whom","why","will","with",
    "you","your","yours","yourself","yourselves",
}


_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _normalize_text(text: str) -> list[str]:
    tokens = _TOKEN_RE.findall(text.lower())
    return [t for t in tokens if len(t) > 1 and t not in _STOPWORDS]


def parse_cran_docs(path: str) -> dict[int, str]:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    docs: dict[int, str] = {}
    current_id: int | None = None
    current_parts: list[str] = []

    for line in content.splitlines():
        if line.startswith(".I "):
            if current_id is not None:
                docs[current_id] = "\n".join(current_parts).strip()
            current_id = int(line.split()[1])
            current_parts = []
        elif line.startswith(".T") or line.startswith(".A") or line.startswith(".B") or line.startswith(".W"):
            continue
        else:
            current_parts.append(line)

    if current_id is not None:
        docs[current_id] = "\n".join(current_parts).strip()

    return docs


def parse_cran_queries(path: str) -> dict[int, str]:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    queries: dict[int, str] = {}
    current_id: int | None = None
    current_parts: list[str] = []

    for line in content.splitlines():
        if line.startswith(".I "):
            if current_id is not None:
                queries[current_id] = "\n".join(current_parts).strip()
            current_id = int(line.split()[1])
            current_parts = []
        elif line.startswith(".W"):
            continue
        else:
            current_parts.append(line)

    if current_id is not None:
        queries[current_id] = "\n".join(current_parts).strip()

    return queries


def parse_cran_qrels(path: str, relevant_grades: set[int] | None = None) -> dict[int, dict[int, int]]:
    if relevant_grades is None:
        relevant_grades = {1, 2, 3, 4}

    qrels: dict[int, dict[int, int]] = defaultdict(dict)
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            cols = line.split()
            if len(cols) < 4:
                continue
            qid = int(cols[0])
            docid = int(cols[2])
            grade = int(cols[3])
            # keep grade as-is; evaluation can binarize or use graded
            if grade in relevant_grades:
                qrels[qid][docid] = grade

    return qrels


class CranfieldIndex:
    def __init__(self, docs: dict[int, str]):
        self.docs_raw = docs
        self.doc_tokens: dict[int, list[str]] = {}
        self.doc_tf: dict[int, Counter[str]] = {}
        self.df: Counter[str] = Counter()
        self.cf: Counter[str] = Counter()
        self.doc_len: dict[int, int] = {}
        self.avg_dl: float = 0.0
        self.vocab_size: int = 0
        self.total_tokens: int = 0

        for docid, text in docs.items():
            toks = _normalize_text(text)
            self.doc_tokens[docid] = toks
            tf = Counter(toks)
            self.doc_tf[docid] = tf
            self.doc_len[docid] = len(toks)
            self.cf.update(tf)
            for term in tf.keys():
                self.df[term] += 1

        self.total_tokens = sum(self.doc_len.values())
        self.avg_dl = (self.total_tokens / len(self.doc_len)) if self.doc_len else 0.0
        self.vocab_size = len(self.df)

    def okapi_tf_score(self, q_terms: list[str]) -> dict[int, float]:
        scores: dict[int, float] = defaultdict(float)
        avg_dl = self.avg_dl or 1.0
        for docid, tf in self.doc_tf.items():
            dl = self.doc_len[docid]
            denom_norm = 0.5 + 1.5 * (dl / avg_dl)
            s = 0.0
            for t in q_terms:
                tfwd = tf.get(t, 0)
                if tfwd:
                    s += tfwd / (tfwd + denom_norm)
            if s != 0.0:
                scores[docid] = s
        return scores

    def tfidf_score(self, q_terms: list[str]) -> dict[int, float]:
        scores: dict[int, float] = defaultdict(float)
        D = len(self.doc_tf)
        avg_dl = self.avg_dl or 1.0
        for docid, tf in self.doc_tf.items():
            dl = self.doc_len[docid]
            denom_norm = 0.5 + 1.5 * (dl / avg_dl)
            s = 0.0
            for t in q_terms:
                tfwd = tf.get(t, 0)
                if not tfwd:
                    continue
                df = self.df.get(t, 0)
                if df == 0:
                    continue
                ok = tfwd / (tfwd + denom_norm)
                s += ok * math.log(D / df)
            if s != 0.0:
                scores[docid] = s
        return scores

    def bm25_score(self, q_terms: list[str], k1: float = 1.2, k2: float = 100.0, b: float = 0.75) -> dict[int, float]:
        scores: dict[int, float] = defaultdict(float)
        D = len(self.doc_tf)
        avg_dl = self.avg_dl or 1.0
        qtf = Counter(q_terms)

        for docid, tf in self.doc_tf.items():
            dl = self.doc_len[docid]
            K = k1 * ((1 - b) + b * (dl / avg_dl))
            s = 0.0
            for t, tfwq in qtf.items():
                df = self.df.get(t, 0)
                if df == 0:
                    continue
                tfwd = tf.get(t, 0)
                if tfwd == 0:
                    continue
                idf = math.log((D + 0.5) / (df + 0.5))
                tf_part = (tfwd * (k1 + 1)) / (tfwd + K)
                q_part = (tfwq * (k2 + 1)) / (tfwq + k2)
                s += idf * tf_part * q_part
            if s != 0.0:
                scores[docid] = s
        return scores

    def lm_laplace_score(self, q_terms: list[str]) -> dict[int, float]:
        scores: dict[int, float] = {}
        V = self.vocab_size or 1
        for docid, tf in self.doc_tf.items():
            dl = self.doc_len[docid]
            s = 0.0
            for t in q_terms:
                tfwd = tf.get(t, 0)
                p = (tfwd + 1.0) / (dl + V)
                s += math.log(p)
            scores[docid] = s
        return scores

    def lm_jm_score(self, q_terms: list[str], lam: float = 0.4) -> dict[int, float]:
        scores: dict[int, float] = {}
        total_tokens = self.total_tokens or 1
        for docid, tf in self.doc_tf.items():
            dl = self.doc_len[docid] or 1
            s = 0.0
            for t in q_terms:
                p_doc = tf.get(t, 0) / dl
                p_bg = self.cf.get(t, 0) / total_tokens
                p = lam * p_doc + (1 - lam) * p_bg
                # guard against log(0)
                if p <= 0.0:
                    p = 1e-12
                s += math.log(p)
            scores[docid] = s
        return scores


def write_trec_run(run_path: str, scores_by_qid: dict[int, dict[int, float]], run_tag: str = "Exp", max_rank: int = 1000):
    os.makedirs(os.path.dirname(run_path), exist_ok=True)
    with open(run_path, "w", encoding="utf-8", errors="replace") as f:
        for qid in sorted(scores_by_qid.keys()):
            scored = sorted(scores_by_qid[qid].items(), key=lambda x: x[1], reverse=True)
            for rank, (docid, score) in enumerate(scored[:max_rank], start=1):
                f.write(f"{qid} Q0 {docid} {rank} {score:.6f} {run_tag}\n")


def evaluate_run(
    qrels: dict[int, dict[int, int]],
    run: dict[int, list[int]],
    k_values: list[int] | None = None,
) -> dict:
    if k_values is None:
        k_values = [5, 10, 20, 50]

    ap_list: list[float] = []
    rprec_list: list[float] = []
    ndcg_list: list[float] = []
    p_at: dict[int, list[float]] = {k: [] for k in k_values}

    for qid, rel_docs in qrels.items():
        ranked = run.get(qid, [])
        if not ranked:
            continue

        rel_set = set(rel_docs.keys())
        R = len(rel_set)
        if R == 0:
            continue

        hits = 0
        sum_prec = 0.0
        gains: list[int] = []

        for i, docid in enumerate(ranked, start=1):
            is_rel = 1 if docid in rel_set else 0
            if is_rel:
                hits += 1
                sum_prec += hits / i
            gains.append(is_rel)

            if i in p_at:
                p_at[i].append(hits / i)

        ap = sum_prec / R
        ap_list.append(ap)

        # R-precision
        top_r = ranked[:R]
        r_hits = sum(1 for d in top_r if d in rel_set)
        rprec_list.append(r_hits / R)

        # nDCG (binary)
        dcg = 0.0
        for i, g in enumerate(gains, start=1):
            dcg += g / math.log2(i + 1)
        ideal_gains = sorted(gains, reverse=True)
        idcg = 0.0
        for i, g in enumerate(ideal_gains, start=1):
            idcg += g / math.log2(i + 1)
        ndcg_list.append(0.0 if idcg == 0.0 else dcg / idcg)

    def mean(xs: list[float]) -> float:
        return sum(xs) / len(xs) if xs else 0.0

    out = {
        "MAP": mean(ap_list),
        "RPrec": mean(rprec_list),
        "nDCG": mean(ndcg_list),
        "P@": {k: mean(v) for k, v in p_at.items()},
        "num_queries": len(ap_list),
    }
    return out


def read_trec_run(run_path: str) -> dict[int, list[int]]:
    run: dict[int, list[int]] = defaultdict(list)
    with open(run_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            cols = line.strip().split()
            if len(cols) < 6:
                continue
            qid = int(cols[0])
            docid = int(cols[2])
            run[qid].append(docid)
    return run
