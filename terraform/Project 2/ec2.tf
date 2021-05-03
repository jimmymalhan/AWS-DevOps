terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

resource "aws_instance" "web" {
  ami           = "ami-001628438d5d7d524"
  instance_type = "t3.micro"

  tags = {
    Name = "YelloWord"
  }
}