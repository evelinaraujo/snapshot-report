#!/usr/bin/python

import json
from datetime import datetime, timedelta, date
import logging
import boto3
#import csv

logger = logging.getLogger()
logger.setLevel(logging.INFO)

tag_key='Name'
account='061682043522'
client = boto3.client('ec2')

def describe_snapshot():
    snapshot = client.describe_snapshots(
        OwnerIds = [account])['Snapshots']
    number = len(snapshot)
    print("There are a total of %s Snapshots in account %s " % (number, account))    
    for snap in snapshot:
        snapid = snap['SnapshotId']
        age = snap['StartTime'].strftime('%F')
        print ("Snapshot %s was created on %s" % (snapid, age))

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
                                

def lambda_handler(event,context):
    describe_snapshot()
#    return age, number, snapshot
    describe_volumes()