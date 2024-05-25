// degree centrality - all links

RETURN "In-, out- and undirected degree of all links" AS `STATUS`;

RETURN "In-degree" AS `STATUS`;

MATCH (n:Resource)
RETURN
    avg(n.in_degree_all) AS `mean`,
    min(n.in_degree_all) AS `min`,
    percentileDisc(n.in_degree_all, 0.1) AS `0.10`,
    percentileDisc(n.in_degree_all, 0.2) AS `0.20`,
    percentileDisc(n.in_degree_all, 0.3) AS `0.30`,
    percentileDisc(n.in_degree_all, 0.4) AS `0.40`,
    percentileDisc(n.in_degree_all, 0.5) AS `0.50`,
    percentileDisc(n.in_degree_all, 0.6) AS `0.60`,
    percentileDisc(n.in_degree_all, 0.7) AS `0.70`,
    percentileDisc(n.in_degree_all, 0.8) AS `0.80`,
    percentileDisc(n.in_degree_all, 0.9) AS `0.90`,
    percentileDisc(n.in_degree_all, 0.95) AS `0.95`,
    percentileDisc(n.in_degree_all, 0.99) AS `0.99`,
    percentileDisc(n.in_degree_all, 0.999) AS `0.999`,
    max(n.in_degree_all) AS `max`
;

RETURN "Out-degree" AS `STATUS`;

MATCH (n:Resource)
RETURN
    avg(n.out_degree_all) AS `mean`,
    min(n.out_degree_all) AS `min`,
    percentileDisc(n.out_degree_all, 0.1) AS `0.10`,
    percentileDisc(n.out_degree_all, 0.2) AS `0.20`,
    percentileDisc(n.out_degree_all, 0.3) AS `0.30`,
    percentileDisc(n.out_degree_all, 0.4) AS `0.40`,
    percentileDisc(n.out_degree_all, 0.5) AS `0.50`,
    percentileDisc(n.out_degree_all, 0.6) AS `0.60`,
    percentileDisc(n.out_degree_all, 0.7) AS `0.70`,
    percentileDisc(n.out_degree_all, 0.8) AS `0.80`,
    percentileDisc(n.out_degree_all, 0.9) AS `0.90`,
    percentileDisc(n.out_degree_all, 0.95) AS `0.95`,
    percentileDisc(n.out_degree_all, 0.99) AS `0.99`,
    percentileDisc(n.out_degree_all, 0.999) AS `0.999`,
    max(n.out_degree_all) AS `max`
;

RETURN "Undirected degree" AS `STATUS`;

MATCH (n:Resource)
RETURN
    avg(n.undirected_degree_all) AS `mean`,
    min(n.undirected_degree_all) AS `min`,
    percentileDisc(n.undirected_degree_all, 0.1) AS `0.10`,
    percentileDisc(n.undirected_degree_all, 0.2) AS `0.20`,
    percentileDisc(n.undirected_degree_all, 0.3) AS `0.30`,
    percentileDisc(n.undirected_degree_all, 0.4) AS `0.40`,
    percentileDisc(n.undirected_degree_all, 0.5) AS `0.50`,
    percentileDisc(n.undirected_degree_all, 0.6) AS `0.60`,
    percentileDisc(n.undirected_degree_all, 0.7) AS `0.70`,
    percentileDisc(n.undirected_degree_all, 0.8) AS `0.80`,
    percentileDisc(n.undirected_degree_all, 0.9) AS `0.90`,
    percentileDisc(n.undirected_degree_all, 0.95) AS `0.95`,
    percentileDisc(n.undirected_degree_all, 0.99) AS `0.99`,
    percentileDisc(n.undirected_degree_all, 0.999) AS `0.999`,
    max(n.undirected_degree_all) AS `max`
;


// degree centrality - wikilinks

RETURN "In-, out- and undirected degree of wikilinks" AS `STATUS`;

RETURN "In-degree" AS `STATUS`;

