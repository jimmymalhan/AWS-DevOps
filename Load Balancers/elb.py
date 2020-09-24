import boto3, os, sys
import botocore.session
from botocore.exceptions import ClientError

def con_to_elb():
    client_elb = boto3.client('elbv2')
    return client_elb

def con_to_sss():
    client_sss = boto3.client('s3')
    return client_sss

def describe_load_balancers(client_elb, **kwargs):
    try:
        response = client_elb.describe_load_balancers(
            LoadBalancerArns=[
            ],
        )
        for elb in response['LoadBalancers']:
            result = elb['LoadBalancerArn']
            for selected_elb in result.split():
                if 'CT-ELB' in selected_elb:
                    return selected_elb
    except botocore.exceptions.ClientError as error:
        raise error

def bucket_policy(client_sss):
    try:
        response = client_sss.get_bucket_policy(
        Bucket='medqia-testing-bucket',
        )
    except botocore.exceptions.ClientError as error:
        raise error

def modify_load_balancer_attributes(client_elb, ct_arn, **kwargs):
    try:
        response = client_elb.modify_load_balancer_attributes(
            LoadBalancerArn=ct_arn,
            Attributes=[
                {
                    'Key': 'deletion_protection.enabled',
                    'Value': 'true',
                },
                {
                    'Key': 'access_logs.s3.enabled',
                    'Value': 'true',
                },
                {
                    'Key': 'access_logs.s3.bucket',
                    'Value': 'medqiacloudtrail-logs',
                },
                {
                    'Key': 'access_logs.s3.prefix',
                    'Value': 'ct_elb_logs',
                },
            ]
        )
    except botocore.exceptions.ClientError as error:
        raise error
    except botocore.exceptions.ParamValidationError as error:
        raise ValueError('The parameters you provided are incorrect: {}'.format(error))
    except botocore.exceptions.InvalidConfigurationRequestException as error:
        raise ValueError('The parameters you provided are incorrect: {}'.format(error))
        return response
    except ClientError as error:
        if error.response['Error'] == 'ElasticLoadBalancingv2.Client.exceptions.InvalidConfigurationRequestException':
            print('ELB: %s, InvalidConfigurationRequestException' % (response['ResponseMetadata']))
        else:
            print("ELB: %s, unexpected error: %s", e)

if __name__ == '__main__':
    try:
        client_elb = con_to_elb()
        client_sss = con_to_sss()
        bucket_policy(client_sss)
        put_bucket_policy(client_sss)
        ct_arn = describe_load_balancers(client_elb)
        modify_load_balancer_attributes(client_elb, ct_arn)
    except Exception as e:
        sys.exit(1)