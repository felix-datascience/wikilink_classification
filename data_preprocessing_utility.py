import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedGroupKFold


def create_pair_id(row):
    """
    Creates a columns with an ID for an entity pair, regardless of their position in the triple.
    This function is designed to be applied on the rows of a pandas dataframe with the apply function.
    """
    subject_id = row["subject"][28:]
    object_id = row["object"][28:]
    return "+".join(sorted([subject_id, object_id]))


def remove_entity_pairs(
        dataset_filepath,
        pairs_dataset_filepath,
        processed_dataset_filepath,
        dataset_filetype="csv",
        pairs_dataset_filetype="csv",
        chunksize=2000000
    ):
    """
    This function is used to remove entity pairs that appear in one dataset from another dataset.

    :param dataset_filepath: file path of the file where pairs are removed
    :type dataset_filepath: str
    :param pairs_dataset_filepath: file path of the file containing the pairs that are remove from the first dataset
    :type pairs_dataset_filepath: str
    :param processed_dataset_filepath: file path which is used to store the dataset with removed pairs
    :type processed_dataset_filepath: str
    :param dataset_filetype: file type, either "csv" or "ttl"
    :type dataset_filetype: str
    :param pairs_dataset_filetype: file type, either "csv" or "ttl"
    :type pairs_dataset_filetype: str
    :param chunksize: size of the chunks that are read when iterating over the files
    :type chunksize: int
    :return: None
    """

    # define and store file parsing arguments
    csv_file_parsing_args = {}
    ttl_file_parsing_args = {"sep": " ", "header": None, "names": ["subject", "predicate", "object", "."]}
    if dataset_filetype == "csv":
        dataset_file_parsing_args = csv_file_parsing_args
    elif dataset_filetype == "ttl":
        dataset_file_parsing_args = ttl_file_parsing_args
    else:
        print('File type can either be "csv" or "ttl"')
        return
    if pairs_dataset_filetype == "csv":
        pairs_dataset_file_parsing_args = csv_file_parsing_args
    elif pairs_dataset_filetype == "ttl":
        pairs_dataset_file_parsing_args = ttl_file_parsing_args
    else:
        print('File type can either be "csv" or "ttl"')
        return

    # read pairs dataset and store unique pair IDs
    entity_pairs = pd.DataFrame()
    for i, chunk in enumerate(pd.read_csv(pairs_dataset_filepath, chunksize=chunksize, **pairs_dataset_file_parsing_args)):
        print(f"read entity pairs dataset (chunk {i+1})...")
        chunk = chunk.apply(create_pair_id, axis=1)
        chunk = chunk.rename("pair_id")
        chunk = chunk.drop_duplicates(ignore_index=True)
        chunk = chunk.to_frame()
        chunk["drop_pair"] = 1
        entity_pairs = pd.concat([entity_pairs, chunk])

    # read dataset that is filtered and remove pairs that appear in the pairs dataset
    n_triples_before = 0
    n_triples_after = 0
    for i, chunk in enumerate(pd.read_csv(dataset_filepath, chunksize=chunksize, **dataset_file_parsing_args)):
        print(f"processing chunk {i+1}...")
        if dataset_filetype == "ttl":
            chunk = chunk.drop(columns=".")
            # remove "<" and ">"
            for col in chunk.columns:
                chunk[col] = chunk[col].str[1:-1]
        n_triples_before = n_triples_before + len(chunk)
        # remove entity pairs
        chunk["pair_id"] = chunk.apply(create_pair_id, axis=1)
        chunk = chunk.merge(entity_pairs, on="pair_id", how="left")
        chunk = chunk[chunk["drop_pair"] != 1]
        chunk = chunk.drop(columns=["pair_id", "drop_pair"])
        n_triples_after = n_triples_after + len(chunk)
        # write back to file
        chunk.to_csv(
            processed_dataset_filepath,
            index=False,
            header=True if i == 0 else False,
            mode="w" if i == 0 else "a"
        )

    # print statistics (triples before and after filtering)
    print("\nnumber of triples\nbefore filtering\tafter filtering")
    print(f"{n_triples_before}\t\t{n_triples_after} ({round(n_triples_after / n_triples_before, 3)})")


