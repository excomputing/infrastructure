#!/bin/bash

: << 'comment'
Open ID Connector -> https://openid.net
grep -> https://www.man7.org/linux/man-pages/man1/grep.1.html
bash conditional expressions -> https://www.gnu.org/software/bash/manual/html_node/Bash-Conditional-Expressions.html

Parameters
  * $1: cluster name
comment

# Cluster name
cluster_name=$1

# Determining the OIDC issuer ID for a cluster in question.
oidc_id=$(aws eks describe-cluster --name "$cluster_name" --query "cluster.identity.oidc.issuer" --output text | cut -d '/' -f 5)
echo "$oidc_id"

# Is an IAM OIDC provider, with the cluster’s issuer ID, already associated with the project's cloud account?
# aws iam list-open-id-connect-providers | grep "$oidc_id" | cut -d "/" -f4
code=$(aws iam list-open-id-connect-providers | grep -o "$oidc_id")
echo "$code"

# If not
if [ -z "$code" ]; then
  eksctl utils associate-iam-oidc-provider --cluster "$cluster_name" --approve
else
  echo "IAM OIDC Code: ${code}"
fi
