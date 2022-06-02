#!/bin/bash

# required argument - relative to base path to folder with the project to build

# abort on errors
set -e

if [ -z "$1" ]; then
  echo "No source directory provided"
  exit 1
fi

BASEDIR=$(dirname $0)

cd "$BASEDIR/../.."

echo "files in source directory:"
ls "$1"

source_folder="src"

source_dir="$1"/"$source_folder"

# delete gitignored files
cd "$source_dir"
git clean -xdf
cd - > /dev/null

dist_folder="$1"/"dist"

rm -rf "$dist_folder"
mkdir "$dist_folder"

# env
env_file_name=".global.env"
cp "$1"/"$env_file_name" "$dist_folder"/.env

if [[ $* == *--exclude-src* ]]; then
  cp -LR "$source_dir/." "$dist_folder"
else
  cp -LR "$source_dir" "$dist_folder"
fi

cd - > /dev/null

exit 0
