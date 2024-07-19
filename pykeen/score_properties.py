import sys
import os
import pandas as pd
import torch
from pykeen.triples import TriplesFactory
from prediction_and_evaluation_utility import true_properties_matrix, score_properties

# model name
MODEL_NAME = sys.argv[1]

# file paths
TRAIN_PATH = "../data/processed_data/train.tsv"
VAL_PATH = "../data/processed_data/val.tsv"
TEST_PATH = "../data/processed_data/test.tsv"
VAL_MATRIX_FILEPATH = "../data/processed_data/val_matrix.csv"
TEST_MATRIX_FILEPATH = "../data/processed_data/test_matrix.csv"
# model dependent filepaths
MODEL_FILEPATH = f"results/{MODEL_NAME}/trained_model.pkl"
ENTITY_TO_ID_FILEPATH = f"results/{MODEL_NAME}/training_triples/entity_to_id.tsv.gz"
RELATION_TO_ID_FILEPATH = f"results/{MODEL_NAME}/training_triples/relation_to_id.tsv.gz"
SCORES_DIR = f"../data/predictions/{MODEL_NAME}/"
VAL_PROPERTY_SCORES_FILEPATH = f"{SCORES_DIR}val_scores.csv"
TEST_PROPERTY_SCORES_FILEPATH = f"{SCORES_DIR}test_scores.csv"

# create directory for storing property scores (if it doesn't exist yet)
if not os.path.isdir(SCORES_DIR):
    os.makedirs(SCORES_DIR)

# load validation matrix file or create it if it doesn't exist yet
if os.path.isfile(VAL_MATRIX_FILEPATH):
    true_properties_val = pd.read_csv(VAL_MATRIX_FILEPATH)
else:
    true_properties_val = true_properties_matrix(VAL_PATH)
    true_properties_val.to_csv(VAL_MATRIX_FILEPATH, index=False)

# load testing matrix file or create it if it doesn't exist yet
if os.path.isfile(TEST_MATRIX_FILEPATH):
    true_properties_test = pd.read_csv(TEST_MATRIX_FILEPATH)
else:
    true_properties_test = true_properties_matrix(TEST_PATH)
    true_properties_test.to_csv(TEST_MATRIX_FILEPATH, index=False)

# take entity pairs from validation and testing sets
entity_pairs_val = true_properties_val[["subject", "object"]].to_numpy()
entity_pairs_test = true_properties_test[["subject", "object"]].to_numpy()

# load training triples factory and model
entity_to_id_dict = pd.read_csv(ENTITY_TO_ID_FILEPATH, compression="gzip", sep="\t")
entity_to_id_dict = dict(zip(entity_to_id_dict["label"], entity_to_id_dict["id"]))
relation_to_id_dict = pd.read_csv(RELATION_TO_ID_FILEPATH, compression="gzip", sep="\t")
relation_to_id_dict = dict(zip(relation_to_id_dict["label"], relation_to_id_dict["id"]))
training = TriplesFactory.from_path(
    path=TRAIN_PATH,
    entity_to_id=entity_to_id_dict,
    relation_to_id=relation_to_id_dict,
)
model = torch.load(MODEL_FILEPATH)

# generate property scores for validation set
property_scores_val = score_properties(entity_pairs_val, model, training, relation_to_id_dict)
property_scores_val.to_csv(VAL_PROPERTY_SCORES_FILEPATH, index=False)

# generate property scores for testing set
property_scores_test = score_properties(entity_pairs_test, model, training, relation_to_id_dict)
property_scores_test.to_csv(TEST_PROPERTY_SCORES_FILEPATH, index=False)