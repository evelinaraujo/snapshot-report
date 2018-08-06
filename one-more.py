#!/usr/bin/python

from datetime import datetime, timedelta, date
import logging
import boto3
import csv
import pandas as pd
from io import BytesIO

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#variables
tag_key = 'Name'
account = '061682043522'
client = boto3.client('ec2')
s3bucket = "s3://evelin-test"


snapshotlist = client.describe_snapshots(OwnerIds = [account])['Snapshots']

def get_snapshots():
    snapshotlistarray = []    
    snapshotnumber = len(snapshotlist)

    print("There are a total of %s Snapshots in account %s " % (snapshotnumber, account))   
    for snapshot in snapshotlist:
        snapshotID = snapshot['SnapshotId']
        snapshotlistarray.append(snapshotID)
    
    return snapshotlistarray

def get_age():
    snapshotagearray = []
    for snapshot in snapshotlist:
        snapshotage = snapshot['StartTime']
        snapshotagearray.append(snapshotage)
    return snapshotagearray

def get_volume():
    snapshotvolumearray = []
    for snapshot in snapshotlist:
        snapshotvolume = snapshot['VolumeId']
        snapshotvolumearray.append(snapshotvolume)          

    return snapshotvolumearray

def volume_exist(snapshotvolumearray):
    volumeexistarray = []
    for volume in snapshotvolumearray:
        try: 
            volumes = client.describe_volumes(VolumeIds = [volume])['Volumes']
            for v in volumes:
                attachment = v['Attachments']
                for i in attachment:
                    volumeexist = i['VolumeId']
                    # print volumeexist
                    volumeexistarray.append("Volume exists")    
        
        except Exception as e:
            volumeexistarray.append('Volume does not exist')
            # logging.error(e)
    return volumeexistarray

snapshotvolumearray = get_volume()
volume_exist(snapshotvolumearray)


def instance_associate():
    instanceidarray = []
    for volume in snapshotvolumearray:
        try: 
            volumes = client.describe_volumes(VolumeIds = [volume])['Volumes']
            for v in volumes:
                attachment = v['Attachments']
                for i in attachment:
                    instanceid = i['InstanceId']
                    instanceidarray.append(instanceid)    
        
        except Exception as e:
            instanceidarray.append('No instance associated')
            # logging.error(e)
    return instanceidarray

snapshotvolumearray = get_volume()

def instance_name():
    instancenamearray = []
    for instance in instanceidarray:
        try:
            reservations = client.describe_instances(InstanceIds = [instance])['Reservations']
            for instances in reservations:
                for instance in instances['Instances']:
                    for tags in instance['Tags']:
                        if tags["Key"] == "Name":
                            instancename = tags["Value"]
                            instancenamearray.append(instancename)     

        except Exception as e:
            instancenamearray.append("no instance name")
            # print "No instance"
            # logging.error(e)

    return instancenamearray
instanceidarray = instance_associate()

def display(snapshotlistarray, snapshotagearray, snapshotvolumearray, volumeexistarray, instanceidarray, instancenamearray):
    client = boto3.client('s3')
    
    df = pd.DataFrame([snapshotlistarray,snapshotagearray, snapshotvolumearray, volumeexistarray, instanceidarray, instancenamearray])
    df.index = ['Snapshots', 'Age', 'VolumeID', 'Volume Exist?', 'Instance ID', 'Instance Name']

    df.to_csv(csv_buffer, index=False)
        
    # write stream to S3
    obj = client.put_object(Bucket="evelin-test", Key = 'report.csv', Body=gz_buffer.getvalue())

    print (snapshotlistarray, snapshotagearray, snapshotvolumearray, volumeexistarray, instanceidarray, instancenamearray)
snapshotlistarray = get_snapshots()
snapshotagearray = get_age()
snapshotvolumearray = get_volume()
volumeexistarray = volume_exist(snapshotvolumearray)
instanceidarray = instance_associate()
instanccenamearray = instance_name()
display(snapshotlistarray, snapshotagearray, snapshotvolumearray, volumeexistarray, instanceidarray, instanccenamearray)


# It looks like df.to_csv takes a file-like instead of an explicit path, so write to a io.BytesIO, and then pass that buffer to s3.upload_fileobj.

