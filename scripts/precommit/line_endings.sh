#!/bin/bash

# takes no arguments

# don't use set -e, otherwise the grep command will fail

BASEDIR=$(dirname $0)

cd "$BASEDIR/../.."

line_endings_files=$(grep -R -I -U -P "\r$" \
  --exclude-dir={.git,node_modules,.gradle,.cache,build,dist,data,venv,*_env,tmp} .)

num_line_endings_files=$(echo -n "$line_endings_files" | grep -c '^')

if [ $num_line_endings_files -ne 0 ]; then
  echo "source file lines that have dos line endings: $num_line_endings_files"
  printf '%s\n' "$line_endings_files"
  exit 1
fi

cd - > /dev/null

exit 0
