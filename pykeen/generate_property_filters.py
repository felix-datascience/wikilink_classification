import pandas as pd
from post_processing_utility import domain_range_filter_triples

VAL_PATH = "../data/processed_data/val.tsv"
TEST_PATH = "../data/processed_data/test.tsv"
FILTERED_PROPERTY_TYPES_FILEPATH = "../data/processed_data/filtered_property_types.csv"
ONTOLOGY_FILEPATH = "../data/raw_data/ontology--DEV_type=parsed_sorted.nt"
TYPES_FILEPATH = "../data/raw_data/instance-types_inference=transitive_lang=en.ttl"

VAL_PROPS_FILTER_STRICT_FILEPATH = "../data/processed_data/val_props_filter_strict.csv"
VAL_PROPS_FILTER_FLEXIBLE_FILEPATH = "../data/processed_data/val_props_filter_flexible.csv"
TEST_PROPS_FILTER_STRICT_FILEPATH = "../data/processed_data/test_props_filter_strict.csv"
TEST_PROPS_FILTER_FLEXIBLE_FILEPATH = "../data/processed_data/test_props_filter_flexible.csv"

# load filtered property types
filtered_prop_types = pd.read_csv(FILTERED_PROPERTY_TYPES_FILEPATH)

# load ontology
ontology = pd.read_csv(ONTOLOGY_FILEPATH, sep="> ", header=None, names=["subject", "predicate", "object", "."])
ontology = ontology.drop(columns=".")
# remove labels
ontology = ontology[ontology["predicate"] != "<http://www.w3.org/2000/01/rdf-schema#label"]
# remove leading "<" characters
for col in ontology.columns:
    ontology[col] = ontology[col].str[1:]

# load triples of validation and testing set
val_df = pd.read_csv(VAL_PATH, sep="\t", names=["subject", "predicate", "object"])
test_df = pd.read_csv(TEST_PATH, sep="\t", names=["subject", "predicate", "object"])

# generate property type filters
val_properties_filter_strict = domain_range_filter_triples(val_df, TYPES_FILEPATH, ontology, filtered_prop_types, handle_untyped_entities="strict")
val_properties_filter_flexible = domain_range_filter_triples(val_df, TYPES_FILEPATH, ontology, filtered_prop_types, handle_untyped_entities="flexible")
test_properties_filter_strict = domain_range_filter_triples(test_df, TYPES_FILEPATH, ontology, filtered_prop_types, handle_untyped_entities="strict")
test_properties_filter_flexible = domain_range_filter_triples(test_df, TYPES_FILEPATH, ontology, filtered_prop_types, handle_untyped_entities="flexible")

# save files
val_properties_filter_strict.to_csv(VAL_PROPS_FILTER_STRICT_FILEPATH, index=False)
val_properties_filter_flexible.to_csv(VAL_PROPS_FILTER_FLEXIBLE_FILEPATH, index=False)
test_properties_filter_strict.to_csv(TEST_PROPS_FILTER_STRICT_FILEPATH, index=False)
test_properties_filter_flexible.to_csv(TEST_PROPS_FILTER_FLEXIBLE_FILEPATH, index=False)