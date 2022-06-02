#!/bin/bash

# abort on errors
set -e

BASEDIR=$(dirname $0)

rm -f $BASEDIR/dist.zip
$BASEDIR/../scripts/aws/build.sh factor_model --exclude-src

cd $BASEDIR/dist
zip -r ../dist.zip . *
cd -