MATCH (n:Resource)
RETURN
    avg(n.in_degree_wikilinks) AS `mean`,
    min(n.in_degree_wikilinks) AS `min`,
    percentileDisc(n.in_degree_wikilinks, 0.1) AS `0.10`,
    percentileDisc(n.in_degree_wikilinks, 0.2) AS `0.20`,
    percentileDisc(n.in_degree_wikilinks, 0.3) AS `0.30`,
    percentileDisc(n.in_degree_wikilinks, 0.4) AS `0.40`,
    percentileDisc(n.in_degree_wikilinks, 0.5) AS `0.50`,
    percentileDisc(n.in_degree_wikilinks, 0.6) AS `0.60`,
    percentileDisc(n.in_degree_wikilinks, 0.7) AS `0.70`,
    percentileDisc(n.in_degree_wikilinks, 0.8) AS `0.80`,
    percentileDisc(n.in_degree_wikilinks, 0.9) AS `0.90`,
    percentileDisc(n.in_degree_wikilinks, 0.95) AS `0.95`,
    percentileDisc(n.in_degree_wikilinks, 0.99) AS `0.99`,
    percentileDisc(n.in_degree_wikilinks, 0.999) AS `0.999`,
    max(n.in_degree_wikilinks) AS `max`
;

RETURN "Out-degree" AS `STATUS`;

MATCH (n:Resource)
RETURN
    avg(n.out_degree_wikilinks) AS `mean`,
    min(n.out_degree_wikilinks) AS `min`,
    percentileDisc(n.out_degree_wikilinks, 0.1) AS `0.10`,
    percentileDisc(n.out_degree_wikilinks, 0.2) AS `0.20`,
    percentileDisc(n.out_degree_wikilinks, 0.3) AS `0.30`,
    percentileDisc(n.out_degree_wikilinks, 0.4) AS `0.40`,
    percentileDisc(n.out_degree_wikilinks, 0.5) AS `0.50`,
    percentileDisc(n.out_degree_wikilinks, 0.6) AS `0.60`,
    percentileDisc(n.out_degree_wikilinks, 0.7) AS `0.70`,
    percentileDisc(n.out_degree_wikilinks, 0.8) AS `0.80`,
    percentileDisc(n.out_degree_wikilinks, 0.9) AS `0.90`,
    percentileDisc(n.out_degree_wikilinks, 0.95) AS `0.95`,
    percentileDisc(n.out_degree_wikilinks, 0.99) AS `0.99`,
    percentileDisc(n.out_degree_wikilinks, 0.999) AS `0.999`,
    max(n.out_degree_wikilinks) AS `max`
;

RETURN "Undirected degree" AS `STATUS`;

MATCH (n:Resource)
RETURN
    avg(n.undirected_degree_wikilinks) AS `mean`,
    min(n.undirected_degree_wikilinks) AS `min`,
    percentileDisc(n.undirected_degree_wikilinks, 0.1) AS `0.10`,
    percentileDisc(n.undirected_degree_wikilinks, 0.2) AS `0.20`,
    percentileDisc(n.undirected_degree_wikilinks, 0.3) AS `0.30`,
    percentileDisc(n.undirected_degree_wikilinks, 0.4) AS `0.40`,
    percentileDisc(n.undirected_degree_wikilinks, 0.5) AS `0.50`,
    percentileDisc(n.undirected_degree_wikilinks, 0.6) AS `0.60`,
    percentileDisc(n.undirected_degree_wikilinks, 0.7) AS `0.70`,
    percentileDisc(n.undirected_degree_wikilinks, 0.8) AS `0.80`,
    percentileDisc(n.undirected_degree_wikilinks, 0.9) AS `0.90`,
    percentileDisc(n.undirected_degree_wikilinks, 0.95) AS `0.95`,
    percentileDisc(n.undirected_degree_wikilinks, 0.99) AS `0.99`,
    percentileDisc(n.undirected_degree_wikilinks, 0.999) AS `0.999`,
    max(n.undirected_degree_wikilinks) AS `max`
;


// degree centrality - all links except wikilinks

RETURN "In-, out- and undirected degree of all links except wikilinks" AS `STATUS`;

RETURN "In-degree" AS `STATUS`;

