import csv
from datetime import datetime, timedelta, date
import boto3
from botocore.exceptions import ClientError

#variables
tag_key = 'Name'
account = '061682043522'
client = boto3.client('ec2')
s3bucket = 'evelin-test'

snapshotlist = client.describe_snapshots(OwnerIds = [account])['Snapshots']

def get_snapshots():
    snapshotnumber = len(snapshotlist)
    print("There are a total of %s Snapshots in account %s " % (snapshotnumber, account))   
    return snapshotlist

#describe volume ids
def volume_exist(volume_id):
    if not volume_id: return ''
    try:
        volume = client.describe_volumes(VolumeIds=[volume_id])
        # return ("Volume = %s" % volume_id)
        print volume
        return "Volume exists"
    except ClientError:
        return "Volume Doesn't Exist"

def instance_exist(instance_id):
    if not instance_id: return ''
    try:
        instance = client.describe_instances(InstanceId=[instance_id])
        return instance_id
    except ClientError:
        return "Instance doesnt exist"

def display():
    with open('report.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Snapshots', 'Age', 'VolumeID', 'Volume Exist?', 'Instance ID', 'Instance Name'])
        instance_id = instance_exist()
        for snapshot in snapshotlist:
            writer.writerow([
                snapshot['SnapshotId'], snapshot['StartTime'], snapshot['VolumeId'], volume_exist(snapshot['VolumeId']), instance_exist(instance_id)
            ])

display()