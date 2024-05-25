#!/bin/bash

# This script is intended to be used on BWUniCluster 2.0 after the setup and data augmentation scripts have been run.
# It performs a data analysis to gather insights about the knowledge graph, especially regarding entities that are
# linked with wikilinks.

CURRENT_DIR=$(pwd)
LOG_FILE_PATH=$CURRENT_DIR/neo4j_export_data_log.txt

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

echo -e "[$(date +%T)] * Start neo4j data export...\n"

# create directory for exported data, start database and run data export script
cp $CURRENT_DIR/export_data.cypher $(ws_find $WORKSPACE_NAME)/containers/$NEO4J_CONTAINER_NAME/var/lib/neo4j
enroot start --rw $NEO4J_CONTAINER_NAME bash << EOF
    mkdir exported_data
    bin/neo4j start
    sleep 180
    cat export_data.cypher | bin/cypher-shell -u neo4j -p $PASSWORD > query_output.txt
    bin/neo4j stop
EOF
echo -e "\n[$(date +%T)] * Data export script output:\n"
cat $(ws_find $WORKSPACE_NAME)/containers/$NEO4J_CONTAINER_NAME/var/lib/neo4j/query_output.txt >> $LOG_FILE_PATH
rm $(ws_find $WORKSPACE_NAME)/containers/$NEO4J_CONTAINER_NAME/var/lib/neo4j/query_output.txt

echo -e "\n[$(date +%T)] * Done!\n"