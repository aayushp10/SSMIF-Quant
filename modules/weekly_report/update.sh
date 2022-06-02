#!/bin/bash

# abort on errors
set -e

BASEDIR=$(dirname $0)

$BASEDIR/../../scripts/update/conda.sh modules/weekly_report
