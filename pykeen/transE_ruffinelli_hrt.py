from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory
from pykeen.nn.init import xavier_normal_

from class_resolver import Hint, HintOrType, OptionalKwargs
from torch.nn import functional
from pykeen.models.nbase import ERModel
from pykeen.nn import TransEInteraction
from pykeen.nn.init import xavier_uniform_, xavier_uniform_norm_
from pykeen.regularizers import Regularizer
from pykeen.typing import Constrainer, Initializer

class TransE_separate_regularizers(ERModel):
    """
    TransE model with separate regularizers for entity and relation.
    """
    def __init__(
        self,
        *,
        embedding_dim: int = 50,
        scoring_fct_norm: int = 1,
        entity_initializer: Hint[Initializer] = xavier_uniform_,
        entity_constrainer: Hint[Constrainer] = functional.normalize,
        relation_initializer: Hint[Initializer] = xavier_uniform_norm_,
        relation_constrainer: Hint[Constrainer] = None,
        entity_regularizer: HintOrType[Regularizer] = "LpRegularizer",
        entity_regularizer_kwargs: OptionalKwargs = dict(weight=1.32*10**-7, p=2),
        relation_regularizer: HintOrType[Regularizer] = "LpRegularizer",
        relation_regularizer_kwargs: OptionalKwargs = dict(weight=3.72*10**-18, p=2),
        **kwargs,
    ) -> None:
        super().__init__(
            interaction=TransEInteraction,
            interaction_kwargs=dict(p=scoring_fct_norm),
            entity_representations_kwargs=dict(
                shape=embedding_dim,
                initializer=entity_initializer,
                constrainer=entity_constrainer,
                regularizer=entity_regularizer,
                regularizer_kwargs=entity_regularizer_kwargs,
            ),
            relation_representations_kwargs=dict(
                shape=embedding_dim,
                initializer=relation_initializer,
                constrainer=relation_constrainer,
                regularizer=relation_regularizer,
                regularizer_kwargs=relation_regularizer_kwargs,
            ),
            **kwargs,
        )

# model name
MODEL_NAME = "transE_ruffinelli_ht"

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
    model=TransE_separate_regularizers,
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
        embedding_dim=512,
        scoring_fct_norm=2
    ),
    # negative sampling
    negative_sampler="basic",
    negative_sampler_kwargs=dict(
        corruption_scheme=("head", "relation" "tail"),
    ),
    # loss
    loss="CrossEntropyLoss",
    # optimizer
    optimizer="Adagrad",
    optimizer_kwargs=dict(
        lr=0.04122
    ),
    lr_scheduler="ReduceLROnPlateau",
    lr_scheduler_kwargs=dict(
        patience=6
    ),
    # embedding normalization
    entity_constrainer=None,
    relation_constrainer=None,
    # embedding initialization
    entity_initializer=xavier_normal_,
    relation_initializer=xavier_normal_,
)

# save results
results.save_to_directory(RESULTS_DIR)
