#!/bin/bash

# abort on errors
set -e

# from https://askubuntu.com/a/145017
dig +short myip.opendns.com @resolver1.opendns.com

exit 0
