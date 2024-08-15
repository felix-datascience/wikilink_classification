import sys
import pandas as pd
import numpy as np
from prediction_and_evaluation_utility import find_thresholds

# model name
MODEL_NAME = sys.argv[1]

# file paths
VAL_MATRIX_FILEPATH = "../data/processed_data/val_matrix.csv"
VAL_FILTER_FILEPATH = "../data/processed_data/val_filter.csv"
# model dependent filepaths
SCORES_DIR = f"../data/predictions/{MODEL_NAME}/"
VAL_PROPERTY_SCORES_FILEPATH = f"{SCORES_DIR}val_scores.csv"
THRESHOLDS_BEFORE_FILTER_FILEPATH = f"{SCORES_DIR}thresholds_before_filter.csv"
THRESHOLDS_AFTER_FILTER_FILEPATH = f"{SCORES_DIR}thresholds_after_filter.csv"

# read scores and ground truth labels
scores = pd.read_csv(VAL_PROPERTY_SCORES_FILEPATH)
filter = pd.read_csv(VAL_FILTER_FILEPATH)
labels = pd.read_csv(VAL_MATRIX_FILEPATH)

# calculate thresholds before applying the relation filter and save file
thresholds_before_filter = find_thresholds(scores, labels, use_optuna=True, n_trials=300)
thresholds_before_filter.to_csv(THRESHOLDS_BEFORE_FILTER_FILEPATH, index=False)

# calculate thresholds after applying the relation filter and save file
props = np.setdiff1d(scores.columns, ["subject", "object"])
scores[props] = filter[props] * scores[props]
thresholds_after_filter = find_thresholds(scores, labels, use_optuna=True, n_trials=300)
thresholds_after_filter.to_csv(THRESHOLDS_AFTER_FILTER_FILEPATH, index=False)