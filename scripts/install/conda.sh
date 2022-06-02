#!/bin/bash

# required argument - relative to base path to folder with the conda project

# abort on errors
set -e

if [ -z "$1" ]; then
  echo "No source directory provided"
  exit 1
fi

BASEDIR=$(dirname $0)

cd "$BASEDIR/../../$1/envs"

env_name=$(grep 'name:' environment_linux.yml | cut -d ' ' -f 2)

rm -rf "./$env_name"

if [ "$(uname)" == "Darwin" ]; then
  os_name="mac"
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
  os_name="linux"
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
  os_name="win32"
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
  os_name="win64"
fi

env_file_name="environment_$os_name.yml"

conda env create --prefix "./$env_name" --file "$env_file_name"

source $(conda info --base)/etc/profile.d/conda.sh

conda activate "./$env_name"

pip install --force-reinstall --no-cache-dir -r ./requirements.txt

cd .. > /dev/null
mypy src || true # initialize mypy
mkdir -p ".mypy_cache"

echo "done creating environment $env_name"

conda deactivate

cd - > /dev/null

exit 0
