import os
import sys
import boto3
import time

def con_to_aws():
    client = boto3.client('ecs')
    return client

def describe_clusters(client):
    response = client.describe_clusters(
    clusters=[
        'arn:aws:ecs:us-west-2:111455572758:cluster/Production-Master'
        ]
    )
    print(response)
    pass
    return

def describe_services(client):
    response = client.describe_services(
        cluster='arn:aws:ecs:us-west-2:111455572758:cluster/Production-Master',
        services=[
            'arn:aws:ecs:us-west-2:111455572758:service/clinicaltrials_dataservice-flask'
        ]
    )
    print(response)
    pass
    return

def list_container_instances(client):
    response = client.list_container_instances(
        cluster='arn:aws:ecs:us-west-2:111455572758:cluster/Production-Master',
        status='ACTIVE'
    )
    for arns in response['containerInstanceArns']:
        print (arns)
    a = arns
    pass
    return response

def update_container_instances_state(client):
    response = client.update_container_instances_state(
        cluster='arn:aws:ecs:us-west-2:111455572758:cluster/Production-Master',
        containerInstances=['arn:aws:ecs:us-west-2:111455572758:container-instance/edceb8b8-7b8e-4339-87cd-51aedd97103d',
        ],
        status='DRAINING'
    )
    print(response)
    pass
    return

def list_services(client):
    response = client.list_services(
        cluster='arn:aws:ecs:us-west-2:111455572758:cluster/Production-Master',
        launchType='EC2',
        schedulingStrategy='REPLICA'
    )
    print(response)    
    pass
    return

def describe_target_groups(client, **kwargs):
    response = client.describe_target_groups(
        LoadBalancerArn='arn:aws:elasticloadbalancing:us-west-2:111455572758:loadbalancer/app/CT-ELB/88f58916fd29e72d',
        TargetGroupsArns=['arn:aws:elasticloadbalancing:us-west-2:111455572758:targetgroup/DS-Ports-Worker/9fd6ba8d863dd65e',
        ]
    )
    print(response)
    pass
    return

def update_service(client, **kwargs):
    response = client.update_service(
        cluster='arn:aws:ecs:us-west-2:111455572758:cluster/Production-Master',
        service='arn:aws:ecs:us-west-2:111455572758:service/clinicaltrials_dataservice-flask',
        desiredCount=0,
    )
    print(response)
    pass
    return

if __name__ == '__main__':
    #os.system('cls')
    #client = boto3.client('ecs')
    client = con_to_aws()
    #describe_clusters(client)
    #describe_services(client)
    list_container_instances(client) # use
    #update_container_instances_state(client) #draining the instance
    #list_services(client) #listing all the services
    #update_service(client)
    

