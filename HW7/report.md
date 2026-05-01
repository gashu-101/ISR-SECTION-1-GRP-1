# HW7 Report — Machine Learning for Email Spam Filtering

## Overview
HW7 implements an ML pipeline for **email spam filtering**. The provided code builds a feature representation of emails and trains a classifier (Logistic Regression in the main script).

## Dataset
- Intended dataset per student report: **TREC07p** email corpus.
- Labels are typically read from an index file (spam/ham).

## Code structure
- `EmailFilter.py`
  - Parses raw emails and extracts text content.
- `FeatureMatrix.py`
  - Builds feature vectors (document-term / n-grams).
- `MachineLeaning.py`
  - Trains a Logistic Regression model.
  - Performs k-fold split and prints accuracy.
  - Performs feature selection using `SelectKBest(f_classif)`.

## How to run (high level)
1. Prepare the dataset and any required index/label files.
2. Generate feature matrix (CSV).
3. Train/evaluate model:
   - `python HW7/MachineLeaning.py`

## Notes / fixes
- Updated deprecated `Imputer` usage to `SimpleImputer` so the script works with modern scikit-learn.
- Fixed `Tagger.py` indentation error so the HW7 package compiles.

## Results
Accuracy and top features depend on the dataset slice and the feature matrix used (e.g., `staticFeatureMatrixFull200.csv`).
