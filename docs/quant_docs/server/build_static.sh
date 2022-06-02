#!/bin/bash

# abort on errors
set -e

out_dir="static"

rm -rf "$out_dir"

cd ../frontend

yarn clean
yarn build

cd -

cp -R ../frontend/build "$out_dir"
