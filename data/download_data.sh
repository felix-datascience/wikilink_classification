# Download data
# wikilinks (en, 2022-12-01)
curl -O https://databus.dbpedia.org/dbpedia/generic/wikilinks/2022.12.01/wikilinks_lang=en.ttl.bz2
# infobox-properties (en, 2022-12-01)
curl -O https://databus.dbpedia.org/dbpedia/generic/infobox-properties/2022.12.01/infobox-properties_lang=en.ttl.bz2

# Extract data
bzip2 -d wikilinks_lang=en.ttl.bz2
bzip2 -d infobox-properties_lang=en.ttl.bz2
