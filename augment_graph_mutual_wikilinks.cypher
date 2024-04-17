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