#!/bin/bash

source .creds

WORKUNIT=$1
STATE=$2

cp -r terraform terraform-${WORKUNIT}

cd terraform-${WORKUNIT}

export TF_VAR_instance_type="c5.2xlarge"
export TF_VAR_volume_size="20"
export TF_VAR_WORKUNIT=$WORKUNIT
export TF_VAR_STATE=$STATE

terraform init 

terraform apply -auto-approve

terraform validate

terraform destroy -auto-approve

cd ../

rm -rf terraform-${WORKUNIT}