resource "aws_instance" "web" {
  ami           = "ami-001628438d5d7d524"
  instance_type = "t3.micro"

  tags = {
    Name = "YelloWord"
  }
}