// initialize database

RETURN "Initialize database..." AS `STATUS: `;

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


// load data

RETURN "Load ontology dataset..." AS `STATUS: `;

CALL n10s.rdf.import.fetch(
    "file:///var/lib/neo4j/raw_data/ontology--DEV_type=parsed_sorted.nt",
    "N-Triples",
    {verifyUriSyntax: false}
);

// remove Resource labels and replace them with Ontology label
MATCH (n:Resource)
REMOVE n:Resource
SET n:Ontology;

RETURN "Load instance types datasets..." AS `STATUS: `;

CALL n10s.rdf.import.fetch(
    "file:///var/lib/neo4j/raw_data/instance-types_inference=specific_lang=en.ttl",
    "Turtle",
    {verifyUriSyntax: false}
);

CALL n10s.rdf.import.fetch(
    "file:///var/lib/neo4j/raw_data/instance-types_inference=transitive_lang=en.ttl",
    "Turtle",
    {verifyUriSyntax: false}
);

RETURN "Load object properties dataset..." AS `STATUS: `;

CALL n10s.rdf.import.fetch(
    "file:///var/lib/neo4j/raw_data/mappingbased-objects_lang=en.ttl",
    "Turtle",
    {verifyUriSyntax: false}
);

RETURN "Load wikilinks dataset..." AS `STATUS: `;

CALL n10s.rdf.import.fetch(
    "file:///var/lib/neo4j/raw_data/wikilinks_lang=en.ttl",
    "Turtle",
    {verifyUriSyntax: false}
);

RETURN "Done!" AS `STATUS: `;