MATCH (n:Resource)
RETURN
    avg(n.in_degree_all_except_wikilinks) AS `mean`,
    min(n.in_degree_all_except_wikilinks) AS `min`,
    percentileDisc(n.in_degree_all_except_wikilinks, 0.1) AS `0.10`,
    percentileDisc(n.in_degree_all_except_wikilinks, 0.2) AS `0.20`,
    percentileDisc(n.in_degree_all_except_wikilinks, 0.3) AS `0.30`,
    percentileDisc(n.in_degree_all_except_wikilinks, 0.4) AS `0.40`,
    percentileDisc(n.in_degree_all_except_wikilinks, 0.5) AS `0.50`,
    percentileDisc(n.in_degree_all_except_wikilinks, 0.6) AS `0.60`,
    percentileDisc(n.in_degree_all_except_wikilinks, 0.7) AS `0.70`,
    percentileDisc(n.in_degree_all_except_wikilinks, 0.8) AS `0.80`,
    percentileDisc(n.in_degree_all_except_wikilinks, 0.9) AS `0.90`,
    percentileDisc(n.in_degree_all_except_wikilinks, 0.95) AS `0.95`,
    percentileDisc(n.in_degree_all_except_wikilinks, 0.99) AS `0.99`,
    percentileDisc(n.in_degree_all_except_wikilinks, 0.999) AS `0.999`,
    max(n.in_degree_all_except_wikilinks) AS `max`
;

RETURN "Out-degree" AS `STATUS`;

MATCH (n:Resource)
RETURN
    avg(n.out_degree_all_except_wikilinks) AS `mean`,
    min(n.out_degree_all_except_wikilinks) AS `min`,
    percentileDisc(n.out_degree_all_except_wikilinks, 0.1) AS `0.10`,
    percentileDisc(n.out_degree_all_except_wikilinks, 0.2) AS `0.20`,
    percentileDisc(n.out_degree_all_except_wikilinks, 0.3) AS `0.30`,
    percentileDisc(n.out_degree_all_except_wikilinks, 0.4) AS `0.40`,
    percentileDisc(n.out_degree_all_except_wikilinks, 0.5) AS `0.50`,
    percentileDisc(n.out_degree_all_except_wikilinks, 0.6) AS `0.60`,
    percentileDisc(n.out_degree_all_except_wikilinks, 0.7) AS `0.70`,
    percentileDisc(n.out_degree_all_except_wikilinks, 0.8) AS `0.80`,
    percentileDisc(n.out_degree_all_except_wikilinks, 0.90) AS `0.90`,
    percentileDisc(n.out_degree_all_except_wikilinks, 0.95) AS `0.95`,
    percentileDisc(n.out_degree_all_except_wikilinks, 0.99) AS `0.99`,
    percentileDisc(n.out_degree_all_except_wikilinks, 0.999) AS `0.999`,
    max(n.out_degree_all_except_wikilinks) AS `max`
;

RETURN "Undirected degree" AS `STATUS`;

MATCH (n:Resource)
RETURN
    avg(n.undirected_degree_all_except_wikilinks) AS `mean`,
    min(n.undirected_degree_all_except_wikilinks) AS `min`,
    percentileDisc(n.undirected_degree_all_except_wikilinks, 0.1) AS `0.10`,
    percentileDisc(n.undirected_degree_all_except_wikilinks, 0.2) AS `0.20`,
    percentileDisc(n.undirected_degree_all_except_wikilinks, 0.3) AS `0.30`,
    percentileDisc(n.undirected_degree_all_except_wikilinks, 0.4) AS `0.40`,
    percentileDisc(n.undirected_degree_all_except_wikilinks, 0.5) AS `0.50`,
    percentileDisc(n.undirected_degree_all_except_wikilinks, 0.6) AS `0.60`,
    percentileDisc(n.undirected_degree_all_except_wikilinks, 0.7) AS `0.70`,
    percentileDisc(n.undirected_degree_all_except_wikilinks, 0.8) AS `0.80`,
    percentileDisc(n.undirected_degree_all_except_wikilinks, 0.9) AS `0.90`,
    percentileDisc(n.undirected_degree_all_except_wikilinks, 0.95) AS `0.95`,
    percentileDisc(n.undirected_degree_all_except_wikilinks, 0.99) AS `0.99`,
    percentileDisc(n.undirected_degree_all_except_wikilinks, 0.999) AS `0.999`,
    max(n.undirected_degree_all_except_wikilinks) AS `max`
