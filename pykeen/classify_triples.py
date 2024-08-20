import sys
import numpy as np
import pandas as pd
from prediction_and_evaluation_utility import classify_triples, evaluate_triple_classification

# model name
MODEL_NAME = sys.argv[1]

# file paths
VAL_MATRIX_FILEPATH = "../data/processed_data/val_matrix.csv"
TEST_MATRIX_FILEPATH = "../data/processed_data/test_matrix.csv"
VAL_RELATION_FILTER = "../data/processed_data/val_filter.csv"
TEST_RELATION_FILTER = "../data/processed_data/test_filter.csv"
TEST_UNLABELED_RELATION_FILTER = "../data/processed_data/unlabeled_test_filter.csv"
# model dependent filepaths
# scores and thresholds
SCORES_DIR = f"../data/predictions/{MODEL_NAME}/"
VAL_PROPERTY_SCORES_FILEPATH = f"{SCORES_DIR}val_scores.csv"
TEST_PROPERTY_SCORES_FILEPATH = f"{SCORES_DIR}test_scores.csv"
TEST_UNLABELED_PROPERTY_SCORES_FILEPATH = f"{SCORES_DIR}test_unlabeled_scores.csv"
THRESHOLDS_BEFORE_FILTER_FILEPATH = f"{SCORES_DIR}thresholds_before_filter.csv"
THRESHOLDS_AFTER_FILTER_FILEPATH = f"{SCORES_DIR}thresholds_after_filter.csv"
# predictions filepaths
VAL_PREDS_NO_FILTER_FILEPATH = f"{SCORES_DIR}val_predictions_no_filter.csv"
TEST_PREDS_NO_FILTER_FILEPATH = f"{SCORES_DIR}test_predictions_no_filter.csv"
TEST_UNLABELED_PREDS_NO_FILTER_FILEPATH = f"{SCORES_DIR}test_unlabeled_predictions_no_filter.csv"
VAL_PREDS_TBF_FILEPATH = f"{SCORES_DIR}val_predictions_tbf.csv"
TEST_PREDS_TBF_FILEPATH = f"{SCORES_DIR}test_predictions_tbf.csv"
TEST_UNLABELED_PREDS_TBF_FILEPATH = f"{SCORES_DIR}test_unlabeled_predictions_tbf.csv"
VAL_PREDS_TAF_FILEPATH = f"{SCORES_DIR}val_predictions_taf.csv"
TEST_PREDS_TAF_FILEPATH = f"{SCORES_DIR}test_predictions_taf.csv"
TEST_UNLABELED_PREDS_TAF_FILEPATH = f"{SCORES_DIR}test_unlabeled_predictions_taf.csv"
# evaluation filepaths
VAL_EVAL_NO_FILTER_FILEPATH = f"{SCORES_DIR}val_evaluation_no_filter.csv"
TEST_EVAL_NO_FILTER_FILEPATH = f"{SCORES_DIR}test_evaluation_no_filter.csv"
VAL_EVAL_TBF_FILEPATH = f"{SCORES_DIR}val_evaluation_tbf.csv"
TEST_EVAL_TBF_FILEPATH = f"{SCORES_DIR}test_evaluation_tbf.csv"
VAL_EVAL_TAF_FILEPATH = f"{SCORES_DIR}val_evaluation_taf.csv"
TEST_EVAL_TAF_FILEPATH = f"{SCORES_DIR}test_evaluation_taf.csv"

# read scores, ground truth labels, thresholds and filters
property_scores_val = pd.read_csv(VAL_PROPERTY_SCORES_FILEPATH)
property_scores_test = pd.read_csv(TEST_PROPERTY_SCORES_FILEPATH)
property_scores_test_unlabeled = pd.read_csv(TEST_UNLABELED_PROPERTY_SCORES_FILEPATH)
labels_val = pd.read_csv(VAL_MATRIX_FILEPATH)
labels_test = pd.read_csv(TEST_MATRIX_FILEPATH)
thresholds_before_filter = pd.read_csv(THRESHOLDS_BEFORE_FILTER_FILEPATH)
thresholds_after_filter = pd.read_csv(THRESHOLDS_AFTER_FILTER_FILEPATH)
val_relation_filter = pd.read_csv(VAL_RELATION_FILTER)
test_relation_filter = pd.read_csv(TEST_RELATION_FILTER)
test_unlabeled_relation_filter = pd.read_csv(TEST_UNLABELED_RELATION_FILTER)

