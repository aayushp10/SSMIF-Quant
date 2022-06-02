#!/bin/bash

# abort on errors
set -e

BASEDIR=$(dirname $0)

$BASEDIR/../../scripts/precommit/python_conda.sh modules/stop_loss_update
