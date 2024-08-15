// sample entities

WITH "
    MATCH (n:Resource)
    WITH n, rand() as r
    ORDER BY r LIMIT 50000
    RETURN
        n.uri AS subject,
        n.in_degree_wikilinks AS in_degree_wikilinks,
        n.out_degree_wikilinks AS out_degree_wikilinks,
        n.in_degree_all_except_wikilinks AS in_degree_all_except_wikilinks,
        n.out_degree_all_except_wikilinks AS out_degree_all_except_wikilinks,
        n.n_types as n_types,
        n.n_mutual_wikilinks as n_mutual_wikilinks
" AS query
CALL apoc.export.csv.query(query, "exported_data/entities_sample.csv", {})
YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data
RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data;