# make predictions and save files
props = np.setdiff1d(property_scores_val.columns, ["subject", "object"])
# predictions without ontology-based filtering
predictions_val_no_filter = classify_triples(property_scores_val, thresholds_before_filter)
predictions_val_no_filter.to_csv(VAL_PREDS_NO_FILTER_FILEPATH, index=False)
predictions_test_no_filter = classify_triples(property_scores_test, thresholds_before_filter)
predictions_test_no_filter.to_csv(TEST_PREDS_NO_FILTER_FILEPATH, index=False)
predictions_test_unlabeled_no_filter = classify_triples(property_scores_test_unlabeled, thresholds_before_filter)
predictions_test_unlabeled_no_filter.to_csv(TEST_UNLABELED_PREDS_NO_FILTER_FILEPATH, index=False)
# predictions with ontology-based filtering and thresholds determined before filtering
predictions_val_tbf = classify_triples(property_scores_val, thresholds_before_filter)
predictions_val_tbf[props] = val_relation_filter[props] * predictions_val_tbf[props]
predictions_val_tbf.to_csv(VAL_PREDS_TBF_FILEPATH, index=False)
predictions_test_tbf = classify_triples(property_scores_test, thresholds_before_filter)
predictions_test_tbf[props] = test_relation_filter[props] * predictions_test_tbf[props]
predictions_test_tbf.to_csv(TEST_PREDS_TBF_FILEPATH, index=False)
predictions_test_unlabeled_tbf = classify_triples(property_scores_test_unlabeled, thresholds_before_filter)
predictions_test_unlabeled_tbf[props] = \
    test_unlabeled_relation_filter.sort_values(["subject", "object"]).reset_index()[props] \
    * predictions_test_unlabeled_tbf.sort_values(["subject", "object"]).reset_index()[props]
predictions_test_unlabeled_tbf.to_csv(TEST_UNLABELED_PREDS_TBF_FILEPATH, index=False)
# predictions with ontology-based filtering and thresholds determined after filtering
predictions_val_taf = classify_triples(property_scores_val, thresholds_after_filter)
predictions_val_taf[props] = val_relation_filter[props] * predictions_val_taf[props]
predictions_val_taf.to_csv(VAL_PREDS_TAF_FILEPATH, index=False)
predictions_test_taf = classify_triples(property_scores_test, thresholds_after_filter)
predictions_test_taf[props] = test_relation_filter[props] * predictions_test_taf[props]
predictions_test_taf.to_csv(TEST_PREDS_TAF_FILEPATH, index=False)
predictions_test_unlabeled_taf = classify_triples(property_scores_test_unlabeled, thresholds_after_filter)
predictions_test_unlabeled_taf[props] = \
    test_unlabeled_relation_filter.sort_values(["subject", "object"]).reset_index()[props] \
    * predictions_test_unlabeled_taf.sort_values(["subject", "object"]).reset_index()[props]
predictions_test_unlabeled_taf.to_csv(TEST_UNLABELED_PREDS_TAF_FILEPATH, index=False)

# run short evaluation and save files
# predictions without ontology-based filtering
evaluation_val_no_filter = evaluate_triple_classification(labels_val, predictions_val_no_filter)
evaluation_val_no_filter.to_csv(VAL_EVAL_NO_FILTER_FILEPATH, index=False)
evaluation_test_no_filter = evaluate_triple_classification(labels_test, predictions_test_no_filter)
evaluation_test_no_filter.to_csv(TEST_EVAL_NO_FILTER_FILEPATH, index=False)
# predictions with ontology-based filtering and thresholds determined before filtering
evaluation_val_tbf = evaluate_triple_classification(labels_val, predictions_val_tbf)
evaluation_val_tbf.to_csv(VAL_EVAL_TBF_FILEPATH, index=False)
evaluation_test_tbf = evaluate_triple_classification(labels_test, predictions_test_tbf)
evaluation_test_tbf.to_csv(TEST_EVAL_TBF_FILEPATH, index=False)
# predictions with ontology-based filtering and thresholds determined after filtering
evaluation_val_taf = evaluate_triple_classification(labels_val, predictions_val_taf)
evaluation_val_taf.to_csv(VAL_EVAL_TAF_FILEPATH, index=False)
evaluation_test_taf = evaluate_triple_classification(labels_test, predictions_test_taf)
evaluation_test_taf.to_csv(TEST_EVAL_TAF_FILEPATH, index=False)