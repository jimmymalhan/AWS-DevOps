provider "aws" {
  region = "your_region"
  access_key = ""
  secret_key = ""
}

# # 1. Create vpc

resource "aws_vpc" "prod-vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "production"
  }
}

# # 2. Create Internet Gateway

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.prod-vpc.id # aws_vpc.foo.id
}
# 3. Create Custom Route Table

resource "aws_route_table" "prod-route-table" {
  vpc_id = aws_vpc.prod-vpc.id #aws_vpc.foo.id

  route {
    cidr_block = "0.0.0.0/0" # sending all ip4 traffic
    gateway_id = aws_internet_gateway.gw.id # aws_internet_gateway.foo.id
  }

  route {
    ipv6_cidr_block = "::/0"
    gateway_id      = aws_internet_gateway.gw.id # aws_egress_only_internet_gateway.foo.id
  }

  tags = {
    Name = "Prod"
  }
}

variable "subnet_prefix" {
  description = "cidr block for the subnet"
  # default = "10.0.66.0/24" # if the value of the variable is not assigned then it uses default value
  type = list # can be used any for boolean,list etc..
}

# 4. Create a Subnet 

resource "aws_subnet" "subnet-1" {
  vpc_id            = aws_vpc.prod-vpc.id # aws_vpc.foo.id
  cidr_block        = var.subnet_prefix[0].cidr_block # first object in a list from variable file - "10.0.1.0/24"
  availability_zone = "us-west-2a" # important to hardcode it

  tags = {
    Name = var.subnet_prefix[0].name
  }
}

resource "aws_subnet" "subnet-2" {
  vpc_id            = aws_vpc.prod-vpc.id # aws_vpc.foo.id
  cidr_block        = var.subnet_prefix[1].cidr_block # 2nd object in a list from variable file - "10.0.2.0/24"
  availability_zone = "us-west-2a" # important to hardcode it

  tags = {
    Name = var.subnet_prefix[0].name
  }
}

# 5. Associate subnet with Route Table
resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.subnet-1.id # aws_subnet.foo.id
  route_table_id = aws_route_table.prod-route-table.id
}

# 6. Create Security Group to allow port 22,80,443
resource "aws_security_group" "allow_web" {
  name        = "allow_web_traffic"
  description = "Allow Web inbound traffic"
  vpc_id      = aws_vpc.prod-vpc.id

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    # ipv6_cidr_blocks = [aws_vpc.main.ipv6_cidr_block]
  }
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1" # -1 -> any protocol 
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_web"
  }
}

# 7. Create a network interface with an ip in the subnet that was created in step 4

resource "aws_network_interface" "web-server-nic" {
  subnet_id       = aws_subnet.subnet-1.id # copy from step 4 aws_subnet.foo.id
  private_ips     = ["10.0.1.50"] # ip address within your subnet
  security_groups = [aws_security_group.allow_web.id] # copied from step 6

}
# 8. Assign an elastic IP to the network interface created in step 7
resource "aws_eip" "one" { # "aws_eip" "foo"
  vpc                       = true
  network_interface         = aws_network_interface.web-server-nic.id # copy from step 7
  associate_with_private_ip = "10.0.1.50"
  depends_on                = [aws_internet_gateway.gw] # EIP may require IGW to exist prior to association # need to pass it in as list
}

output "server_public_ip" {
  value = aws_eip.one.public_ip
}

# 9. Create Ubuntu server and install/enable apache2

resource "aws_instance" "web-server-instance" {
  ami               = "ami-02701bcdc5509e57b"
  instance_type     = "t2.micro"
  availability_zone = "us-west-2a" 
  key_name          = "main- key"

  network_interface {
    device_index         = 0
    network_interface_id = aws_network_interface.web-server-nic.id # copy from step 7
  }

  user_data = <<-EOF
                #!/bin/bash
                sudo apt update -y
                sudo apt install apache2 -y
                sudo systemctl start apache2
                sudo bash -c 'echo your very first web server > /var/www/html/index.html'
                EOF
  tags = {
    Name = "web-server"
  }
}

output "server_private_ip" {
  value = aws_instance.web-server-instance.private_ip # value = aws_instance.<server_name_created>.<required_diplay_resource>

}

output "server_id" {
  value = aws_instance.web-server-instance.id
}


# resource "<provider>_<resource_type>" "name" {
#     config options.....
#     key = "value"
#     key2 = "another value"
# }