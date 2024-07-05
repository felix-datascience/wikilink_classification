import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score


def get_expanded_subclass_relationships(ontology_df, depth_limit=999, blacklist=[]):
    """
    This function recursively expands the subclass relationships in the ontology.
    
    E.g. the ontology contains the triples:
    - Academic, subClassOf, Person
    - Person, subClassOf, Animal
    The function would add the triple:
    - Academic, subClassOf, Animal
    
    This procedure is repeated until no new subclass relationships can be added or for the specied number of recusions
    (determined with depth_limit parameter).

    :param ontology_df: dataframe containing ontology triples
    :type ontology_df: pd.DataFrame
    :param depth_limit: limits of the number of steps in the hierarchy that are followed to extend the subclass relationships
    :type depth_limit: int
    :param blacklist: any subclass-superclass pair with this type as superclass will be removed (can be used to remove too generic types)
    :type_blacklist: list
    :return: dataframe containing pairs of subclass-superclass pairs
    """
    subclasses = ontology_df[ontology_df["predicate"] == "http://www.w3.org/2000/01/rdf-schema#subClassOf"]
    expanded_subclasses = subclasses.copy()
    expanded_subclasses = expanded_subclasses.drop(columns="predicate")
    expanded_subclasses = expanded_subclasses.rename(columns={"subject": "superclass0", "object": "superclass1"})
    
    # create chains of subclass relationships
    expanded_classes = True
    superclass_idx = 1
    while expanded_classes == True and superclass_idx < depth_limit:
        expanded_subclasses = expanded_subclasses.merge(subclasses, left_on=f"superclass{superclass_idx}", right_on="subject", how="left")
        expanded_subclasses = expanded_subclasses.drop(columns=["predicate", "subject"])
        superclass_idx += 1
        expanded_subclasses = expanded_subclasses.rename(columns={"object": f"superclass{superclass_idx}"})
        if (~expanded_subclasses[f"superclass{superclass_idx}"].isna()).sum() > 0:
            expanded_classes = True
        else:
            expanded_classes = False
        
    # create every possible pair of subclass-class relations
    expanded_subclass_pairs = pd.DataFrame()
    for i in range(superclass_idx):
        for j in range(i+1, superclass_idx+1):
            subclass_col = f"superclass{i}"
            superclass_col = f"superclass{j}"
            pairs = expanded_subclasses[[subclass_col, superclass_col]]
            pairs = pairs.rename(columns={subclass_col: "subclass", superclass_col: "superclass"})
            pairs = pairs.dropna()
            expanded_subclass_pairs = pd.concat([expanded_subclass_pairs, pairs], axis=0)
            expanded_subclass_pairs = expanded_subclass_pairs.drop_duplicates()
            expanded_subclass_pairs = expanded_subclass_pairs.reset_index(drop=True)

    # remove blacklist types
    expanded_subclass_pairs = expanded_subclass_pairs[~expanded_subclass_pairs["superclass"].isin(blacklist)]

    return expanded_subclass_pairs


