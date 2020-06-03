import boto3
import sys
import os
import time
try:
    from past.builtins import raw_input
except:
    raw_input = input

def conn_to_my_aws(my_region):
    ec2_conn = boto3.resource('ec2', region_name=my_region)
    return ec2_conn


def list_instances(ec2_conn):
    for each in ec2_conn.instances.all():
        print(each.id)


def get_ec2_state_conn(ec2_conn, instance_id):
    for each in ec2_conn.instances.filter(Filters=[{'Name': 'instance-id', "Values": [instance_id]}]):
        pr_state = each.state['Name']
    return pr_state


def start_instance(ec2_conn, instance_id):
    pr_state = get_ec2_state_conn(ec2_conn, instance_id)
    if pr_state == "running":
        print('Instance is already running.')
    else:
        for each in ec2_conn.instances.filter(Filters=[{'Name': 'instance-id', "Values": [instance_id]}]):
            each.start()
            print('Please wait, system is performing the desired activity to start the instance.')
            each.wait_until_running()
            print('Alrighty! It is running now.')
    return


def Thank_you():
    print('\n\n************** System Ended ******************')
    return None


def stop_instance(ec2_conn, instance_id):
    pr_state = get_ec2_state_conn(ec2_conn, instance_id)
    if pr_state == "stopped":
        print('Instance is already stopped.')
    else:
        for each in ec2_conn.instances.filter(Filters=[{'Name': 'instance-id', "Values": [instance_id]}]):
            each.stop()
            print('Please wait, Instance is stopping!')
            each.wait_until_stopped()
            print('Alrighty! It is stopped now.')


def welcome():
    print('This script will help you in starting and stopping instances based on specified region and instance id provided by the user.')
    time.sleep(3)


def main():
    welcome()
    my_region = raw_input("Enter your region name: ")
    print('Please wait! The system is in a process into connecting to your AWS Environment.')
    time.sleep(3)
    ec2_conn = conn_to_my_aws(my_region)
    print('The System is displaying all instance ids in your region {}'.format(my_region))
    list_instances(ec2_conn)
    instance_id = raw_input("Enter the instance id for your ec2 node: ")
    start_stop = raw_input("Enter either stop or start command for your ec2-instance: ")
    while True:
        if start_stop not in ["start", "stop"]:
            start_stop = raw_input("Enter only stop or start commands: ")
            continue
        else:
            break
    if start_stop == "start":
        start_instance(ec2_conn, instance_id)
    else:
        stop_instance(ec2_conn, instance_id)
    Thank_you()


if __name__ == '__main__':
    os.system('cls')
    main()

