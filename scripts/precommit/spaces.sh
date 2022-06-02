#!/bin/bash

# takes no arguments

# don't use set -e, otherwise the grep command will fail

BASEDIR=$(dirname $0)

cd "$BASEDIR/../.."

tab_files=$(grep -R -I -n -P "\t" \
  --exclude-dir={.git,node_modules,.gradle,.cache,build,dist,static,dist_swagger,data,.pytest_cache,venv,.terraform,*_env,tmp} \
  --exclude={.SRCINFO,.gitmodules,*.mod,makefile,.classpath,.project,swagger.yml,*.jar,*.go,*.svg} .)

num_tab_files=$(echo -n "$tab_files" | grep -c '^')


if [ $num_tab_files -ne 0 ]; then
  echo "source file lines that have tabs: $num_tab_files"
  printf '%s\n' "$tab_files"
  exit 1
fi

cd - > /dev/null

exit 0
