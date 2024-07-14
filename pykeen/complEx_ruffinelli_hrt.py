from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory
from torch.nn.init import uniform_
from pykeen_extensions import ComplexNegativeSampler, ComplEx_dropout_and_separate_regularizers
import torch

# model name
MODEL_NAME = "complEx_ruffinelli_hrt"

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

# overwrite torch dropout function so that pykeen is forced to use it
original_torch_dropout = torch.nn.functional.dropout
def dropout_complex(input, p=0.5, training=True, inplace=False):
    # work around for unimplemented dropout for complex data type
    # source: https://discuss.pytorch.org/t/how-can-i-dropout-for-torch-complex-data-type/135577
    if input.is_complex():
        mask = original_torch_dropout(torch.ones_like(input.real), p=p, training=training, inplace=inplace)
        return input * mask
    else:
        return original_torch_dropout(input, p=p, training=training, inplace=inplace)
torch.nn.functional.dropout = dropout_complex

# train model
results = pipeline(
    training=training,
    testing=testing,
    model=ComplEx_dropout_and_separate_regularizers,
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
        embedding_dim=256,
        # embedding initialization
        entity_initializer=uniform_,
        entity_initializer_kwargs=dict(
            a=-0.85,
            b=0.85
        ),
        relation_initializer=uniform_,
        relation_initializer_kwargs=dict(
            a=-0.85,
            b=0.85
        ),
    ),
    # negative sampling
    negative_sampler=ComplexNegativeSampler,
    negative_sampler_kwargs=dict(
        n_subject_samples=557,
        n_predicate_samples=100,
        n_object_samples=376,
    ),
    # loss
    loss="CrossEntropyLoss",
    # optimizer
    optimizer="Adagrad",
    optimizer_kwargs=dict(
        lr=0.18255
    ),
    lr_scheduler="ExponentialLR",
    lr_scheduler_kwargs=dict(
        gamma=0.95
    ),
)

# save results
results.save_to_directory(RESULTS_DIR)