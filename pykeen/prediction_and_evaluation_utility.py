import pandas as pd
import numpy as np
from pykeen.predict import predict_target
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import optuna


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
    scores = scores.reindex(cols, axis=1)

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
    true_props = true_props.reindex(cols, axis=1)
    # sort rows
    true_props = true_props.sort_values(["subject", "object"])

    return true_props


def max_acc_threshold(scores, labels):
    """
    This function finds a threshold for classifying triples, according to their score.
    The threshold with the highest accuracy is picked. In case of ties the lowest score is used.

    :param scores: list or array containing the scores for multiple triples, all with the same property type
    :type scores: list
    :param labels: list or array containing ground truth binary labels
    :type labels: list
    :return: the optimal threshold for this data (float)
    """
    scores_labels = pd.DataFrame({"score": scores, "label": labels})
    scores_labels = scores_labels.sort_values("score").reset_index(drop=True)
    # iterate over the sorted_values and determine accuracy for this threshold
    # for predicting a positive label the score needs to surpass the score of this row
    # start below first positive triple
    if len(scores_labels[scores_labels["label"] == 1]) != 0:
        first_pos_idx = scores_labels[scores_labels["label"] == 1].iloc[0].name
        acc_vals = [0 for i in range(first_pos_idx-1)]
        for i in range(first_pos_idx-1, scores_labels.index.max()+1):
            y_pred = np.concatenate((np.repeat(0, i+1), np.repeat(1, len(scores_labels) - (i+1))))
            acc = accuracy_score(scores_labels["label"], y_pred)
            acc_vals.append(acc)
        scores_labels["acc"] = acc_vals
        # get threshold with best accuracy
        # (select lowest value in case of ties)
        max_acc = scores_labels["acc"].max()
        threshold = scores_labels[scores_labels["acc"] == max_acc]["score"].min()
    else:
        threshold = np.nan
    return threshold


def max_acc_threshold_optuna(scores, labels, n_trials=100):
    """
    Function for optimizing the threshold with optuna. This function can have a significantly lower runtime.
    Instead of trying out any possible threshold, like in the max_acc_threshold function, optuna is used to
    calculate the accuracy for a subset of thresholds.

    :param scores: list or array containing the scores for multiple triples, all with the same property type
    :type scores: list
    :param labels: list or array containing ground truth binary labels
    :type labels: list
    :param n_trials: number of trials in the optuna study (number of sampled thresholds)
    :type n_trials: int
    :return: the optimal threshold for this data (float)
    """
    scores_labels = pd.DataFrame({"score": scores, "label": labels})
    scores_labels = scores_labels.sort_values("score").reset_index(drop=True)
    min_threshold, max_threshold = scores_labels["score"].agg(["min", "max"])
    
    def objective(trial):
        threshold = trial.suggest_float('threshold', min_threshold, max_threshold)
        predictions = (scores_labels["score"] >= threshold).astype(int)
        accuracy = accuracy_score(scores_labels["label"], predictions)
        return accuracy
    
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=n_trials, n_jobs=-1)
    
    return study.best_params["threshold"]


def find_thresholds(scores_df, labels_df, use_optuna=False, n_trials=None):
    """
    This function iterates over all property types that are contained in the ground truth dataset and
    finds the optimal threshold for all property types. This function makes use of the max_acc_threshold
    function and thus finds thresholds which maximize the accuracy.

    :param scores_df: dataframe containing scores for multiple entity pairs (rows) and property types (columns)
    :type scores_df: pd.DataFrame
    :param labels_df: dataframe containing ground truth labels for multiple entity pairs (rows) and property types (columns)
    :type labels_df: pd.DataFrame
    :param use_optuna: if set to True, use optuna for optimizing with sampled thresholds, if set to False all thresholds are tested to find the best
    :type use_optuna: bool
    :param n_trials: number of trials in the optuna study (number of sampled thresholds)
    :type n_trials: int
    :return: dataframe containing the optimized thresholds for all property types that are available in the ground truth dataset
    """
    thresholds = {}
    # iterate over all properties contained in labels_df and get thresholds for each property
    for col in np.setdiff1d(labels_df.columns, ["subject", "object"]):
        scores, labels = scores_df[col], labels_df[col]
        if use_optuna == True:
            thresholds[col] = max_acc_threshold_optuna(scores, labels, n_trials=n_trials)
        else:
            thresholds[col] = max_acc_threshold(scores, labels)
    thresholds_df = pd.DataFrame.from_dict(thresholds, orient="index")
    thresholds_df = thresholds_df.reset_index()
    thresholds_df = thresholds_df.rename(columns={"index": "property", 0: "threshold"})
    return thresholds_df


def classify_triples(scores_df, thresholds_df):
    """
    This function applies the thresholds to the scores to predict binary labels.

    :param scores_df: dataframe containing scores for multiple entity pairs (rows) and property types (columns)
    :type scores_df: pd.DataFrame
    :param thresholds_df: dataframe containing thresholds for all property types that need to be included in the predictions
    :type thresholds_df: pd.DataFrame
    :return: dataframe containing the predictions in the same format as the ground truth dataframe
    """
    predictions = {"subject": scores_df["subject"], "object": scores_df["object"]}
    
    for prop in np.setdiff1d(scores_df.columns, ["subject", "object"]):
        if not prop in thresholds_df["property"].values:
            print(f"WARNING: threshold for {prop} not available")
            continue
        threshold = thresholds_df[thresholds_df["property"] == prop]["threshold"].iloc[0]
        if threshold == np.nan:
            prop_predictions = np.repeat(np.nan, len(scores_df))
        else:
            # predict triple as authentic if its score surpasses the threshold
            prop_predictions = (scores_df[prop] > threshold).astype(int)
        predictions[prop] = prop_predictions
    predictions = pd.DataFrame(predictions)
    
    return predictions


def evaluate_triple_classification(ground_truth_df, predictions_df):
    """
    This function returns per property type evaluation measures for predicted triple authenticities.
    The evaluation metrics are accuracy, precision, recall and f1-score.

    :param ground_truth_df: dataframe containing ground truth labels for multiple entity pairs (rows) and property types (columns)
    :type ground_truth_df: pd.DataFrame
    :param predictions_df: dataframe containing predicted labels for multiple entity pairs (rows) and property types (columns)
    :type predictions_df: pd.DataFrame
    :return: dataframe containing multiple evaluation measures for each property type
    """
    accuracy = {}
    precision = {}
    recall = {}
    f1 = {}
    # iterate over all properties contained in labels_df and get thresholds for each property
    for col in np.setdiff1d(ground_truth_df.columns, ["subject", "object"]):
        accuracy[col] = accuracy_score(ground_truth_df[col], predictions_df[col])
        precision[col] = precision_score(ground_truth_df[col], predictions_df[col])
        recall[col] = recall_score(ground_truth_df[col], predictions_df[col])
        f1[col] = f1_score(ground_truth_df[col], predictions_df[col])
    evaluation = pd.concat((
        pd.Series(accuracy, name="accuracy"),
        pd.Series(precision, name="precision"),
        pd.Series(recall, name="recall"),
        pd.Series(f1, name="f1")
    ), axis=1)
    evaluation = evaluation.reset_index()
    evaluation = evaluation.rename(columns={"index": "property"})
    
    return evaluation