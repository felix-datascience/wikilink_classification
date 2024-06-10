from pykeen.hpo import hpo_pipeline
from pykeen.triples import TriplesFactory

# model name
MODEL_NAME = "transE_hpo"

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
hpo_pipeline_results = hpo_pipeline(
    n_trials=20,
    training=training,
    testing=testing,
    model="TransE",
    training_loop="sLCWA",
    # use adagrad optimizer
    optimizer="Adagrad",
    training_kwargs=dict(
        num_epochs=1000,
        checkpoint_name=CHECKPOINT_NAME,
    ),
    model_kwargs_ranges=dict(
        # optimize embedding dimension
        embedding_dim=dict(type=int, low=100, high=600, q=100),
        # optimize l_p norm applied in the interaction function
        scoring_fct_norm=dict(type=int, low=1, high=2)
    ),
    negative_sampler="basic",
    negative_sampler_kwargs=dict(
        corruption_scheme=("head", "tail"),
    ),
    loss='MarginRankingLoss',
    loss_kwargs_ranges=dict(
        # optimize margin
        margin=dict(type=float, low=1.0, high=2.0),
    ),
    # use learning rate scheduler
    lr_scheduler='ExponentialLR',
    result_tracker="csv",
    result_tracker_kwargs=dict(
        name=RESULTS_TRACKER_PATH,
    ),
    random_seed=42,
)

# save results
hpo_pipeline_results.save_to_directory(RESULTS_DIR)
