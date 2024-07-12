from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory
from torch.nn.init import normal_

# model name
MODEL_NAME = "complEx_trouillon_ht"

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
    model="ComplEx",
    training_loop="sLCWA",
    result_tracker="csv",
    result_tracker_kwargs=dict(
        name=RESULTS_TRACKER_PATH,
    ),
    # epochs and batch size
    training_kwargs=dict(
        num_epochs=10,
        batch_size=100,
        checkpoint_name=CHECKPOINT_NAME,
    ),
    random_seed=42,
    model_kwargs=dict(
        # embedding size
        embedding_dim=200,
        # embedding initialization
        entity_initializer=normal_,
        relation_initializer=normal_,
    ),
    # negative sampling
    negative_sampler="basic",
    negative_sampler_kwargs=dict(
        corruption_scheme=("head", "tail"),
        num_negs_per_pos=100
    ),
    # loss
    loss="SoftplusLoss",
    loss_kwargs=dict(
        reduction="mean"
    ),
    # optimizer
    optimizer="Adagrad",
    optimizer_kwargs=dict(
        lr=0.5
    ),
    # regularization
    regularizer="LpRegularizer",
    regularizer_kwargs=dict(
        weight=0.001,
        p=2
    ),
)

# save results
results.save_to_directory(RESULTS_DIR)
