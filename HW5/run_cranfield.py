import json
import os
import sys


def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from cran.cranfield_ir import (
        CranfieldIndex,
        _normalize_text,
        evaluate_run,
        parse_cran_docs,
        parse_cran_qrels,
        parse_cran_queries,
        read_trec_run,
        write_trec_run,
    )
    cran_dir = os.path.join(repo_root, "cran")

    docs_path = os.path.join(cran_dir, "cran.all.1400")
    queries_path = os.path.join(cran_dir, "cran.qry")
    qrels_path = os.path.join(cran_dir, "cranqrel")

    out_dir = os.path.join(repo_root, "results", "cranfield")
    os.makedirs(out_dir, exist_ok=True)

    docs = parse_cran_docs(docs_path)
    queries = parse_cran_queries(queries_path)
    qrels = parse_cran_qrels(qrels_path)

    index = CranfieldIndex(docs)

    models = {
        "OkapiTF": lambda qt: index.okapi_tf_score(qt),
        "TFIDF": lambda qt: index.tfidf_score(qt),
        "BM25": lambda qt: index.bm25_score(qt),
        "LM_Laplace": lambda qt: index.lm_laplace_score(qt),
        "LM_JM": lambda qt: index.lm_jm_score(qt, lam=0.4),
    }

    eval_summary = {}

    for name, scorer in models.items():
        scores_by_qid = {}
        for qid in sorted(queries.keys()):
            q_terms = _normalize_text(queries[qid])

            scores_by_qid[qid] = scorer(q_terms)

        run_path = os.path.join(out_dir, f"{name}.run.txt")
        write_trec_run(run_path, scores_by_qid, run_tag="Cranfield")

        run = read_trec_run(run_path)
        metrics = evaluate_run(qrels, run)
        eval_summary[name] = metrics

    with open(os.path.join(out_dir, "eval.json"), "w", encoding="utf-8") as f:
        json.dump(eval_summary, f, indent=2)

    # Write a small markdown table for easy copy/paste into reports
    md_lines = []
    md_lines.append("| Model | MAP | R-Prec | nDCG | P@5 | P@10 |")
    md_lines.append("|---|---:|---:|---:|---:|---:|")
    for name in ["OkapiTF", "TFIDF", "BM25", "LM_Laplace", "LM_JM"]:
        m = eval_summary[name]
        md_lines.append(
            "| {} | {:.4f} | {:.4f} | {:.4f} | {:.4f} | {:.4f} |".format(
                name,
                m["MAP"],
                m["RPrec"],
                m["nDCG"],
                m["P@"][5],
                m["P@"][10],
            )
        )

    with open(os.path.join(out_dir, "eval.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines) + "\n")

    print("Wrote runs + eval to:", out_dir)
    print("\n".join(md_lines))


if __name__ == "__main__":
    main()
