#!/bin/bash

set -e

# kubernetes is actually too expensive due to limitations with gpu acceleration and fargate
# see https://github.com/aws/containers-roadmap/issues/88
# when that issue gets resolved you can revisit this if you want
# the reason for using fargate was to avoid paying a lot for the cluster, but with spot instances
# and scale down it shouldn't be a problem anymore.

# note - you need to create a dedicated spark cluster for this to work.

# from https://docs.amazonaws.cn/emr/latest/EMR-on-EKS-DevelopmentGuide/setting-up.html

cluster_name="ssmif-eks"
namespace="spark"

eksctl create cluster -f cluster-config.yml

aws eks --region us-east-1 update-kubeconfig --name "$cluster_name"

# kubectl create -f ./namespace.json

eksctl create iamidentitymapping \
    --cluster "$cluster_name" \
    --namespace "$namespace" \
    --service-name "emr-containers"

aws eks describe-cluster --name "$cluster_name" --query "cluster.identity.oidc.issuer" --output text

aws emr-containers update-role-trust-policy \
    --cluster-name "$cluster_name" \
    --namespace "$namespace" \
    --role-name ssmif-eks-role

aws emr-containers create-virtual-cluster --cli-input-json file://./create_virtual_cluster.json

# from https://docs.amazonaws.cn/en_us/emr/latest/ManagementGuide/emr-studio-create-eks-cluster.html

aws emr-containers create-managed-endpoint \
    --type JUPYTER_ENTERPRISE_GATEWAY \
    --virtual-cluster-id wh64y0ytchaa18kwan44ci8h8 \
    --name spark \
    --execution-role-arn arn:aws:iam::774311540350:role/ssmif-eks-role \
    --release-label emr-6.2.0-latest \
    --certificate-arn arn:aws:acm:us-east-1:774311540350:certificate/28bc0e24-9c5a-4cb4-b069-09bce4e10927

# auth
kubectl apply -f eks-console-full-access.yaml

kubectl edit cm aws-auth -n kube-system

# output info
aws emr-containers list-managed-endpoints --virtual-cluster-id wh64y0ytchaa18kwan44ci8h8
aws emr-containers describe-managed-endpoint --id ker1wsay3f9z0 --virtual-cluster-id wh64y0ytchaa18kwan44ci8h8

# aws emr-containers start-job-run \
#     --virtual-cluster-id wh64y0ytchaa18kwan44ci8h8 \
#     --name test --execution-role-arn arn:aws:iam::774311540350:role/ssmif-eks-role \
#     --release-label emr-6.2.0-latest \
#     --job-driver '{"sparkSubmitJobDriver": {"entryPoint": "local:///usr/lib/spark/examples/src/main/python/pi.py","sparkSubmitParameters": "--conf spark.executor.instances=2 --conf spark.executor.memory=2G --conf spark.executor.cores=2 --conf spark.driver.cores=1"}}' 

# ssh into node
ssh -i ssmif-spark-eks.pem ec2-user@ip-address.ec2.internal # or public ip