def filter_properties(
        properties_dataset_filepath,
        filtered_property_types_filepath,
        processed_dataset_filepath,
        properties_dataset_filetype="csv",
        chunksize=2000000
    ):
    """
    This function is used to filter properties in a datset. The properties that are filtered need to be stored in a separate file.

    :param properties_dataset_filepath: file path of the file containing properties that will be filtered
    :type properties_dataset_filepath: str
    :param filtered_property_types_filepath: file path of the file containing the subset of property types that are filtered
    :type filtered_property_types_filepath: str
    :param processed_dataset_filepath: file path which is used to store the filtered dataset
    :type processed_dataset_filepath: str
    :param properties_dataset_filetype: file type, either "csv" or "ttl"
    :type properties_dataset_filetype: str
    :param chunksize: size of the chunks that are read when iterating over the file
    :type chunksize: int
    :return: None
    """
    
    # read filtered property types
    filtered_property_types = pd.read_csv(filtered_property_types_filepath)

    # define and store file parsing arguments
    csv_file_parsing_args = {}
    ttl_file_parsing_args = {"sep": " ", "header": None, "names": ["subject", "predicate", "object", "."]}
    if properties_dataset_filetype == "csv":
        dataset_file_parsing_args = csv_file_parsing_args
    elif properties_dataset_filetype == "ttl":
        dataset_file_parsing_args = ttl_file_parsing_args
    else:
        print('File type can either be "csv" or "ttl"')
        return

    # read dataset that is filtered and remove property types that don't appear in the filtered property types dataset
    n_triples_before = 0
    n_triples_after = 0
    for i, chunk in enumerate(pd.read_csv(properties_dataset_filepath, chunksize=chunksize, **dataset_file_parsing_args)):
        print(f"processing chunk {i+1}...")
        if properties_dataset_filetype == "ttl":
            chunk = chunk.drop(columns=".")
            # remove "<" and ">"
            for col in chunk.columns:
                chunk[col] = chunk[col].str[1:-1]
        n_triples_before = n_triples_before + len(chunk)
        # remove entity pairs
        chunk = chunk.merge(filtered_property_types, left_on="predicate", right_on="filtered_property_types")
        chunk = chunk.drop(columns="filtered_property_types")
        n_triples_after = n_triples_after + len(chunk)
        # write back to file
        chunk.to_csv(
            processed_dataset_filepath,
            index=False,
            header=True if i == 0 else False,
            mode="w" if i == 0 else "a"
        )

    # print statistics (triples before and after filtering)
    print("\nnumber of triples\nbefore filtering\tafter filtering")
    print(f"{n_triples_before}\t\t{n_triples_after} ({round(n_triples_after / n_triples_before, 3)})")


