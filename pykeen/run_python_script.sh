#!/bin/bash

# Run a python script insede the pykeen virtual environment with this script.

# read flags
while getopts f: flag                                                           
do                                                                              
    case "${flag}" in                                                           
        f) PYTHON_SCRIPT=${OPTARG};;                                                 
    esac                                                                        
done   
if [[ $PYTHON_SCRIPT == "" ]]; then
    echo "\nERROR: No filepath to a python script specified (use -f argument)\n"
    exit 1
fi

# activate virtual environment
source ~/pykeen_env/bin/activate

# run python script
python $PYTHON_SCRIPT