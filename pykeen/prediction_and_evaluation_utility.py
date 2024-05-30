import pandas as pd
import numpy as np
from pykeen.predict import predict_target


def score_properties(entity_pairs, model, triples_factory, relation_to_id_dict):
    """
    This function computes scores of all properties for all suplied entity pairs.

    :param entity_pairs: list containing tuples of entity pairs
    :type entity_pairs: list
    :param model: model that is used to generate scores
    :type model: pykeen model
    :param triples_factory: triples factory that was used to train the model
    :type triples_factory: pykeen triples factory
    :param relation_to_id_dict: dictionary containing mappings of relation IDs to names
    :type relation_to_id_dict: dict
    :return: pandas dataframe containing the subject-object pair and scores for all property types
    """
    # initiate empty dataframe for storing scores
    scores = pd.DataFrame()
    # iterate over provided subject-object pairs and predict scores for all properties
    for subject, object in entity_pairs:
        pred = predict_target(
            model=model,
            head=subject,
            tail=object,
            triples_factory=triples_factory
        )
        pred = pred.df
        pred = pred["score"]
        pred = pred._append(pd.Series({"subject": subject, "object": object}))
        scores = scores._append(pred, ignore_index=True)
    
    # replace property IDs with names
    scores = scores.rename(columns={val: key for key, val in relation_to_id_dict.items()})
    # sort columns
    cols = np.setdiff1d(scores.columns.array, ["subject", "object"])
    cols.sort()
    cols = np.insert(cols, 0, "subject")
    cols = np.insert(cols, 1, "object")

    return scores


def true_properties_matrix(filepath):
    """
    This funtion generates a pandas dataframe containing a row for each entity pair and a column for each property type in the provided dataset.
    If an entity pair is linked with a property the corresponding field contains a 1 otherwise a 0.

    :param filepath: file path to a TSV file containing triples that are used to generate the matrix
    :type filepath: str
    :return: pandas dataframe containing property occurences
    """
    true_props = pd.read_csv(filepath, sep="\t", names=["subject", "predicate", "object"])
    true_props["dummy"] = 1
    true_props = true_props.pivot(index=["subject", "object"], columns="predicate", values="dummy")
    true_props = true_props.fillna(0)
    true_props = true_props.reset_index()
    # convert to integers
    prop_cols = np.setdiff1d(true_props.columns.array, ["subject", "object"])
    true_props[prop_cols] = true_props[prop_cols].astype(int)
    # sort columns
    cols = np.setdiff1d(true_props.columns.array, ["subject", "object"])
    cols.sort()
    cols = np.insert(cols, 0, "subject")
    cols = np.insert(cols, 1, "object")
    # sort rows
    true_props = true_props.sort_values(["subject", "object"])

    return true_props