def extract_domain_range_filter(
    ontology_df,
    filtered_property_types_df,
    upwards_extension_depth_limit=999,
    upwards_extension_blacklist=[]
):
    """
    Creates two matrices that can be used for filtering relevant properties for subject and object entity type.
    The filter is based on the domain and range restrictions in the ontology. The tolerated types (of the range
    and domain) are first expanded downwards, meaning all subclasses of the type that is listed in the domain
    or range restriction are tolerated as well. In an optional second step the tolerated types are expanded
    upwards for a specified number of steps in the hierarchy (upwards_extension_depth_limit). To avoid this, set
    the parameter to 0. In this upwards extension step, a blacklist can be provided to prevent too generic types
    to be tolerated (e.g. owl:Thing).

    :param ontology_df: dataframe containing the ontology triples
    :type ontology_df: pd.DataFrame
    :param filtered_property_types_df: dataframe containing the list of filtered property types
    :type filtered_property_types_df: pd.DataFrame
    :param upwards_extension_depth_limit: limits of the number of steps in the hierarchy that are followed upwards to extend the subclass relationships
    :type upwards_extension_depth_limit: int
    :param upwards_extension_blacklist: can be used to prevent too generic types from being introduced in the upwards expansion step
    :type upwards_extension_blacklist: list
    :return: two pandas dataframes containing the domain / range filter matrices
    """
    domain_range = ontology_df[
        (ontology_df["predicate"] == "http://www.w3.org/2000/01/rdf-schema#domain")
        | (ontology_df["predicate"] == "http://www.w3.org/2000/01/rdf-schema#range")
    ]
    # filter property types
    # (only keep range and domain restrictions for the subset of filtered property types)
    domain_range = domain_range.merge(filtered_property_types_df, left_on="subject", right_on="filtered_property_types")
    domain_range = domain_range.drop(columns="filtered_property_types")
    # expand domain and range restrictions downwards with subclass relationships
    expanded_subclass_relationships = get_expanded_subclass_relationships(ontology_df)
    domain_range_downwards_expanded = domain_range.merge(expanded_subclass_relationships, left_on="object", right_on="superclass")
    domain_range_downwards_expanded = domain_range_downwards_expanded.drop(columns=["object", "superclass"])
    domain_range_downwards_expanded = domain_range_downwards_expanded.rename(columns={"subclass": "object"})
    domain_range = pd.concat([domain_range, domain_range_downwards_expanded])
    domain_range = domain_range.drop_duplicates()
    # expand domain and range restrictions upwards with subclass relationships
    if upwards_extension_depth_limit > 0:
        expanded_subclass_relationships = get_expanded_subclass_relationships(
            ontology_df,
            depth_limit=upwards_extension_depth_limit,
            blacklist=upwards_extension_blacklist
        )
        domain_range_upwards_expanded = domain_range.merge(expanded_subclass_relationships, left_on="object", right_on="subclass")
        domain_range_upwards_expanded = domain_range_upwards_expanded.drop(columns=["object", "subclass"])
        domain_range_upwards_expanded = domain_range_upwards_expanded.rename(columns={"superclass": "object"})
        domain_range = pd.concat([domain_range, domain_range_upwards_expanded])
        domain_range = domain_range.drop_duplicates()
    # create matrix for filtering relevant properties for each subject entity type
    domain_filter = domain_range[domain_range["predicate"] == "http://www.w3.org/2000/01/rdf-schema#domain"]
    domain_filter = domain_filter.drop(columns="predicate")
    domain_filter["dummy"] = 1
    domain_filter = domain_filter.rename(columns={"subject": "property_type", "object": "entity_type"})
    domain_filter = domain_filter.pivot(index="entity_type", columns="property_type", values="dummy")
    domain_filter = domain_filter.fillna(0)
    domain_filter = domain_filter.astype(int)
    domain_filter = domain_filter.reset_index()
    # create matrix for filtering relevant properties for each object entity type
    range_filter = domain_range[domain_range["predicate"] == "http://www.w3.org/2000/01/rdf-schema#range"]
    range_filter = range_filter.drop(columns="predicate")
    range_filter["dummy"] = 1
    range_filter = range_filter.rename(columns={"subject": "property_type", "object": "entity_type"})
    range_filter = range_filter.pivot(index="entity_type", columns="property_type", values="dummy")
    range_filter = range_filter.fillna(0)
    range_filter = range_filter.astype(int)
    range_filter = range_filter.reset_index()
    
    return domain_filter, range_filter


def read_entity_types(triples_df, types_filepath):
    """
    Reads the file of type triples and filters entity types for all entities that are part of the
    provided dataset (triples_df).
    
    :param triples_df: dataframe of triples containing the entities whose types are returned
    :type triples_df: pd.DataFrame
    :param types_filepath: file path of the types dataset
    :type types_filepath: str
    :return: dataframe containing pairs of entity and entity type
    """
    entities = np.union1d(triples_df["subject"], triples_df["object"])
    entities = pd.Series(entities, name="entity")
    entity_types = pd.DataFrame()
    for i, chunk in enumerate(pd.read_csv(types_filepath, sep=" ", header=None, names=["subject", "predicate", "object", "."], chunksize=200000)):
        chunk = chunk.drop(columns=".")
        # remove "<" and ">"
        for col in chunk.columns:
            chunk[col] = chunk[col].str[1:-1]
        chunk = chunk.drop(columns="predicate")
        chunk = chunk.rename(columns={"subject": "entity", "object": "entity_type"})
        chunk = chunk.merge(entities, on="entity")
        entity_types = entity_types._append(chunk, ignore_index=True)
    
    return entity_types