;


// distribution of number of mutual wikilinks

RETURN "Distribution of number of mutual Wikilinks per entity" AS `STATUS`;

MATCH (n:Resource)
RETURN
    avg(n.n_mutual_wikilinks) AS `mean`,
    min(n.n_mutual_wikilinks) AS `min`,
    percentileDisc(n.n_mutual_wikilinks, 0.1) AS `0.10`,
    percentileDisc(n.n_mutual_wikilinks, 0.2) AS `0.20`,
    percentileDisc(n.n_mutual_wikilinks, 0.3) AS `0.30`,
    percentileDisc(n.n_mutual_wikilinks, 0.4) AS `0.40`,
    percentileDisc(n.n_mutual_wikilinks, 0.5) AS `0.50`,
    percentileDisc(n.n_mutual_wikilinks, 0.6) AS `0.60`,
    percentileDisc(n.n_mutual_wikilinks, 0.7) AS `0.70`,
    percentileDisc(n.n_mutual_wikilinks, 0.8) AS `0.80`,
    percentileDisc(n.n_mutual_wikilinks, 0.9) AS `0.90`,
    percentileDisc(n.n_mutual_wikilinks, 0.95) AS `0.95`,
    percentileDisc(n.n_mutual_wikilinks, 0.99) AS `0.99`,
    percentileDisc(n.n_mutual_wikilinks, 0.999) AS `0.999`,
    max(n.n_mutual_wikilinks) AS `max`
;


// count of unique properties

RETURN "Count of unique properties" AS `STATUS`;

CALL db.relationshipTypes() YIELD relationshipType as type
CALL apoc.cypher.run('MATCH ()-[:`'+type+'`]->() RETURN count(*) as count',{}) YIELD value
WHERE type STARTS WITH "http://dbpedia.org/ontology/"
RETURN count(*);


// most common properties

RETURN "Most common properties" AS `STATUS`;

CALL db.relationshipTypes() YIELD relationshipType as type
CALL apoc.cypher.run('MATCH ()-[:`'+type+'`]->() RETURN count(*) as count',{}) YIELD value
WHERE type STARTS WITH "http://dbpedia.org/ontology/"
RETURN type, value.count
ORDER BY value.count DESC
LIMIT 10;


// distribution of number of entities per property

RETURN "Distribution of number of entities per property" AS `STATUS`;

CALL db.relationshipTypes() YIELD relationshipType as type
CALL apoc.cypher.run('MATCH ()-[:`'+type+'`]->() RETURN count(*) as count',{}) YIELD value
WHERE type STARTS WITH "http://dbpedia.org/ontology/"
RETURN
    avg(value.count) AS `mean`,
    min(value.count) AS `min`,
    percentileDisc(value.count, 0.1) AS `0.10`,
    percentileDisc(value.count, 0.2) AS `0.20`,
    percentileDisc(value.count, 0.3) AS `0.30`,
    percentileDisc(value.count, 0.4) AS `0.40`,
    percentileDisc(value.count, 0.5) AS `0.50`,
    percentileDisc(value.count, 0.6) AS `0.60`,
    percentileDisc(value.count, 0.7) AS `0.70`,
    percentileDisc(value.count, 0.8) AS `0.80`,
    percentileDisc(value.count, 0.9) AS `0.90`,
    percentileDisc(value.count, 0.95) AS `0.95`,
    percentileDisc(value.count, 0.99) AS `0.99`,
    percentileDisc(value.count, 0.999) AS `0.999`,
    max(value.count) AS `max`
;


// distribution of number of types per entity

RETURN "Distribution of number of types per entity" AS `STATUS`;

