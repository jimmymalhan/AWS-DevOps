import csv
import boto3
from boto3.session import Session
import json

session = boto3.Session(profile_name='default')

def read_from_csv():
    resources = []
    with open('Config_resource.csv', newline='') as csvfile:
        reader_csv = csv.DictReader(csvfile)
        for row in reader_csv:
            if type(row) == list:
                removeNestings(row)
            else:
                resources.append(row)
    return resources

def tag_resource(session):
    reader = read_from_csv()
    for resources in reader:
        client = boto3.client('resourcegroupstaggingapi', region_name=resources['Region'])
        resources_arn = resources['ResourceARNList']
        key_list = list(resources.keys())
        val_list = list(resources.values()) 
        response = client.tag_resources(
            ResourceARNList=[
                resources_arn,
            ],
            Tags={
                key_list[2]: val_list[2],
                key_list[3]: val_list[3],
                key_list[4]: val_list[4],
                key_list[5]: val_list[5],
                key_list[6]: val_list[6],
                key_list[7]: val_list[7],
                key_list[8]: val_list[8],
                key_list[9]: val_list[9],
                key_list[10]: val_list[10],
                key_list[11]: val_list[11],
                key_list[12]: val_list[12],
                key_list[13]: val_list[13]
            }
        )
if __name__ == "__main__":
    tag_resource(session)