def filter_entities(
        dataset_filepath,
        entities_dataset_filepath,
        processed_dataset_filepath,
        filter_subject_only=False,
        dataset_filetype="csv",
        entities_dataset_filetype="csv",
        chunksize=2000000
    ):
    """
    This function is used to filter one dataset for entities that appear in another datset.

    :param dataset_filepath: file path of the file that is filtered
    :type dataset_filepath: str
    :param entities_dataset_filepath: file path of the file containing the entities that will be filtered
    :type entities_dataset_filepath: str
    :param processed_dataset_filepath: file path which is used to store the filtered dataset
    :type processed_dataset_filepath: str
    :param filter_subject_only: if set to True, only the subjects are filtered, otherwise subjects and objects
    :type filter_subject_only: bool
    :param dataset_filetype: file type, either "csv" or "ttl"
    :type dataset_filetype: str
    :param entities_dataset_filetype: file type, either "csv" or "ttl"
    :type entities_dataset_filetype: str
    :param chunksize: size of the chunks that are read when iterating over the files
    :type chunksize: int
    :return: None
    """
    
    # define and store file parsing arguments
    csv_file_parsing_args = {}
    ttl_file_parsing_args = {"sep": " ", "header": None, "names": ["subject", "predicate", "object", "."]}
    if dataset_filetype == "csv":
        dataset_file_parsing_args = csv_file_parsing_args
    elif dataset_filetype == "ttl":
        dataset_file_parsing_args = ttl_file_parsing_args
    else:
        print('File type can either be "csv" or "ttl"')
        return
    if entities_dataset_filetype == "csv":
        entities_dataset_file_parsing_args = csv_file_parsing_args
    elif entities_dataset_filetype == "ttl":
        entities_dataset_file_parsing_args = ttl_file_parsing_args
    else:
        print('File type can either be "csv" or "ttl"')
        return

    # read dataset that contains entities that are filtered from the other dataset and store entities
    entities = np.array([])
    for i, chunk in enumerate(pd.read_csv(entities_dataset_filepath, chunksize=chunksize, **entities_dataset_file_parsing_args)):
        print(f"read entities dataset (chunk {i+1})...")
        entities = np.union1d(entities, np.union1d(chunk["subject"].unique(), chunk["object"].unique()))
    entities = pd.Series(entities, name="entity")

    # read dataset that is filtered and remove entities that don't appear in the entities dataset
    try:
        n_triples_before = 0
        n_triples_after = 0
        for i, chunk in enumerate(pd.read_csv(dataset_filepath, chunksize=chunksize, **dataset_file_parsing_args)):
            print(f"processing chunk {i+1}...")
            if dataset_filetype == "ttl":
                chunk = chunk.drop(columns=".")
                # remove "<" and ">"
                for col in chunk.columns:
                    chunk[col] = chunk[col].str[1:-1]
            n_triples_before = n_triples_before + len(chunk)

            # filter entities
            chunk = chunk.merge(entities, left_on="subject", right_on="entity")
            chunk = chunk.drop(columns="entity")
            if not filter_subject_only:
                chunk = chunk.merge(entities, left_on="object", right_on="entity")
                chunk = chunk.drop(columns="entity")
            n_triples_after = n_triples_after + len(chunk)

            # write back to file
            chunk.to_csv(
                processed_dataset_filepath,
                index=False,
                header=True if i == 0 else False,
                mode="w" if i == 0 else "a"
            )
    except pd.errors.ParserError:
        dataset_file_parsing_args = {"sep": ", "}
        n_triples_before = 0
        n_triples_after = 0
        for i, chunk in enumerate(pd.read_csv(dataset_filepath, chunksize=chunksize, **dataset_file_parsing_args)):
            print(f"processing chunk {i+1}...")
            # remove " characters
            for col in chunk.columns:
                chunk[col] = chunk[col].str[1:-1]
            n_triples_before = n_triples_before + len(chunk)

            # filter entities
            chunk = chunk.merge(entities, left_on="subject", right_on="entity")
            chunk = chunk.drop(columns="entity")
            if not filter_subject_only:
                chunk = chunk.merge(entities, left_on="object", right_on="entity")
                chunk = chunk.drop(columns="entity")
            n_triples_after = n_triples_after + len(chunk)

            # write back to file
            chunk.to_csv(
                processed_dataset_filepath,
                index=False,
                header=True if i == 0 else False,
                mode="w" if i == 0 else "a"
            )


    # print statistics (triples before and after filtering)
    print("\nnumber of triples\nbefore filtering\tafter filtering")
    print(f"{n_triples_before}\t\t{n_triples_after} ({round(n_triples_after / n_triples_before, 3)})")


