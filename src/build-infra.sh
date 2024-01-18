#!/bin/bash

source .creds

################################################################################
# Help                                                                         #
################################################################################
Help()
{
   # Display Help
   echo "Arguments to run Terraform process"
   echo
   echo "Syntax: [-w|s|t|e|v|]"
   echo "options:"
   echo "w     Input workunit. Example: CA_NoCAL_Wildfires_B1_2018"
   echo "s     State the workunit. Example: California"
   echo "p     Process type. Options are [bcm, surfaces, solar, infra]"
   echo "e     EC2 name. Example: t2.micro"
   echo "v     EBS volume size for EC2. In GB. Example: 200"
   echo "t     Type of process: test or all. Options: [test, all]"
   echo "h     Print this Help."
   echo
}

while getopts "w:s:p:e:v:t:h" flag;
do
    case $flag in
        w) WORKUNIT=$OPTARG;;
        s) STATE=$OPTARG;;
        p) PROCESS=$OPTARG;;
        e) EC2=$OPTARG;;
        v) VOLUME_SIZE=$OPTARG;;
        t) TYPE=$OPTARG;;
        h) Help
           exit;;
        \?) # Invalid option
         echo "Error: Invalid option. See \"make tf-build-help\""
         exit;;
    esac
done

cp -r terraform terraform-${WORKUNIT}-${TYPE}

cd terraform-${WORKUNIT}-${TYPE}

export TF_VAR_instance_type="${EC2}"
export TF_VAR_volume_size="${VOLUME_SIZE}"
if [[ $TYPE == "test" ]]; then
        export TF_VAR_test="${TYPE}/"
        export TF_VAR_process_file="build-${PROCESS}-${TYPE}.sh"
    else
    export TF_VAR_process_file="build-${PROCESS}.sh"
fi
export TF_VAR_workunit=$WORKUNIT
export TF_VAR_state=$STATE

terraform init 

terraform apply -auto-approve

terraform validate

terraform destroy -auto-approve

cd ../

rm -rf terraform-${WORKUNIT}-${TYPE}

echo "DONE!"

exit