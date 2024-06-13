from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory

# model name
MODEL_NAME = "transE_model2"

# training, validation and test data file paths
TRAIN_PATH = "../data/processed_data/train.tsv"
VAL_PATH = "../data/processed_data/val.tsv"
TEST_PATH = "../data/processed_data/test.tsv"

# results, tracker and checkpoint file paths
RESULTS_DIR = f"results/{MODEL_NAME}"
RESULTS_TRACKER_PATH = f"{MODEL_NAME}.csv"
CHECKPOINT_NAME = f"{MODEL_NAME}_checkpoint.pt"

# create triple factories
training = TriplesFactory.from_path(TRAIN_PATH)

validation = TriplesFactory.from_path(
    VAL_PATH,
    entity_to_id=training.entity_to_id,
    relation_to_id=training.relation_to_id,
)

testing = TriplesFactory.from_path(
    TEST_PATH,
    entity_to_id=training.entity_to_id,
    relation_to_id=training.relation_to_id,
)

# train model
results = pipeline(
    training=training,
    testing=testing,
    model="TransE",
    training_loop="sLCWA",
    loss="CrossEntropyLoss",
    optimizer="Adam",
    training_kwargs=dict(
        num_epochs=20,
        checkpoint_name=CHECKPOINT_NAME,
    ),
    negative_sampler="basic",
    negative_sampler_kwargs=dict(
        corruption_scheme=("head", "relation", "tail"),
    ),
    result_tracker="csv",
    result_tracker_kwargs=dict(
        name=RESULTS_TRACKER_PATH,
    ),
    random_seed=42,
)

# save results
results.save_to_directory(RESULTS_DIR)
