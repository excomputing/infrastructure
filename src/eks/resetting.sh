#!/bin/bash

: << 'comment'
For resetting kubeconfig details.

References:
bash conditional expressions -> https://www.gnu.org/software/bash/manual/html_node/Bash-Conditional-Expressions.html

Parameters
  $1: arn:aws:eks:{region.code}:{account.identifier}:cluster/{cluster.name} -> old
  $2: cluster name -> latest
  $3: region code
comment


# old
kubectl config view

kubectl config delete-cluster "$1"
kubectl config delete-context "$1"
kubectl config delete-user "$1"


# latest
if [ -z "$2" ]; then
  echo "skipping update-kubeconfig"
else
  aws eks update-kubeconfig --region "$3" --name "$2"
  kubectl get svc
fi