MATCH (n:Resource)
RETURN
    avg(n.n_types) AS `mean`,
    min(n.n_types) AS `min`,
    percentileDisc(n.n_types, 0.1) AS `0.10`,
    percentileDisc(n.n_types, 0.2) AS `0.20`,
    percentileDisc(n.n_types, 0.3) AS `0.30`,
    percentileDisc(n.n_types, 0.4) AS `0.40`,
    percentileDisc(n.n_types, 0.5) AS `0.50`,
    percentileDisc(n.n_types, 0.6) AS `0.60`,
    percentileDisc(n.n_types, 0.7) AS `0.70`,
    percentileDisc(n.n_types, 0.8) AS `0.80`,
    percentileDisc(n.n_types, 0.9) AS `0.90`,
    percentileDisc(n.n_types, 0.95) AS `0.95`,
    percentileDisc(n.n_types, 0.99) AS `0.99`,
    percentileDisc(n.n_types, 0.999) AS `0.999`,
    max(n.n_types) AS `max`
;


// count of unique types

RETURN "Count of unique types" AS `STATUS`;

CALL db.labels() YIELD label
CALL apoc.cypher.run('MATCH (:`'+label+'`) RETURN count(*) as count',{}) YIELD value
WHERE
    label <> "Resource"
    AND label <> "_GraphConfig"
    AND label <> "Ontology"
    AND label <> "http://www.w3.org/2002/07/owl#Class"
    AND label <> "http://www.w3.org/2002/07/owl#DatatypeProperty"
    AND label <> "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"
    AND label <> "http://www.w3.org/2002/07/owl#FunctionalProperty"
    AND label <> "http://www.w3.org/2002/07/owl#ObjectProperty"
    AND label <> "http://purl.org/vocommons/voaf#Vocabulary"
    AND label <> "http://www.w3.org/2002/07/owl#Ontology"
    AND label <> "http://www.w3.org/2000/01/rdf-schema#Datatype"
RETURN count(*) AS `count of unique types`;


// most common types

RETURN "Most common types" AS `STATUS`;

CALL db.labels() YIELD label
CALL apoc.cypher.run('MATCH (:`'+label+'`) RETURN count(*) as count',{}) YIELD value
WHERE
    label <> "Resource"
    AND label <> "_GraphConfig"
    AND label <> "Ontology"
    AND label <> "http://www.w3.org/2002/07/owl#Class"
    AND label <> "http://www.w3.org/2002/07/owl#DatatypeProperty"
    AND label <> "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"
    AND label <> "http://www.w3.org/2002/07/owl#FunctionalProperty"
    AND label <> "http://www.w3.org/2002/07/owl#ObjectProperty"
    AND label <> "http://purl.org/vocommons/voaf#Vocabulary"
    AND label <> "http://www.w3.org/2002/07/owl#Ontology"
    AND label <> "http://www.w3.org/2000/01/rdf-schema#Datatype"
RETURN label, value.count
ORDER BY value.count DESC
LIMIT 50;


// distribution of number of entities per type

RETURN "Distribution of number of entities per type" AS `STATUS`;

CALL db.labels() YIELD label
CALL apoc.cypher.run('MATCH (:`'+label+'`) RETURN count(*) as count',{}) YIELD value
WHERE
    label <> "Resource"
    AND label <> "_GraphConfig"
    AND label <> "Ontology"
    AND label <> "http://www.w3.org/2002/07/owl#Class"
    AND label <> "http://www.w3.org/2002/07/owl#DatatypeProperty"
    AND label <> "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"
    AND label <> "http://www.w3.org/2002/07/owl#FunctionalProperty"
    AND label <> "http://www.w3.org/2002/07/owl#ObjectProperty"
    AND label <> "http://purl.org/vocommons/voaf#Vocabulary"
    AND label <> "http://www.w3.org/2002/07/owl#Ontology"
    AND label <> "http://www.w3.org/2000/01/rdf-schema#Datatype"
