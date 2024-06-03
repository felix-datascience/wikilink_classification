import pandas as pd
from prediction_and_evaluation_utility import find_thresholds

# model name
MODEL_NAME = "transE_model1"

# file paths
VAL_MATRIX_FILEPATH = "../data/processed_data/val_matrix.csv"
# model dependent filepaths
SCORES_DIR = f"../data/predictions/{MODEL_NAME}/"
VAL_PROPERTY_SCORES_FILEPATH = f"{SCORES_DIR}val_scores.csv"
THRESHOLDS_FILEPATH = f"{SCORES_DIR}thresholds.csv"

# read scores and ground truth labels
scores = pd.read_csv(VAL_PROPERTY_SCORES_FILEPATH)
labels = pd.read_csv(VAL_MATRIX_FILEPATH)

# calculate thresholds and save file
thresholds = find_thresholds(scores, labels)
thresholds.to_csv(THRESHOLDS_FILEPATH, index=False)