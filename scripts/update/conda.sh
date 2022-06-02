#!/bin/bash

# takes 1 argument, the path to the directory of the conda project relative
# to the root folder

# abort on errors
set -e

if [ -z "$1" ]; then
  echo "No source directory provided"
  exit 1
fi

BASEDIR=$(dirname $0)

cd "$BASEDIR/../../$1"

source $(conda info --base)/etc/profile.d/conda.sh

env_folder="envs"

env_name=$(grep 'name:' $env_folder/environment_linux.yml | cut -d ' ' -f 2)

echo "using env \"$env_name\""

conda activate "$env_folder/$env_name"

conda update --all

echo "done updating env \"$env_name\""

conda deactivate

./precommit.sh

cd - > /dev/null

exit 0
