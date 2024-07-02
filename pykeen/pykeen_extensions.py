from class_resolver import Hint, HintOrType, OptionalKwargs
import torch
from torch.nn import functional
from torch.nn.init import uniform_
from pykeen.sampling import NegativeSampler, BasicNegativeSampler
from pykeen.models.nbase import ERModel
from pykeen.nn import TransEInteraction, ComplExInteraction
from pykeen.nn.init import xavier_uniform_, xavier_uniform_norm_
from pykeen.regularizers import Regularizer
from pykeen.typing import Constrainer, Initializer
from typing import Optional


class ComplexNegativeSampler(NegativeSampler):
    """
    Implementation of a negative sampler that allows sampling subject, predicate and object of a triple
    and determining the amount of samples per subject, predicate and object individually.
    When negative predicate samples are included, the generated samples are filtered using pykeen's
    default filter (because the low number of property types leads to a higher chance of introducing
    false negatives).
    """

    def __init__(
        self,
        *,
        n_subject_samples=None,
        n_predicate_samples=None,
        n_object_samples=None,
        **kwargs
    ) -> None:
        """
        :param n_subject_samples:
            number of negative samples per subject
        :param n_predicate_samples:
            number of negative samples per predicate
        :param n_object_samples:
            number of negative samples per object
        :param kwargs:
            Additional keyword based arguments passed to :class:`pykeen.sampling.NegativeSampler`.
        """
        super().__init__(**kwargs)
        if not n_subject_samples == None:
            self.subject_sampler = BasicNegativeSampler(corruption_scheme=["head"], num_negs_per_pos=n_subject_samples, **kwargs)
        else:
            self.subject_sampler = None
        if not n_predicate_samples == None:
            self.predicate_sampler = BasicNegativeSampler(corruption_scheme=["relation"], num_negs_per_pos=n_predicate_samples, filtered=True, **kwargs)
        else:
            self.predicate_sampler = None
        if not n_object_samples == None:
            self.object_sampler = BasicNegativeSampler(corruption_scheme=["tail"], num_negs_per_pos=n_object_samples, **kwargs)
        else:
            self.object_sampler = None

    def corrupt_batch(self, positive_batch: torch.LongTensor) -> torch.LongTensor:  
        samples = []
        if not self.subject_sampler == None:
            samples.append(self.subject_sampler.corrupt_batch(positive_batch))
        if not self.predicate_sampler == None:
            samples.append(self.predicate_sampler.corrupt_batch(positive_batch))
        if not self.object_sampler == None:
            samples.append(self.object_sampler.corrupt_batch(positive_batch))
        return torch.cat(samples, dim=1)


class TransE_separate_regularizers(ERModel):
    """
    TransE model with separate regularizers for entity and relation embeddings.
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


class ComplEx_dropout_and_separate_regularizers(ERModel):
    """
    ComplEx model with dropout and separate regularizers for entity and relation embeddings.
    """
    def __init__(
        self,
        *,
        embedding_dim: int = 200,
        entity_initializer: Hint[Initializer] = uniform_,
        entity_initializer_kwargs: OptionalKwargs = dict(a=-0.85, b=0.85),
        relation_initializer: Hint[Initializer] = uniform_,
        relation_initializer_kwargs: OptionalKwargs = dict(a=-0.85, b=0.85),
        entity_regularizer: HintOrType[Regularizer] = "LpRegularizer",
        entity_regularizer_kwargs: OptionalKwargs = dict(weight=4.52*10**-6, p=3),
        relation_regularizer: HintOrType[Regularizer] = "LpRegularizer",
        relation_regularizer_kwargs: OptionalKwargs = dict(weight=4.19*10**-10, p=3),
        entity_dropout: Optional[float] = 0.36,
        relation_dropout: Optional[float] = 0.31,
        **kwargs,
    ) -> None:
        super().__init__(
            interaction=ComplExInteraction,
            entity_representations_kwargs=dict(
                shape=embedding_dim,
                initializer=entity_initializer,
                initializer_kwargs=entity_initializer_kwargs,
                dtype=torch.cfloat,
                regularizer=entity_regularizer,
                regularizer_kwargs=entity_regularizer_kwargs,
                dropout=entity_dropout,
            ),
            relation_representations_kwargs=dict(
                shape=embedding_dim,
                initializer=relation_initializer,
                initializer_kwargs=relation_initializer_kwargs,
                dtype=torch.cfloat,
                regularizer=relation_regularizer,
                regularizer_kwargs=relation_regularizer_kwargs,
                dropout=relation_dropout,
            ),
            **kwargs,
        )