RETURN
    avg(value.count) AS `mean`,
    min(value.count) AS `min`,
    percentileDisc(value.count, 0.1) AS `0.10`,
    percentileDisc(value.count, 0.2) AS `0.20`,
    percentileDisc(value.count, 0.3) AS `0.30`,
    percentileDisc(value.count, 0.4) AS `0.40`,
    percentileDisc(value.count, 0.5) AS `0.50`,
    percentileDisc(value.count, 0.6) AS `0.60`,
    percentileDisc(value.count, 0.7) AS `0.70`,
    percentileDisc(value.count, 0.8) AS `0.80`,
    percentileDisc(value.count, 0.9) AS `0.90`,
    percentileDisc(value.count, 0.95) AS `0.95`,
    percentileDisc(value.count, 0.99) AS `0.99`,
    percentileDisc(value.count, 0.999) AS `0.999`,
    max(value.count) AS `max`
;


// count of all nodes, nodes with wikilink(s), nodes with mutual wikilink(s)

RETURN "Count of all entities" AS `STATUS`;

MATCH (n:Resource)
RETURN count(n) AS `count (all nodes)`;

RETURN "Count of entities with wikilinks" AS `STATUS`;

MATCH (n:Resource)
WHERE n.undirected_degree_wikilinks > 0
RETURN count(n) AS `count (nodes with wikilinks)`;

RETURN "Count of entities with mutual wikilinks" AS `STATUS`;

MATCH (n:Resource)
WHERE n.n_mutual_wikilinks > 0
RETURN count(n) AS `count (nodes with mutual wikilinks)`;


// distribution of number of other properties connecting a pair that is also wikilinked
// note: the pairs and their property counts appear twice, because each pair has two mutual_wikilinks edges
//       this does not change the percentile values and mean though

RETURN "Distribution of number of other properties connecting a pair that is also wikilinked (one sided count)" AS `STATUS`;

MATCH (a)-[r:mutual_wikilinks]->(b)
RETURN
    avg(r.n_connecting_properties_out + r.n_connecting_properties_in) AS `mean`,
    min(r.n_connecting_properties_out + r.n_connecting_properties_in) AS `min`,
    percentileDisc(r.n_connecting_properties_out + r.n_connecting_properties_in, 0.1) AS `0.10`,
    percentileDisc(r.n_connecting_properties_out + r.n_connecting_properties_in, 0.2) AS `0.20`,
    percentileDisc(r.n_connecting_properties_out + r.n_connecting_properties_in, 0.3) AS `0.30`,
    percentileDisc(r.n_connecting_properties_out + r.n_connecting_properties_in, 0.4) AS `0.40`,
    percentileDisc(r.n_connecting_properties_out + r.n_connecting_properties_in, 0.5) AS `0.50`,
    percentileDisc(r.n_connecting_properties_out + r.n_connecting_properties_in, 0.6) AS `0.60`,
    percentileDisc(r.n_connecting_properties_out + r.n_connecting_properties_in, 0.7) AS `0.70`,
    percentileDisc(r.n_connecting_properties_out + r.n_connecting_properties_in, 0.8) AS `0.80`,
    percentileDisc(r.n_connecting_properties_out + r.n_connecting_properties_in, 0.9) AS `0.90`,
    percentileDisc(r.n_connecting_properties_out + r.n_connecting_properties_in, 0.95) AS `0.95`,
    percentileDisc(r.n_connecting_properties_out + r.n_connecting_properties_in, 0.99) AS `0.99`,
    percentileDisc(r.n_connecting_properties_out + r.n_connecting_properties_in, 0.999) AS `0.999`,
    max(r.n_connecting_properties_out + r.n_connecting_properties_in) AS `max`
;


// number of entity pairs with mutual wikilinks
// count is divided by two because each pair has two mutual_wikilinks edges

RETURN "Count of mutually wikilinked entity pairs" AS `STATUS`;

MATCH (a)-[r:mutual_wikilinks]->(b)
RETURN count(r) / 2 AS `number of entity pairs with mututal wikilinks`;


// number of entity pairs with mutual wikilinks and at least one other connecting property (in either direction)
// count is divided by two because each pair has two mutual_wikilinks edges

RETURN "Count of mutually wikilinked entity pairs with at least one connecting property" AS `STATUS`;

MATCH (a)-[r:mutual_wikilinks]->(b)
WHERE r.n_connecting_properties_in > 0 OR r.n_connecting_properties_out > 0
RETURN count(r) / 2 AS `number of entity pairs with mututal wikilinks and at least one connecting property`;