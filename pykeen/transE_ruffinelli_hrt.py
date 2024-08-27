from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory
from pykeen.nn.init import xavier_normal_
from pykeen_extensions import ComplexNegativeSampler, TransE_separate_regularizers

# model name
MODEL_NAME = "transE_ruffinelli_hrt"

# training, validation and test data file paths
TRAIN_PATH = "../data/processed_data/train.tsv"
VAL_PATH = "../data/processed_data/val.tsv"
TEST_PATH = "../data/processed_data/test.tsv"

# results, tracker and checkpoint file paths
RESULTS_DIR = f"../data/model_results/{MODEL_NAME}"
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
    model=TransE_separate_regularizers,
    training_loop="sLCWA",
    result_tracker="csv",
    result_tracker_kwargs=dict(
        name=RESULTS_TRACKER_PATH,
    ),
    # epochs and batch size
    training_kwargs=dict(
        num_epochs=10,
        batch_size=128,
        checkpoint_name=CHECKPOINT_NAME,
    ),
    random_seed=42,
    model_kwargs=dict(
        # embedding size and scoring function norm
        embedding_dim=512,
        scoring_fct_norm=2,
        # embedding normalization
        entity_constrainer=None,
        relation_constrainer=None,
        # embedding initialization
        entity_initializer=xavier_normal_,
        relation_initializer=xavier_normal_,
    ),
    # negative sampling
    negative_sampler=ComplexNegativeSampler,
    negative_sampler_kwargs=dict(
        n_subject_samples=2,
        n_predicate_samples=10,
        n_object_samples=56
    ),
    # loss
    loss="CrossEntropyLoss",
    # optimizer
    optimizer="Adagrad",
    optimizer_kwargs=dict(
        lr=0.0003
    ),
    lr_scheduler="ExponentialLR",
    lr_scheduler_kwargs=dict(
        gamma=0.95
    ),
)

# save results
results.save_to_directory(RESULTS_DIR)
