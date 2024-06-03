import pandas as pd
from prediction_and_evaluation_utility import classify_triples, evaluate_triple_classification

# model name
MODEL_NAME = "transE_model1"

# file paths
VAL_MATRIX_FILEPATH = "../data/processed_data/val_matrix.csv"
TEST_MATRIX_FILEPATH = "../data/processed_data/test_matrix.csv"
# model dependent filepaths
SCORES_DIR = f"../data/predictions/{MODEL_NAME}/"
VAL_PROPERTY_SCORES_FILEPATH = f"{SCORES_DIR}val_scores.csv"
TEST_PROPERTY_SCORES_FILEPATH = f"{SCORES_DIR}test_scores.csv"
THRESHOLDS_FILEPATH = f"{SCORES_DIR}thresholds.csv"
VAL_PREDS_FILEPATH = f"{SCORES_DIR}val_predictions.csv"
TEST_PREDS_FILEPATH = f"{SCORES_DIR}test_predictions.csv"
VAL_EVAL_FILEPATH = f"{SCORES_DIR}val_evaluation.csv"
TEST_EVAL_FILEPATH = f"{SCORES_DIR}test_evaluation.csv"

# read scores, ground truth labels and thresholds
property_scores_val = pd.read_csv(VAL_PROPERTY_SCORES_FILEPATH)
property_scores_test = pd.read_csv(TEST_PROPERTY_SCORES_FILEPATH)
labels_val = pd.read_csv(VAL_MATRIX_FILEPATH)
labels_test = pd.read_csv(TEST_MATRIX_FILEPATH)
thresholds = pd.read_csv(THRESHOLDS_FILEPATH)

# make predictions and save files
predictions_val = classify_triples(property_scores_val, thresholds)
predictions_val.to_csv(VAL_PREDS_FILEPATH, index=False)
predictions_test = classify_triples(property_scores_test, thresholds)
predictions_test.to_csv(TEST_PREDS_FILEPATH, index=False)

# run short evaluation and save files
evaluation_val = evaluate_triple_classification(labels_val, predictions_val)
evaluation_val.to_csv(VAL_EVAL_FILEPATH, index=False)
evaluation_test = evaluate_triple_classification(labels_test, predictions_test)
evaluation_test.to_csv(TEST_EVAL_FILEPATH, index=False)