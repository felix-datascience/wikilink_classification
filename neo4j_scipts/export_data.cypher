// property triples of mutually wikilinked entity pairs
// these triples do not contain wikilinks themselves
// only if at least one connecting property per entity exists

WITH "
    MATCH (a:Resource)-[r:mutual_wikilinks]->(b:Resource)
    WHERE
        r.n_connecting_properties_out > 0
        AND r.n_connecting_properties_in > 0
    WITH a, b
    MATCH (a)-[r]->(b)
    WHERE
        NOT r:mutual_wikilinks
        AND NOT r:`http://dbpedia.org/ontology/wikiPageWikiLink`
    RETURN
        a.uri AS subject,
        type(r) AS predicate,
        b.uri AS object
" AS query
CALL apoc.export.csv.query(query, "exported_data/mutual_wikilinks_properties_both_sides.csv", {})
YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data
RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data;


// property triples of mutually wikilinked entity pairs
// these triples do not contain wikilinks themselves
// only if just one entity links the other with one or more properties, the other entity doesn't
// note: this dataset can also be used to generate "placeholder" triples for the entity that does not link the other

WITH "
    MATCH (a:Resource)-[r:mutual_wikilinks]->(b:Resource)
    WHERE
        r.n_connecting_properties_out > 0
        AND r.n_connecting_properties_in = 0
    WITH a, b
    MATCH (a)-[r]->(b)
    WHERE
        NOT r:mutual_wikilinks
        AND NOT r:`http://dbpedia.org/ontology/wikiPageWikiLink`
    RETURN
        a.uri AS subject,
        type(r) AS predicate,
        b.uri AS object 
" AS query
CALL apoc.export.csv.query(query, "exported_data/mutual_wikilinks_properties_one_side.csv", {})
YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data
RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data;


// triples of mutually wikilinked entity pairs that are not connected with other properties
// only if both entities have at least one type or are part of at least one triple that is not a wikilink triple

WITH "
    MATCH (a:Resource)-[r:mutual_wikilinks]->(b:Resource)
    WHERE
        r.n_connecting_properties_out = 0
        AND r.n_connecting_properties_in = 0
        AND [a.n_types > 0 OR a.in_degree_all_except_wikilinks > 0 OR a.out_degree_all_except_wikilinks > 0]
        AND [b.n_types > 0 OR b.in_degree_all_except_wikilinks > 0 OR b.out_degree_all_except_wikilinks > 0]
    RETURN a.uri AS subject, 'http://dbpedia.org/ontology/wikiPageWikiLink' AS predicate, b.uri AS object" AS query
CALL apoc.export.csv.query(query, "exported_data/mutual_wikilinks_no_properties.csv", {})
YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data
RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data;


// triples of all other pairs
// these triples don't contain wikilinks
// all properties connecting entity pairs that are not connected via mutual wikilinks

WITH "
    MATCH (a:Resource)-[r]->(b:Resource)
    WHERE
        NOT exists((a)-[:mutual_wikilinks]->(b))
        AND NOT r:`http://dbpedia.org/ontology/wikiPageWikiLink`
    RETURN
        a.uri AS subject,
        type(r) AS predicate,
        b.uri AS object
" AS query
CALL apoc.export.csv.query(query, "exported_data/remaining_triples.csv", {})
YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data
RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data;


// type triples

WITH "
    MATCH (n:Resource)
    WHERE n.n_types > 0
    UNWIND labels(n) AS object
    WITH n.uri AS subject, 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate, object
    WHERE object <> 'Resource'
    RETURN subject, predicate, object
" AS query
CALL apoc.export.csv.query(query, "exported_data/type_triples.csv", {})
YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data
RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data;


// property counts

WITH "
    CALL db.relationshipTypes() YIELD relationshipType as type
    CALL apoc.cypher.run('MATCH ()-[:`'+type+'`]->() RETURN count(*) as count',{}) YIELD value
    WHERE type STARTS WITH 'http://dbpedia.org/ontology/'
    RETURN type, value.count
    ORDER BY value.count DESC
" AS query
CALL apoc.export.csv.query(query, "exported_data/property_counts.csv", {})
YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data
RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data;