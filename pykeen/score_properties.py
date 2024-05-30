import os
import pandas as pd
import torch
from pykeen.constants import PYKEEN_CHECKPOINTS
from pykeen.triples import TriplesFactory
from pykeen.models import TransE
from prediction_and_evaluation_utility import true_properties_matrix, score_properties

# model name
MODEL_NAME = "transE_model1"

# file paths
TRAIN_PATH = "../data/processed_data/train.tsv"
VAL_PATH = "../data/processed_data/val.tsv"
TEST_PATH = "../data/processed_data/test.tsv"
VAL_MATRIX_FILEPATH = "../data/processed_data/val_matrix.csv"
TEST_MATRIX_FILEPATH = "../data/processed_data/test_matrix.csv"
# model dependent filepaths
CHECKPOINT_NAME = f"{MODEL_NAME}_checkpoint.pt"
SCORES_DIR = f"../data/predictions/{MODEL_NAME}/"
VAL_PROPERTY_SCORES_FILEPATH = f"{SCORES_DIR}val_scores.csv"
TEST_PROPERTY_SCORES_FILEPATH = f"{SCORES_DIR}test_scores.csv"

# create directory for storing property scores (if it doesn't exist yet)
if not os.path.isdir(SCORES_DIR):
    os.mkdir(SCORES_DIR)

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
checkpoint = torch.load(PYKEEN_CHECKPOINTS.joinpath(CHECKPOINT_NAME), map_location=torch.device('cpu'))
training = TriplesFactory.from_path(
    path=TRAIN_PATH,
    entity_to_id=checkpoint['entity_to_id_dict'],
    relation_to_id=checkpoint['relation_to_id_dict'],
)
model = TransE(triples_factory=training)
model.load_state_dict(checkpoint['model_state_dict'])

# generate property scores for validation set
property_scores_val = score_properties(entity_pairs_val, model, training, checkpoint["relation_to_id_dict"])
property_scores_val.to_csv(VAL_PROPERTY_SCORES_FILEPATH, index=False)

# generate property scores for testing set
property_scores_test = score_properties(entity_pairs_test, model, training, checkpoint["relation_to_id_dict"])
property_scores_test.to_csv(TEST_PROPERTY_SCORES_FILEPATH, index=False)