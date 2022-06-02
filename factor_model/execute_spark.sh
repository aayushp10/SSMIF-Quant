#!/bin/bash

# execute script on spark cluster

# abort on errors
set -e

BASEDIR=$(dirname $0)

in_prod=false

if [[ $* == *--prod* ]]; then
  in_prod=true
  echo "in production"
else
  echo "not in production"
fi

docker_image="774311540350.dkr.ecr.us-east-1.amazonaws.com/ssmif-factor-model"
python_path="/app/envs/factor_model_env/bin/python"

if "$in_prod"; then
  deploy_mode="cluster"
  python_path="/app/envs/factor_model_env/bin/python"
  factor_model_source="s3a://factor-model-spark/dist.zip"
  spark_script="s3a://factor-model-spark/spark.py"
  master="yarn"
else
  deploy_mode="client"
  python_path="$BASEDIR/envs/factor_model_env/bin/python"
  factor_model_source="$BASEDIR/dist.zip"
  master="local"
  if ! [ -f "$factor_model_source" ]; then
    echo "$factor_model_source does not exist"
    exit 1
  fi
  spark_script="$BASEDIR/src/spark.py"
  if ! [ -f "$spark_script" ]; then
    echo "$spark_script does not exist"
    exit 1
  fi
fi

PYSPARK_PYTHON="$python_path"

spark-submit --master "$master" --deploy-mode "$deploy_mode" \
  --conf spark.executorEnv.JAVA_HOME=/usr \
  --conf spark.executorEnv.YARN_CONTAINER_RUNTIME_TYPE=docker \
  --conf spark.executorEnv.YARN_CONTAINER_RUNTIME_DOCKER_IMAGE="$docker_image" \
  --conf spark.executorEnv.PYSPARK_PYTHON="$python_path" \
  --conf spark.executorEnv.PYSPARK_DRIVER_PYTHON="$python_path" \
  --conf spark.yarn.appMasterEnv.JAVA_HOME=/usr \
  --conf spark.yarn.appMasterEnv.YARN_CONTAINER_RUNTIME_TYPE=docker \
  --conf spark.yarn.appMasterEnv.YARN_CONTAINER_RUNTIME_DOCKER_IMAGE="$docker_image" \
  --conf spark.yarn.appMasterEnv.PYSPARK_DRIVER_PYTHON="$python_path" \
  --conf spark.yarn.appMasterEnv.PYSPARK_PYTHON="$python_path" \
  --py-files "$factor_model_source" "$spark_script" "$@"
