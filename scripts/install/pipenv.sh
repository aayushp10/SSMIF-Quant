#!/bin/bash

# required argument - relative to base path to folder with the Pipfile

# abort on errors
set -e

if [ -z "$1" ]; then
  echo "No source directory provided"
  exit 1
fi

BASEDIR=$(dirname $0)

cd "$BASEDIR/../../$1"

pipenv install --dev

mkdir -p ".mypy_cache"

cd - > /dev/null

exit 0
