// number of types per node

MATCH (n:Resource)
// number of types is equal to number of labels - 1 (because of Resource label)
SET n.n_types = (SIZE(LABELS(n)) - 1);


// degree centrality - all links

RETURN "Create in-memory graph containing all links..." AS `STATUS`;

CALL gds.graph.project("wholeGraphProjection", "Resource", "*")
YIELD graphName, nodeProjection, nodeCount, relationshipProjection, relationshipCount, projectMillis;

RETURN "Calculate and write in-degree..." AS `STATUS`;

CALL gds.degree.write("wholeGraphProjection", {orientation: "REVERSE", writeProperty: "in_degree_all" })
YIELD centralityDistribution
RETURN centralityDistribution AS in_degree_centrality_all;

RETURN "Calculate and write out-degree..." AS `STATUS`;

CALL gds.degree.write("wholeGraphProjection", {orientation: "NATURAL", writeProperty: "out_degree_all" })
YIELD centralityDistribution
RETURN centralityDistribution AS out_degree_centrality_all;

RETURN "Calculate and write undirected degree..." AS `STATUS`;

CALL gds.degree.write("wholeGraphProjection", {orientation: "UNDIRECTED", writeProperty: "undirected_degree_all" })
YIELD centralityDistribution
RETURN centralityDistribution AS undirected_degree_centrality_all;


// degree centrality - wikilinks

RETURN "Create in-memory graph containing only wikilinks..." AS `STATUS`;

CALL gds.graph.project("wikilinksProjection", "Resource", "http://dbpedia.org/ontology/wikiPageWikiLink")
YIELD graphName, nodeProjection, nodeCount, relationshipProjection, relationshipCount, projectMillis;

RETURN "Calculate and write in-degree..." AS `STATUS`;

CALL gds.degree.write("wikilinksProjection", {orientation: "REVERSE", writeProperty: "in_degree_wikilinks" })
YIELD centralityDistribution
RETURN centralityDistribution AS in_degree_centrality_wikilinks;

RETURN "Calculate and write out-degree..." AS `STATUS`;

CALL gds.degree.write("wikilinksProjection", {orientation: "NATURAL", writeProperty: "out_degree_wikilinks" })
YIELD centralityDistribution
RETURN centralityDistribution AS out_degree_centrality_wikilinks;

RETURN "Calculate and write undirected degree..." AS `STATUS`;

CALL gds.degree.write("wikilinksProjection", {orientation: "UNDIRECTED", writeProperty: "undirected_degree_wikilinks" })
YIELD centralityDistribution
RETURN centralityDistribution AS undirected_degree_centrality_wikilinks;


// degree centrality - all links except wikilinks

RETURN "Calculate and write in-, out- and undirected degree..." AS `STATUS`;

MATCH (n:Resource)
SET
    n.in_degree_all_except_wikilinks = n.in_degree_all - n.in_degree_wikilinks,
    n.out_degree_all_except_wikilinks = n.out_degree_all - n.out_degree_wikilinks,
    n.undirected_degree_all_except_wikilinks = n.undirected_degree_all - n.undirected_degree_wikilinks
;