#!/bin/bash

set -e

aws ecs create-service --cluster ssmif-ecs --cli-input-json file://ssmif-ecs-service.json
