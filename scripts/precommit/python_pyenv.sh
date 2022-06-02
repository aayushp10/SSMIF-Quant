#!/bin/bash

# takes 1 argument, the path to the directory of the pyenv project relative
# to the root folder

# abort on errors
set -e

if [ -z "$1" ]; then
  echo "No main directory provided"
  exit 1
fi

if [ -z "$2" ]; then
  echo "No source directory provided"
  exit 1
fi

BASEDIR=$(dirname $0)

cd "$BASEDIR/../../$1"

# sync dependencies first
pipenv run pipenv-setup sync

# format files
pipenv run autopep8 --in-place --recursive .

if ! [[ $* == *--skip-lint* ]]; then
  # lint files
  pipenv run pylint "$2"
    
  # check types
  pipenv run mypy --install-types --non-interactive "$2"
fi

echo "done with precommit for $2"

cd - > /dev/null

exit 0
