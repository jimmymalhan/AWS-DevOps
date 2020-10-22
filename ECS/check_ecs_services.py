import boto3,os,sys
import botocore.session

def con_to_aws():
    client = boto3.client('ecs')
    return client

def list_clusters(client, **kwargs):
    response = client.list_clusters(
        maxResults=10
    )
    my_cluster_lookup = 'enter_your_cluster_name'
    for clusters in response['clusterArns']:
        selected_cluster = my_cluster_lookup 
        # print(selected_cluster)
        break
    return response

def describe_clusters(client, **kwargs):
    response = client.describe_clusters(
        clusters=[
            'enter_your_cluster_name',
            ],
            include=[
            'ATTACHMENTS',
            'SETTINGS',
            'STATISTICS', 
            'TAGS',
            ]
        )
    for cluster in response['clusters']:
        print("Cluster: " , (cluster['clusterName']))
        print("Registered Instance: " , (cluster['registeredContainerInstancesCount']))
        print("Registered TasksCount: " , (cluster['runningTasksCount']))
        print("PendingTasksCount: " , (cluster['pendingTasksCount']))
        print("ActiveServicesCount: " , (cluster['activeServicesCount']))
        return response


def list_services(client, production_cluster,  **kwargs):
    response = client.list_services(
        cluster=('enter_your_cluster_name'),
        launchType='EC2',
        maxResults=30,
        )
    for services in response['serviceArns']:
        print(services)
    return response

if __name__ == '__main__':
    try :
        os.system('cls')
        client = con_to_aws()
        production_cluster = list_clusters(client)
        describe_clusters(client)
        list_services(client, production_cluster)
    except Exception as e:
        print (e)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ServerException':
            print("The Server Exception raised error due to:", e)
        elif e.response['Error']['Code'] == 'ClientException':
            print("The Client Exception raised error due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
        elif e.response['Error']['Code'] == 'ClusterNotFoundException':
            print("The Cluster Not Found Exception raised error due to:", e)
        sys.exit(1)
        print(sys.exit(1))