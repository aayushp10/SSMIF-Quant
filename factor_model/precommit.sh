#!/bin/bash

# abort on errors
set -e

BASEDIR=$(dirname $0)

$BASEDIR/../scripts/precommit/python_conda.sh factor_model --skip-lint
