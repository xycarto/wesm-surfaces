terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-west-2"
}

data "template_file" "user_data" {
  template = file("../cloud-init/cloud-init.yml")
}

resource "aws_instance" "app_server" {
  ami                     = "ami-0fcf52bcf5db7b003"
  instance_type           = "t2.xlarge"
  user_data               = data.template_file.user_data.rendered
  security_groups         = ["wesm"]
  key_name                = var.key_name
  vpc_security_group_ids  = ["sg-0d478e38195ba3d1d"]

  # root disk
  root_block_device {
    volume_size           = "40"
    volume_type           = "gp2"
    encrypted             = true
    delete_on_termination = true
  }

  tags = {
    Name = var.instance_name
  }
}