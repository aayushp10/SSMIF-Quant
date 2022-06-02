#!/bin/bash

set -e

conda env export --no-builds | grep -v "^prefix: " > environment.yml

