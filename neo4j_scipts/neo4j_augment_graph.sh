#!/bin/bash

# This script is intended to be used on BWUniCluster 2.0 after the setup scrip has been run.
# It augments the entities in the graph with information like their number of types, degree centrality
# and number of mutual wikilinks.

CURRENT_DIR=$(pwd)
LOG_FILE_PATH=$CURRENT_DIR/neo4j_augment_graph_log.txt

# read flags
while getopts p:c:w flag                                                           
do                                                                              
    case "${flag}" in                                                           
        p) PASSWORD=${OPTARG};;                                                 
        c) NEO4J_CONTAINER_NAME=${OPTARG};;
        w) WORKSPACE_NAME=${OPTARG};;
    esac                                                                        
done   
if [[ $PASSWORD == "" ]]; then
    echo "\nERROR: Password for the neo4j database has to be specified (use -p argument)!\n"
    exit 1
fi
if [[ $NEO4J_CONTAINER_NAME == "" ]]; then
    NEO4J_CONTAINER_NAME="pyxis_neo4j"
fi
if [[ $WORKSPACE_NAME == "" ]]; then
    WORKSPACE_NAME="wikilinks_ws"
fi

# from here on, redirect output to log file
exec >$LOG_FILE_PATH 2>&1

echo -e "[$(date +%T)] * Start neo4j graph augmentation...\n"

# start database and run types and degree centrality augmentation script
cp $CURRENT_DIR/augment_graph_types_and_degree_centrality.cypher $(ws_find $WORKSPACE_NAME)/containers/$NEO4J_CONTAINER_NAME/var/lib/neo4j
enroot start --rw $NEO4J_CONTAINER_NAME bash << EOF
    bin/neo4j start
    sleep 180
    cat augment_graph_types_and_degree_centrality.cypher | bin/cypher-shell -u neo4j -p $PASSWORD > query_output.txt
    bin/neo4j stop
EOF
echo -e "\n[$(date +%T)] * Types and degree augmentation script output:\n"
cat $(ws_find $WORKSPACE_NAME)/containers/$NEO4J_CONTAINER_NAME/var/lib/neo4j/query_output.txt >> $LOG_FILE_PATH
rm $(ws_find $WORKSPACE_NAME)/containers/$NEO4J_CONTAINER_NAME/var/lib/neo4j/query_output.txt
sleep 180

# run mutual wikilinks augmentation script
cp $CURRENT_DIR/augment_graph_mutual_wikilinks.cypher $(ws_find $WORKSPACE_NAME)/containers/$NEO4J_CONTAINER_NAME/var/lib/neo4j
enroot start --rw $NEO4J_CONTAINER_NAME bash << EOF
    bin/neo4j start
    sleep 180
    cat augment_graph_mutual_wikilinks.cypher | bin/cypher-shell -u neo4j -p $PASSWORD > query_output.txt
    bin/neo4j stop
EOF
echo -e "\n[$(date +%T)] * Mutual wikilinks augmentation script output:\n"
cat $(ws_find $WORKSPACE_NAME)/containers/$NEO4J_CONTAINER_NAME/var/lib/neo4j/query_output.txt >> $LOG_FILE_PATH
rm $(ws_find $WORKSPACE_NAME)/containers/$NEO4J_CONTAINER_NAME/var/lib/neo4j/query_output.txt

echo -e "\n[$(date +%T)] * Done!\n"