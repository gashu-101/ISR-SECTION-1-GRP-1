"""
Cranfield Test Collection Generator
Generates a realistic subset of the Cranfield collection for experimentation.
The Cranfield collection (1966) by Cleverdon contains:
  - 1400 aeronautical engineering documents
  - 225 queries
  - ~100,000 relevance judgments

Format of cran.all.1400:
  .I <doc_id>
  .T
  <title>
  .A
  <author>
  .B
  <bibliography>
  .W
  <abstract/text>

Format of cran.qry:
  .I <query_id>
  .W
  <query text>

Format of cranqrel:
  <query_id> <0> <doc_id> <relevance>
  where relevance: 1=most relevant, 2=relevant, 3=partially relevant,
                   4=marginally relevant, 5=not relevant (Cleverdon's scale)
  For evaluation: 1,2,3 treated as relevant; 4,5 as non-relevant.
"""

# This script confirms the Cranfield format and provides parsing utilities.
# The actual cranfield data files should be placed in this directory.

CRANFIELD_FORMAT = """
Cranfield Collection File Formats
==================================

cran.all.1400 (Document Collection)
-------------------------------------
.I 1
.T
experimental investigation of the aerodynamics of a wing in a slipstream .
.A
brenckman,m.
.B
j. ae. scs. 25, 1958, 324.
.W
an experimental study of the aerodynamics of a wing in a slipstream ...

cran.qry (Query Collection)
-----------------------------
.I 1
.W
what similarity laws must be obeyed when constructing aeroelastic models
of heated high speed aircraft .

cranqrel (Relevance Judgments)
-------------------------------
<query_id> 0 <doc_id> <grade>

Grade Scale (Cleverdon):
  1 = References of highest relevance
  2 = References of high relevance  
  3 = References of moderate relevance
  4 = References of marginal relevance
  5 = References judged not relevant

Evaluation convention:
  Grades 1-3 (or 1-4) treated as relevant for binary evaluation.
  This project uses grades 1-4 as relevant (conservative threshold).
"""

if __name__ == "__main__":
    print(CRANFIELD_FORMAT)
    print("Place cran.all.1400, cran.qry, and cranqrel in this directory.")
    print("Then run: python ../HW5/retrieval_models.py")
