#!/bin/bash

# takes 1 argument, the path to the directory of the node project relative
# to the root folder

# abort on errors
set -e

if [ -z "$1" ]; then
  echo "No source directory provided"
  exit 1
fi

BASEDIR=$(dirname $0)

cd "$BASEDIR/../../$1"

npx npm-check-updates -u
if [ -f yarn.lock ]; then
    echo "using yarn package manager"
    rm -f package-lock.json
    yarn install
else
    echo "using npm package manager"
    npm install
fi

cd - > /dev/null

exit 0
