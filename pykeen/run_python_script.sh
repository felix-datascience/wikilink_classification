#!/bin/bash

# Run a python script inside the pykeen virtual environment with this script.

# read flags
while getopts f:m: flag                                                           
do                                                                              
    case "${flag}" in                                                           
        f) PYTHON_SCRIPT=${OPTARG};;                                                 
        m) MODEL_NAME=${OPTARG};;                                                 
    esac                                                                        
done   
if [[ $PYTHON_SCRIPT == "" ]]; then
    echo "\nERROR: No filepath to a python script specified (use -f argument)\n"
    exit 1
fi
if [[ $MODEL_NAME == "" ]]; then
    echo "\nERROR: No model name specified (use -m argument)\n"
    exit 1
fi

# activate virtual environment
source ~/pykeen_env/bin/activate

# run python script and pass model name as argument
python $PYTHON_SCRIPT $MODEL_NAME