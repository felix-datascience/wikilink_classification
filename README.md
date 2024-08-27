# Code Repository for the Master Thesis "Classifying Wikilinks to Refine the DBpedia Knowledge Graph"

The code repository contains three directories with scripts that are used to process and analyze data and train and evaluate triple classification models. The directories are:

- *neo4j_scriptes*: contains scripts that are used for setting up a neo4j database, loading, processing and exporting data in it and performing a data analysis of the knowledge graph
- *data_preprocessing*: contains data analyses that are performed as preparation for the data pre-processing as well as code that is used for processing the datasets that are exported from the neo4j database to obtain training, validation and testing datasets
- *pykeen*: contains scripts for training and evaluating triple classification models and for building an ontology-based relation filter

The contents of these three folders are explained in more detail below.


## neo4j_scripts

### Neo4j database setup

The neo4j setup script (*neo4j_setup.sh* & *load_data.cypher*) is intended to be used on the BWUniCluster2.0. It creates a workspace in which a container with a neo4j database is set up. The script also loads the data into the database. Use the following command to start it with SLURM on the BWCluster2.0. A password for the neo4j database has to be specified with the *-p* argument.

```
sbatch -p single -n 1 -t 1440 --mem=16000 ./neo4j_setup.sh -p <password>
```

Receiving status updates is possible by adding `--mail-type` and `--mail-user` arguments.

```
sbatch -p single -n 1 -t 1440 --mem=16000 --mail-type=ALL --mail-user=<mail_address> ./neo4j_setup.sh -p <password>
```

The status of the job can be checked with the following command.

```
squeue -l
```

After the setup, it might be necessary to update the memory configuration in the neo4j.conf file (in the conf directory), depending on the hardware configuration that is used. I used the following setting with the hardware configuration defined in the SLURM commands above.

```
server.memory.heap.initial_size=100g
server.memory.heap.max_size=100g
server.memory.pagecache.size=20g
```

