#!/bin/bash

source .creds
source configs/process-config.env

PROCESS=$1

## Set TF VARS
export TF_VAR_instance_type="${EC2}"
export TF_VAR_volume_size="${VOLUME_SIZE}"
export TF_VAR_process=$PROCESS
export TF_VAR_workunit=$WORKUNIT
export TF_VAR_state=$STATE
export TF_VAR_test_type=$TYPE
export TF_VAR_location=$LOCATION

## Process Location: Local or Remote
if [[ $LOCATION == "local" ]]; then
    echo "Testing Locally..."
    bash build.sh ${PROCESS}
elif [[ $LOCATION == "remote" ]]; then
    tf_dir=terraform-${WORKUNIT}-${TYPE}-${PROCESS}
    cp -r terraform $tf_dir
    cd $tf_dir
    terraform init
    terraform apply -auto-approve
    terraform validate
    terraform destroy -auto-approve
    cd ../
    rm -rf $tf_dir
else
    echo "A location where to process, 'local' or 'remote', must be set"
fi

echo "DONE!"

# exit