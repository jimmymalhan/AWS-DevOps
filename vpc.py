import boto3
import sys
import os



def conn_to_my_aws_resource(my_region):
    ec2_con_resource = boto3.resource('ec2', region_name=my_region)
    return ec2_con_resource

def conn_to_my_aws_client(my_region):
    ec2_con_client = boto3.client('ec2', region_name=my_region)
    return ec2_con_client

def vpc(ec2_con_resource, conn_to_my_aws_client):

    vpc = ec2_con_resource.create_vpc(CidrBlock='172.16.0.0/16')
    # we can assign a name to vpc, or any resource, by using tag
    vpc.create_tags(Tags=[{"Key": "Name", "Value": "vpc_name"}])
    vpc.wait_until_available()
    print(vpc.id)

    # enable public dns hostname, not enabled by default
    conn_to_my_aws_client.modify_vpc_attribute(VpcId = vpc.id ,EnableDnsSupport = { 'Value': True } )
    conn_to_my_aws_client.modify_vpc_attribute(VpcId = vpc.id ,EnableDnsHostnames = { 'Value': True } )
    
    # create then attach internet gateway
    internetGateway = ec2_con_resource.create_internet_gateway()
    vpc.attach_internet_gateway(InternetGatewayId=internetGateway.id)
    print(internetGateway.id)

    # create a route table and a public route
    routeTable = vpc.create_route_table()
    route = routeTable.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=internetGateway.id)
    print(routeTable.id)

    # create subnet
    subnet = ec2_con_resource.create_subnet(CidrBlock='192.168.1.0/24', VpcId=vpc.id)
    print(subnet.id)

    # associate the route table with the subnet
    routeTable.associate_with_subnet(SubnetId=subnet.id)

    # Create sec group
    sec_group = ec2_con_resource.create_security_group(
        GroupName='slice_0', Description='slice_0 sec group', VpcId=vpc.id)
    sec_group.authorize_ingress(
        CidrIp='0.0.0.0/0',
        IpProtocol='icmp',
        FromPort=-1,
        ToPort=-1
    )
    print(sec_group.id)

def main(): 
    my_region = "us-west-2"
    ec2_con_resource = conn_to_my_aws_resource(my_region)
    ec2_con_client = conn_to_my_aws_client(my_region)
    vpc(ec2_con_resource, ec2_con_client)

if __name__ == '__main__':
    main()
