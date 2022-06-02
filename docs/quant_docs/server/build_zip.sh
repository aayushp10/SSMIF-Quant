#!/bin/bash

# abort on errors
set -e

output="dist.zip"

temp_folder="temp"

yarn clean

yarn build

rm -rf "$output" "$temp_folder"
mkdir "$temp_folder"

cp -R lib "$temp_folder"
cp package.json swagger.yml .npmrc "$temp_folder"
cp -R .platform "$temp_folder"
cp -R .ebextensions "$temp_folder"

# copy folder with static files
cp -R static "$temp_folder"
cp -R public "$temp_folder"

cd "$temp_folder"
zip -r "$output" * .[^.]*
mv "$output" ..
cd -
rm -rf "$temp_folder"