For more information visit the [memory configuration section of the neo4j documentation](https://neo4j.com/docs/operations-manual/current/performance/memory-configuration/).

### Augmenting nodes and edges in the database

The cypher queries in *augment_graph_mutual_wikilinks.cypher* and *augment_graph_types_and_degree_centrality.cypher* augment the nodes and edges in the database with further information about the entities' numbers of mutual wikilinks with other entities, their numbers of types and their degree centralities. Use the following command to start the graph augmentation:

```
sbatch -p single -n 1 -t 1440 --mem=16000 ./neo4j_augment_graph.sh -p <password>
```

### Exporting data

The cypher queries in *export_data.cypher* are used to export data from the neo4j database. The datasets that are exported are:

- *mutual_wikilinks_properties_both_sides.csv*: triples with properties that connect entities that are mutually linked with wikilinks (where both entities appear as subject)
- *mutual_wikilinks_properties_one_side.csv*: triples with properties that connect entities that are mutually linked with wikilinks (where only one entity appears as subject)
- *mutual_wikilinks_no_properties.csv*: triples with entity pairs that are mutually linked with wikilinks but are not connected with any other property
- *remaining_triples.csv*: triples with all other pairs that are connected with properties but not with mutual wikilinks
- *type_triples.csv*: triples with type statements
- *property_counts.csv*: count of appearance of all relations 

Export the datasets with this command:

```
sbatch -p single -n 1 -t 1440 --mem=16000 ./neo4j_augment_graph.sh -p <password>
```

### Sampling entities

The cypher query in *sample_entities.cypher* samples 50,000 entities from the graph. This dataset is used in the *analyze_entitites.ipynb* notebook to find reasons for the divergence of the number of entities in the knowledge graph from the number of Wikipedia pages. Run the sampling script with the following command:

```
sbatch -p single -n 1 -t 1440 --mem=16000 ./neo4j_augment_graph.sh -p <password>
```


## data_preprocessing

### Data analyses

The notebook *neo4j_analysis_visualizations.ipynb* contains tables and plots that visualize the results of the neo4j data analysis of the whole knowledge graph. The notebooks *analyze_entities.ipynb*, *analyze_relations.ipynb* contain further analyses of the exported datasets. *analyze_entitites.ipynb* analyzes the entities in the datasets with regard to the issue of the diverging numbers of entities in the graph and pages on Wikipedia. *analyze_relations.ipynb* analyzes the relations in the graph and their numbers of appearances in the different exported datasets.

### Data pre-processing

The data pre-processing is performed in the *data_preprocessing.ipynb* notebook. The data preprocessing is built on the knowledge gained in the different data analyses. The functions that are used during pre-processing are kept in the utility file *data_preprocessing_utility.py*.


## pykeen

### Ontology-based relation filtering

In the *domain_range_filtering_analysis.ipynb* notebook, an ontology-based relation filter is built. The notebook also contains analyses that concern relation filtering with the implemented solution. The utility file *post_processing_utility.py* contains functions that are used for relation filtering.

### Knowledge graph embedding models

Each of the knowledge graph embedding models that are shown in the thesis is set up in a different python script. The files are named like the models in the thesis, with the exception of the file endings. Models with negative sampling of subject and object have files ending with *_ht.py* and models with additional negative sampling of properties have files ending with *_hrt.py*. The file *pykeen_extensions.py* contains extensions of the pykeen source code that allow building models with the configurations that are shown in the thesis. The individual models' python scripts are used to train the models and can be run as any other python script. If they are run on the BWUniCluster2.0, the file run_python_scrip.sh can be used to submit them to the SLURM queing system. Note, that the script requires a virtual environment with the pykeen package to be set up under the name *pykeen_env*. The following command is used to train a model on BWCluster2.0. Replace *<model_name>* with the name of model that is supposed to be trained, e.g. *complEx_ruffinelli_hrt*.

```
sbatch -p gpu_4_a100 -n 1 -t 2880 --mem=80000 --gres=gpu:1 run_python_script.sh -f <model_name>.py -m <model_name>
```

Some models need training for more than 48 hours. In that case, use the same command to train them further.

### Triple classification

To build triple classification models, the trained embedding models are used to generate scores for triples and relation-dependent thresholds are calculated to perform a binary classification that predicts the authenticity of hypothetical triples.

The scripts *score_properties.py* and *score_properties_makeshift.py* are used to score properties of entity pairs in the validation and testing datasets with the trained knowledge graph embedding models. *score_properties.py* is used to score properties with models that are trained for 10 epochs, as specified. As some of the models could not be trained, due to long waiting times on BWUniCluster2.0, there are models which are trained for less than 10 epochs. As they can only be used from their checkpoint file instead of the results folder in which fully trained models are stored, different code is necessary to use them. Both scoring scripts use functions that are defined in the *prediction_and_evaluation_utility.py* file. To score properties with a fully trained model use this command:

```
sbatch -p gpu_4_a100 -n 1 -t 2880 --mem=80000 --gres=gpu:1 run_python_script.sh -f score_properties.py -m <model_name>
```

To score properties with a model that is not fully trained, use this command:

```
sbatch -p gpu_4_a100 -n 1 -t 2880 --mem=80000 --gres=gpu:1 run_python_script.sh -f score_properties_makeshift.py -m <model_name>
```

After generating scores, it is necessary to calculate relation-specific thresholds for the triple classification models. The *calculate_thresholds.py* script is used for this task. The functionality is implemented in the *prediction_and_evaluation_utility.py* file. Use the following command to calculate thresholds for a model that was already used to score the validation and testing datasets.

```
sbatch -p single -n 1 -t 120 --mem=32000 run_python_script.sh -f calculate_thresholds.py -m <model_name>
```

When scores and thresholds are available for a model, predictions can be made with the *classify_triples.py* script. The script also performs evaluations of the predictions on the validation and testing datasets. It utilizes functions that are defined in the *prediction_and_evaluation_utility.py* file. Use the following command to perform a triple classification on the validation and testing datasets.

```
sbatch -p single -n 1 -t 120 --mem=32000 run_python_script.sh -f classify_triples.py -m <model_name>
```

### Evaluation

The triple classifications of all models are evaluated in the *evaluation.ipynb* notebook. The notebook uses the evaluation datasets that are created by the *classify_triples.py* script.