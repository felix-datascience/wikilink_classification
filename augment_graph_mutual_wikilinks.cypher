// mutual wikilinks edges

RETURN "Add edges between mutually (wiki)linked entities in the graph" AS `STATUS`;

MATCH (a:Resource)-[:`http://dbpedia.org/ontology/wikiPageWikiLink`]->(b:Resource)-[:`http://dbpedia.org/ontology/wikiPageWikiLink`]->(a:Resource)
WHERE
    a.out_degree_wikilinks > 0
    AND a.in_degree_wikilinks > 0
    AND b.out_degree_wikilinks > 0
    AND b.in_degree_wikilinks > 0
CREATE (a)-[:mutual_wikilinks]->(b);


// mutual wikilinks counts per node

RETURN "Calculate and write number of mutual wikilinks per node" AS `STATUS`;

RETURN "Create in-memory graph containing mutual wikilinks..." AS `STATUS`;

CALL gds.graph.project("mutualWikilinksProjection", "Resource", "mutual_wikilinks")
YIELD graphName, nodeProjection, nodeCount, relationshipProjection, relationshipCount, projectMillis;

RETURN "Calculate and write degree (in degree = out degree)..." AS `STATUS`;

CALL gds.degree.write("mutualWikilinksProjection", {orientation: "NATURAL", writeProperty: "n_mutual_wikilinks" })
YIELD centralityDistribution
RETURN centralityDistribution AS degree_centrality_mutual_wikilinks;


// number of links (except wikilinks) connecting a mutually (wiki)linked pair of entities

MATCH (a:Resource)-[m:mutual_wikilinks]->(b:Resource)
WITH a, b, m
OPTIONAL MATCH (a)-[r]->(b)
WHERE
NOT r:mutual_wikilinks
AND NOT r:`http://dbpedia.org/ontology/wikiPageWikiLink`
WITH a, b, m, count(r) AS n_connecting_properties_out
OPTIONAL MATCH (a)<-[r]-(b)
WHERE
NOT r:mutual_wikilinks
AND NOT r:`http://dbpedia.org/ontology/wikiPageWikiLink`
WITH a, b, m, n_connecting_properties_out, count(r) AS n_connecting_properties_in
SET m.n_connecting_properties_out = n_connecting_properties_out
SET m.n_connecting_properties_in = n_connecting_properties_in;