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
  ami                     = var.ami
  instance_type           = var.instance_type
  user_data               = data.template_file.user_data.rendered
  security_groups         = ["wesm"]
  key_name                = var.key_name
  vpc_security_group_ids  = ["sg-0d478e38195ba3d1d"]

  # root disk
  root_block_device {
    volume_size           = var.volume_size
    volume_type           = "gp2"
    encrypted             = true
    delete_on_termination = true
  }

  tags = {
    Name = var.instance_name
  }
}

resource "null_resource" "run_surface" {

    depends_on = [
      aws_instance.app_server
    ]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = "${file("../.ssh/wesm.pem")}"
      host        = aws_instance.app_server.public_dns
    }

    provisioner "local-exec" { 
      command = "aws ec2 wait instance-status-ok --region us-west-2 --instance-ids ${aws_instance.app_server.id}" 
      }

    provisioner "file" {
    source      = "../.creds"
    destination = "/home/ubuntu/.creds"
    }

    provisioner "remote-exec" {
    inline = [
      "mkdir -p /home/ubuntu/configs",
    ]
    }

    provisioner "file" {
    source      = "../configs/process-config.sh"
    destination = "/home/ubuntu/configs/process-config.sh"
    }

    provisioner "file" {
    source      = "../build.sh"
    destination = "/home/ubuntu/build.sh"
    }    

    provisioner "remote-exec" {
    inline = [
      "ls -a",
      "ls -a configs",
      "bash build.sh ${var.process}",
    ]
    }
}
