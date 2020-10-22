import boto3,os,sys
import botocore.session
from botocore.exceptions import ClientError

def con_to_aws():
    client = boto3.client('ecs')
    return client

def list_services(client, **kwargs):
    response = client.list_services(
        cluster=('arn:aws:ecs:us-west-2:111455572758:cluster/Production-Master'),
        launchType='EC2',
        maxResults=50,
        )
    for all_services in response['serviceArns']:
        if 'flask' in all_services:
            flask_services = all_services
            print(flask_services)
            return all_services


def update_service(client, a, **kwargs):
    # print(a)
    response = client.update_service(
        cluster='arn:aws:ecs:us-west-2:111455572758:cluster/Production-Master',
        service='arn:aws:ecs:us-west-2:111455572758:service/clinicaltrials_dataservice-flask',
        desiredCount=0,
        deploymentConfiguration={
        'maximumPercent': 100,
        'minimumHealthyPercent': 0},
        forceNewDeployment=True,
        healthCheckGracePeriodSeconds=5000000
    )
    # print(response)
    return response

if __name__ == '__main__':
    try :
        os.system('cls')
        client = con_to_aws()
        a = list_services(client)
        update_service(client, a)
    except Exception as e:
        print (e)
