#!/bin/bash

# takes 1 argument, the path to the directory of the pyenv project relative
# to the root folder

# abort on errors
set -e

if [ -z "$1" ]; then
  echo "No main directory provided"
  exit 1
fi

BASEDIR=$(dirname $0)

cd "$BASEDIR/../../$1"

# update dependencies
pipenv run pipenv update

echo "done updating dependencies"

cd - > /dev/null

exit 0
