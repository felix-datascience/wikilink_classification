from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory
from torch.nn.functional import normalize
from pykeen.nn.init import xavier_uniform_, xavier_uniform_norm_

# model name
MODEL_NAME = "transE_bordes_hrt"

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
    result_tracker="csv",
    result_tracker_kwargs=dict(
        name=RESULTS_TRACKER_PATH,
    ),
    # epochs and batch size
    training_kwargs=dict(
        num_epochs=100,
        batch_size=128,
        checkpoint_name=CHECKPOINT_NAME,
    ),
    random_seed=42,
    # embedding size and scoring function norm
    model_kwargs=dict(
        embedding_dim=50,
        scoring_fct_norm=2
    ),
    # negative sampling
    negative_sampler="basic",
    negative_sampler_kwargs=dict(
        corruption_scheme=("head", "relation", "tail"),
    ),
    # loss
    loss="MarginRankingLoss",
    loss_kwargs=dict(
        margin=1
    ),
    # optimizer
    optimizer="SGD",
    optimizer_kwargs=dict(
        lr=0.01
    ),
    # regularization
    regularizer=None,
    # embedding normalization
    entity_constrainer=normalize,
    relation_constrainer=None,
    # embedding initialization
    entity_initializer=xavier_uniform_,
    relation_initializer=xavier_uniform_norm_,
)

# save results
results.save_to_directory(RESULTS_DIR)
