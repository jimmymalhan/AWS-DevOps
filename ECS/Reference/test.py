import boto3
from boto3 import client


def con_to_aws():
    client = boto3.client('elbv2')
    return client

def deregister_targets(client):
    response = client.deregister_targets(
        TargetGroupArn='arn:aws:elasticloadbalancing:us-west-2:111455572758:targetgroup/DS-Ports-Worker/9fd6ba8d863dd65e',
        Targets=[
            {
                'Id': 'i-038e7da1e29ed0ed1',
            },
        ],
    )

    print(response)



if __name__ == '__main__':
    client = con_to_aws()
    deregister_targets(client)
    