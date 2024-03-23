# Create directory in which raw data is stored and navigate into it
mkdir raw_data
cd raw_data

# Download data
# wikilinks (en, 2022-12-01)
curl -O https://databus.dbpedia.org/dbpedia/generic/wikilinks/2022.12.01/wikilinks_lang=en.ttl.bz2
# cleaned object properties (en, 2022-12-01)
curl -O https://databus.dbpedia.org/dbpedia/mappings/mappingbased-objects/2022.12.01/mappingbased-objects_lang=en.ttl.bz2
# types, transitive inference (en, 2022-12-01)
curl -O https://databus.dbpedia.org/dbpedia/mappings/instance-types/2022.12.01/instance-types_inference=transitive_lang=en.ttl.bz2
# ontology
curl -O https://databus.dbpedia.org/ontologies/dbpedia.org/ontology--DEV/2022.12.09-011003/ontology--DEV_type=parsed.nt

# Extract data
bzip2 -d wikilinks_lang=en.ttl.bz2
bzip2 -d mappingbased-objects_lang=en.ttl.bz2
bzip2 -d instance-types_inference=transitive_lang=en.ttl.bz2
bzip2 -d ontology--DEV_type=parsed.nt