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

# format files
autopep8 --in-place --recursive src

if ! [[ $* == *--skip-lint* ]]; then
  # lint files
  pylint src

  # check types
  mypy --install-types --non-interactive src
fi

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
spec_file_name="spec_$os_name.txt"

# save current environment to file
conda env export -p "$env_folder/$env_name" --no-builds | grep -v "^prefix: " | sed "/  - pip:/Q" | sed "s/^name: null$/name: $env_name/g" > "$env_folder/$env_file_name"
conda list --explicit > "$env_folder/$spec_file_name"

echo "done with precommit for $env_name"

conda deactivate

cd - > /dev/null

exit 0
