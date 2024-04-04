#!/bin/bash

# This script is intended to be used on BWUniCluster 2.0.
# It sets up a workspace and a neo4j container with the initial raw data.

CURRENT_DIR=$(pwd)
LOG_FILE_PATH=$CURRENT_DIR/neo4j_setup_log.txt

# Read flags
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

# Test if workspace already exists
if [[ $(ws_list) =~ $WORKSPACE_NAME ]]; then

    # Workspace already exists, print error message and quit
    echo -e "\nERROR: ${WORKSPACE_NAME} workspace already exists.\n
Maybe the setup was already done before?
Otherwise, remove the workspace and restart the setup script.\n"

else

    # From here on, redirect output to log file
    exec >$LOG_FILE_PATH 2>&1

    echo -e "[$(date +%T)] * Start neo4j setup...\n"

    # Setup workspace
    echo -e "\n[$(date +%T)] * Setup workspace...\n"
    ws_allocate $WORKSPACE_NAME 60

    # Get RDF files
    cd $(ws_find $WORKSPACE_NAME)
    mkdir data
    cd data
    mkdir raw_data
    cd raw_data
    # wikilinks (en, 2022-12-01)
    echo -e "\n[$(date +%T)] * Download wikilinks dataset...\n"
    curl -L -O https://databus.dbpedia.org/dbpedia/generic/wikilinks/2022.12.01/wikilinks_lang=en.ttl.bz2
    echo -e "\n[$(date +%T)] * Extract wikilinks dataset...\n"
    bzip2 -d wikilinks_lang=en.ttl.bz2
    # cleaned object properties (en, 2022-12-01)
    echo -e "\n[$(date +%T)] * Download object properties dataset...\n"
    curl -L -O https://databus.dbpedia.org/dbpedia/mappings/mappingbased-objects/2022.12.01/mappingbased-objects_lang=en.ttl.bz2
    echo -e "\n[$(date +%T)] * Extract object properties dataset...\n"
    bzip2 -d mappingbased-objects_lang=en.ttl.bz2
    # types, transitive inference (en, 2022-12-01)
    echo -e "\n[$(date +%T)] * Download instance types dataset...\n"
    curl -L -O https://databus.dbpedia.org/dbpedia/mappings/instance-types/2022.12.01/instance-types_inference=transitive_lang=en.ttl.bz2
    echo -e "\n[$(date +%T)] * Extract instance types dataset...\n"
    bzip2 -d instance-types_inference=transitive_lang=en.ttl.bz2
    # ontology
    echo -e "\n[$(date +%T)] * Download ontology dataset...\n"
    curl -L -O https://databus.dbpedia.org/ontologies/dbpedia.org/ontology--DEV/2022.12.09-011003/ontology--DEV_type=parsed.nt

    # Setup neo4j in ENROOT container
    echo -e "\n[$(date +%T)] * Setup neo4j in ENROOT container...\n"
    # NOTE: The following lines define the location of ENROOT containers.
    # If there are other containers already available on the system they become invisible to ENROOT after running this script and restarting the shell.
    export ENROOT_DATA_PATH=$(ws_find $WORKSPACE_NAME)/containers
    echo -e "\n# define directory where enroot containers are stored\nexport ENROOT_DATA_PATH=$(ws_find $WORKSPACE_NAME)/containers" >> ~/.bashrc
    enroot import docker://neo4j:4.4.12-community
    enroot create -n $NEO4J_CONTAINER_NAME neo4j+4.4.12-community.sqsh
    rm neo4j+4.4-community.sqsh
    
    # Setup n10s plugin
    enroot start --rw $NEO4J_CONTAINER_NAME bash << EOF
        cd plugins
        wget https://github.com/neo4j-labs/neosemantics/releases/download/4.4.0.3/neosemantics-4.4.0.3.jar
        echo -e "\ndbms.unmanaged_extension_classes=n10s.endpoint=/rdf" >> ../conf/neo4j.conf
        exit
EOF

    # Setup graph data science plugin
    enroot start --rw $NEO4J_CONTAINER_NAME bash << EOF
        cd plugins
        wget https://github.com/neo4j/graph-data-science/releases/download/2.6.2/neo4j-graph-data-science-2.6.2.jar
        echo -e "dbms.security.procedures.unrestricted=gds.*" >> ../conf/neo4j.conf
        echo -e "dbms.security.procedures.allowlist=gds.*" >> ../conf/neo4j.conf
        exit
EOF

    # Copy data into ENROOT container
    cp -r $(ws_find $WORKSPACE_NAME)/data/raw_data $(ws_find $WORKSPACE_NAME)/containers/$NEO4J_CONTAINER_NAME/var/lib/neo4j

    # Change initial password
    enroot start --rw $NEO4J_CONTAINER_NAME bash << EOF
        bin/neo4j-admin set-initial-password $PASSWORD
EOF

    # Start database and run data loading script
    echo -e "\n[$(date +%T)] * Load database...\n"
    cp $CURRENT_DIR/load_data.cypher $(ws_find $WORKSPACE_NAME)/containers/$NEO4J_CONTAINER_NAME/var/lib/neo4j
    enroot start --rw $NEO4J_CONTAINER_NAME bash << EOF
        bin/neo4j start
        sleep 180
        cat load_data.cypher | bin/cypher-shell -u neo4j -p $PASSWORD
EOF

    echo -e "\n[$(date +%T)] * Done!\n"

fi