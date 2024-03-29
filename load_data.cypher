CREATE CONSTRAINT n10s_unique_uri FOR (r:Resource) REQUIRE r.uri IS UNIQUE;

CALL n10s.graphconfig.init({
	handleVocabUris: "KEEP",
	handleMultival: "OVERWRITE",
	multivalPropList: [],
	keepLangTag: true,
	handleRDFTypes: "LABELS",
	keepCustomDataTypes: false,
	customDataTypePropList: [],
	applyNeo4jNaming: false
});

CALL n10s.rdf.import.fetch(
    "file:///var/lib/neo4j/raw_data/wikilinks_lang=en.ttl",
    "Turtle",
    {verifyUriSyntax: false}
);


CALL n10s.rdf.import.fetch(
    "file:///var/lib/neo4j/raw_data/mappingbased-objects_lang=en.ttl",
    "Turtle",
    {verifyUriSyntax: false}
);

CALL n10s.rdf.import.fetch(
    "file:///var/lib/neo4j/raw_data/instance-types_inference=transitive_lang=en.ttl",
    "Turtle",
    {verifyUriSyntax: false}
);

CALL n10s.rdf.import.fetch(
    "file:///var/lib/neo4j/raw_data/ontology--DEV_type=parsed.nt",
    "N-Triples",
    {verifyUriSyntax: false}
);