def split_dataset(
        dataset_filepath,
        trainset_filepath,
        valset_filepath,
        testset_filepath,
        val_test_fraction=5,
        random_state=42
    ):
    """
    This function is used to split a dataset of triples into a training, validation and testing set.
    The split is performed in a way that entity pairs can only exist in one part of the split and
    the split is stratified by the properties. The function reads the whole dataset into memory so
    it does not work with files that are too large for that.

    :param dataset_filepath: path to the dataset that is split
    :type dataset_filepath: str
    :param trainset_filepath: path under which the training set is stored
    :type trainset_filepath: str
    :param valset_filepath: path under which the validation set is stored
    :type valset_filepath: str
    :param testset_filepath: path under which the testing set is stored
    :type testset_filepath: str
    :param val_test_fraction: determines validation and testing set size as 1 / val_test_fraction
    :type val_test_fraction: int
    :param random_state: random state for shuffling the dataset before splitting
    :type random_state: int
    :return: None
    """
    
    dataset = pd.read_csv(dataset_filepath)
    dataset["pair_id"] = dataset.apply(create_pair_id, axis=1)

    # generate indexes for splitting the dataset
    sgkf = StratifiedGroupKFold(n_splits=val_test_fraction, shuffle=True, random_state=random_state)
    splitter = sgkf.split(
        dataset[["subject", "object"]],
        dataset["predicate"],
        dataset["pair_id"]
    )
    _, val_idx = next(splitter)
    _, test_idx = next(splitter)
    train_idx = np.setdiff1d(dataset.index, np.concatenate([test_idx, val_idx]))

    # split the dataset using the indexes
    train_df = dataset.iloc[train_idx]
    val_df = dataset.iloc[val_idx]
    test_df = dataset.iloc[test_idx]
    train_df = train_df.drop(columns="pair_id")
    val_df = val_df.drop(columns="pair_id")
    test_df = test_df.drop(columns="pair_id")

    # save sets into files
    train_df.to_csv(trainset_filepath, index=False)
    val_df.to_csv(valset_filepath, index=False)
    test_df.to_csv(testset_filepath, index=False)

    # print out statistics
    n_props_train = len(train_df["predicate"].unique())
    n_props_val = len(val_df["predicate"].unique())
    n_props_test = len(test_df["predicate"].unique())
    print("\nnumber of triples\ntraining set\tvalidation set\ttesting set")
    print(f"{len(train_df)}\t\t{len(val_df)}\t\t{len(test_df)}")
    print("\nnumber of unique properties\ntraining set\tvalidation set\ttesting set")
    print(f"{n_props_train}\t\t{n_props_val}\t\t{n_props_test}")


def concat_files(filepaths, filetypes, processed_dataset_filepath, chunksize=2000000):
    """
    This function is used to concatenate multiple files containing triples into one TSV file that can be used with pykeen.
    The function can handle datasets that don't fit into memory.

    :param filepaths: list of file paths (strings)
    :type filepaths: list
    :param filetypes: list of filetypes (strings, either "csv" or "ttl")
    :type filetypes: list
    :param processed_dataset_filepath: file path under which the final concatenated files are stored
    :type processed_dataset_filepath: str
    :param chunksize: size of the chunks that are read when iterating over the files
    :type chunksize: int
    :return: None
    """

    # iterate over filepaths and filetypes
    for i, (filepath, filetype) in enumerate(zip(filepaths, filetypes)):
        print(f"reading file {i+1}")
        # define and store file parsing arguments
        csv_file_parsing_args = {}
        ttl_file_parsing_args = {"sep": " ", "header": None, "names": ["subject", "predicate", "object", "."]}
        if filetype == "csv":
            dataset_file_parsing_args = csv_file_parsing_args
        elif filetype == "ttl":
            dataset_file_parsing_args = ttl_file_parsing_args
        else:
            print('File type can either be "csv" or "ttl"')
            return

        # iterate over file and write it to the file containing the concatenated files
        for j, chunk in enumerate(pd.read_csv(filepath, chunksize=chunksize, **dataset_file_parsing_args)):
            print(f"\nchunk {j+1}...")
            if filetype == "ttl":
                chunk = chunk.drop(columns=".")
                # remove "<" and ">"
                for col in chunk.columns:
                    chunk[col] = chunk[col].str[1:-1]
            chunk.to_csv(
                processed_dataset_filepath,
                sep="\t",
                index=False,
                header=False,
                mode="w" if i == 0 and j == 0 else "a"
            )