#!/usr/bin/python

import json
from datetime import datetime, timedelta, date
import logging
import boto3
import csv

logger = logging.getLogger()
logger.setLevel(logging.INFO)

tag_key='Name'
account='061682043522'
client = boto3.client('ec2')
s3bucket = "evelin-test"

def describe_snapshot():
    #initializing two arrays for snap id and age  
    snapid = []
    age = []
    snapshot = client.describe_snapshots(
        OwnerIds = [account])['Snapshots']
    number = len(snapshot)
    print("There are a total of %s Snapshots in account %s " % (number, account))   
    #appending to the empty array every time this loops
    for snap in snapshot:
        snapid = snap['SnapshotId']
        snapid.append
        age = snap['StartTime']#.strftime('%F')
        print ("Snapshot %s was created on %s" % (snapid, age))
    
    return snapid, age

def describe_volumes():
    volume = client.describe_volumes()
    for v in volume['Volumes']:
        if v['Attachments'] == []:
            volumeid = v['VolumeId']
            print ("The following volumes are not attached to an instance %s" % volumeid)
        else:
            for i in v['Attachments']:
                instanceid = i['InstanceId']
                instance = client.describe_instances(InstanceIds = [instanceid])['Reservations']
                for i in instance:
                    for l in i['Instances']:
                        if l['Tags'] == []:
                            print("Volume %s is attached to instance ID %s with no tag name" % (volumeid, instanceid))
                        else:
                            for m in l['Tags']:
                                if m['Key'] == 'Name':
                                    name = m['Value']
                                    print ("Volume %s  is attached to instance name %s %s" % (volumeid, name, instanceid))

def export_to_csv():
    with open('report.csv', 'w') as csvfile:
        fieldnames = ['Snapshots', 'Age', 'VolumeID', 'Associated to Instance Y/N', 'InstanceID', 'Instance Name']
        #fieldnames = ['first_name', 'last_name', 'Grade']
        snapid, age = describe_snapshot()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()    
        writer.writerows(
            [
                {'Snapshots': snapid, 'Age': age,

                }
            ]
        )
        #writer.writerows([{'Grade': 'B', 'first_name': 'Alex', 'last_name': 'Brian'},
                        # {'Grade': 'A', 'first_name': 'Rachael', 'last_name': 'Rodriguez'},
                        # {'Grade': 'C', 'first_name': 'Tom', 'last_name': 'smith'},
                        # {'Grade': 'B', 'first_name': 'Jane', 'last_name': 'Oscar'},
                        # {'Grade': 'A', 'first_name': 'Kennzy', 'last_name': 'Tim'}])
            
print("writing complete")

def lambda_handler():
    describe_snapshot()
    describe_volumes()
    export_to_csv()

if __name__ == '__main__':
    lambda_handler()