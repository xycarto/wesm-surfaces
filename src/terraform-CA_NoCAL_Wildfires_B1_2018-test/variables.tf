variable "instance_name" {
  description = "Value of the Name Tag for the EC2 instance"
  type        = string
  default     = "wesm-surfaces-terraform"
}

variable "key_name" {
  description = "Key Pair to Use"
  type        = string
  default     = "wesm"
}

variable "ami" {
    type = string
    default = "ami-008fe2fc65df48dac"
}

variable "instance_type" {
    type = string
    default = "t2.micro"
}

variable "volume_size" {
    type = string
    default = "10"
}

variable "workunit" {
  type = string
  default = "empty"
}

variable "state" {
  type = string
  default = "empty"
}

variable "process_file" {
  type = string
  default = "empty"
}

variable "process" {
  type = string
  default = "empty"
}

variable "test_type" {
  type = string
  default = ""
}

variable "test" {
  type = string
  default = ""
}