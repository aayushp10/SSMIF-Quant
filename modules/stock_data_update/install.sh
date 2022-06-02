#!/bin/bash

# abort on errors
set -e

BASEDIR=$(dirname $0)

$BASEDIR/../../scripts/install/conda.sh modules/stock_data_update