def domain_range_filter_triples(
        triples_df,
        specific_types_filepath,
        ontology_df,
        filtered_property_types_df,
        handle_untyped_entities="strict",
        upwards_extension_depth_limit=999,
        upwards_extension_blacklist=[]
    ):
    """
    Creates a matrix indicating which properties are relevant to a pair of entities (depending on their types).
    The filtering is based on the extract_domain_range_filter function. Additionally, the handling of untyped
    entities can be controlled to either allow or prevent entities without any types to be considered in the
    range / domain of a restricted property.

    :param triples_df: triples for whose entity pairs the subsets of relevant property types are returned
    :type triples_df: pd.DataFrame
    :param specific_types_filepath: file path of the specific types dataset
    :type specific_types_filepath: str
    :param ontology_df: dataframe containing ontology triples
    :type ontology_df: pd.DataFrame
    :param filtered_property_types_df: dataframe containing list of filtered property types
    :type filtered_property_types_df: pd.DataFrame
    :param handle_untyped_entities: if set to "strict" entities without types can only be in range/domain of properties without restrictions,
        if set to "flexible" they can be in range/domain of any property
    :type handle_untyped_entities: str
    :param upwards_extension_depth_limit: limits of the number of steps in the hierarchy that are followed upwards to extend the subclass relationships
    :type upwards_extension_depth_limit: int
    :param upwards_extension_blacklist: can be used to prevent too generic types from being introduced in the upwards expansion step
    :type upwards_extension_blacklist: list
    :return: dataframe annotating which properties (columns) are relevant for a pair of entities (rows)
    """
    if handle_untyped_entities == "strict":
        untyped_entities_fill_value = 0
    elif handle_untyped_entities == "flexible":
        untyped_entities_fill_value = 1
    else:
        print('ERROR: handle_untyped_enities argument can only be "strict" or "flexible"')
        return None
    
    # read entity types
    entity_types = read_entity_types(triples_df, specific_types_filepath)
    
    # extract domain and range restrictions from ontology
    domain_filter, range_filter = extract_domain_range_filter(
        ontology_df,
        filtered_property_types_df,
        upwards_extension_depth_limit=upwards_extension_depth_limit,
        upwards_extension_blacklist=upwards_extension_blacklist
    )
    
    # add entity types that don't appear in the domain restrictions and set their values to 0
    remaining_entity_types = pd.DataFrame(columns=domain_filter.columns)
    remaining_entity_types["entity_type"] = np.setdiff1d(entity_types["entity_type"].unique(), domain_filter["entity_type"])
    remaining_entity_types = remaining_entity_types.fillna(0)
    domain_filter = domain_filter._append(remaining_entity_types, ignore_index=True)
    # add entity types that don't appear in the range restrictions and set their values to 0
    remaining_entity_types = pd.DataFrame(columns=range_filter.columns)
    remaining_entity_types["entity_type"] = np.setdiff1d(entity_types["entity_type"].unique(), range_filter["entity_type"])
    remaining_entity_types = remaining_entity_types.fillna(0)
    range_filter = range_filter._append(remaining_entity_types, ignore_index=True)
    
    # add properties without domain restricions and set to 1 for every entity type
    no_domain_restrictions_props = np.setdiff1d(
        filtered_property_types_df["filtered_property_types"].values,
        np.setdiff1d(domain_filter.columns, ["entity_type"])
    )
    no_domain_restrictions_props = pd.DataFrame(index=domain_filter.index, columns=no_domain_restrictions_props)
    no_domain_restrictions_props = no_domain_restrictions_props.fillna(1)
    domain_filter = pd.concat([domain_filter, no_domain_restrictions_props], axis=1)
    # add properties without range restricions and set to 1 for every entity type
    no_range_restrictions_props = np.setdiff1d(
        filtered_property_types_df["filtered_property_types"].values,
        np.setdiff1d(range_filter.columns, ["entity_type"])
    )
    no_range_restrictions_props = pd.DataFrame(index=range_filter.index, columns=no_range_restrictions_props)
    no_range_restrictions_props = no_range_restrictions_props.fillna(1)
    range_filter = pd.concat([range_filter, no_range_restrictions_props], axis=1)

    # merge with entity types and set possible property types to 1 if entity has at least one of the required entity types
    entities_domain_filter = entity_types.merge(domain_filter, on="entity_type")
    entities_domain_filter = entities_domain_filter.drop(columns="entity_type")
    entities_domain_filter = entities_domain_filter.groupby("entity").max()
    entities_domain_filter = entities_domain_filter.reset_index()
    entities_range_filter = entity_types.merge(range_filter, on="entity_type")
    entities_range_filter = entities_range_filter.drop(columns="entity_type")
    entities_range_filter = entities_range_filter.groupby("entity").max()
    entities_range_filter = entities_range_filter.reset_index()

    # combine subject and object restrictions for each triple
    subject_restrictions = triples_df["subject"].rename("entity").to_frame()
    subject_restrictions = subject_restrictions.merge(entities_domain_filter, on="entity", how="left")
    object_restrictions = triples_df["object"].rename("entity").to_frame()
    object_restrictions = object_restrictions.merge(entities_range_filter, on="entity", how="left")
    # fill rows of entities without types
    subject_restrictions[no_domain_restrictions_props.columns] = subject_restrictions[no_domain_restrictions_props.columns].fillna(1)
    object_restrictions[no_range_restrictions_props.columns] = object_restrictions[no_range_restrictions_props.columns].fillna(1)
    subject_restrictions = subject_restrictions.fillna(untyped_entities_fill_value)
    object_restrictions = object_restrictions.fillna(untyped_entities_fill_value)
    triple_restrictions = subject_restrictions.add(object_restrictions)
    # set property types to 1 if the range and domain restrictions are fullfilled, otherwise set to 0
    prop_cols = np.setdiff1d(triple_restrictions.columns, ["entity"])
    triple_restrictions[prop_cols] = triple_restrictions[prop_cols] == 2
    triple_restrictions[prop_cols] = triple_restrictions[prop_cols].astype(int)
    triple_restrictions = pd.concat([
        triples_df[["subject", "object"]],
        triple_restrictions[np.setdiff1d(triple_restrictions.columns, ["entity"])]
    ], axis=1)

    # drop duplicated rows
    triple_restrictions = triple_restrictions.drop_duplicates()
    # sort columns
    cols = np.setdiff1d(triple_restrictions.columns, ["subject", "object"])
    cols.sort()
    cols = np.insert(cols, 0, "subject")
    cols = np.insert(cols, 1, "object")
    triple_restrictions = triple_restrictions.reindex(cols, axis=1)
    # sort rows
    triple_restrictions = triple_restrictions.sort_values(["subject", "object"])
    triple_restrictions = triple_restrictions.reset_index(drop=True)

    return triple_restrictions


def evaluate_filter(ground_truth, filter):
    """
    Returns a pandas dataframe containing accuracy, precision and recall of a domain and range filter
    for each property type and the mean of all property types (equally weighted).

    :param ground_truth: ground truth data in matrix form
    :type ground_truth: pd.DataFrame
    :param filter: filter in the same format as ground_truth
    :type filter: pd.DataFrame
    :return: pandas dataframe with 
    """
    props = np.setdiff1d(ground_truth.columns, ["subject", "object"])
    scores = pd.DataFrame(index=props, columns=["accuracy", "precision", "recall"])
    for prop in props:
        scores.loc[prop, "accuracy"] = accuracy_score(ground_truth[prop], filter[prop])
        scores.loc[prop, "precision"] = precision_score(ground_truth[prop], filter[prop])
        scores.loc[prop, "recall"] = recall_score(ground_truth[prop], filter[prop])
    scores = scores._append(scores.mean().rename("mean"))
    
    return scores