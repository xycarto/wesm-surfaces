#!/bin/bash

source .creds

WORKUNIT=$1
STATE=$2
TYPE=$3
EC2=$4
VOLUME_SIZE=$5

cp -r terraform terraform-${WORKUNIT}-${TYPE}

cd terraform-${WORKUNIT}-${TYPE}

export TF_VAR_instance_type="${EC2}"
export TF_VAR_volume_size="${VOLUME_SIZE}"
export TF_VAR_process_file="build-${TYPE}.sh"
export TF_VAR_WORKUNIT=$WORKUNIT
export TF_VAR_STATE=$STATE

echo ${TF_VAR_instance_type}
echo ${TF_VAR_volume_size}
echo ${TF_VAR_process_file}
echo ${TF_VAR_WORKUNIT}
echo ${TF_VAR_STATE}

# terraform init 

# terraform apply -auto-approve

# terraform validate

# terraform destroy -auto-approve

# cd ../

rm -rf terraform-${WORKUNIT}-${TYPE}