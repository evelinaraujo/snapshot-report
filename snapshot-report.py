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
    snapshot = []
    snapshot = client.describe_snapshots(OwnerIds = [account])['Snapshots']
    number = len(snapshot)
    print("There are a total of %s Snapshots in account %s " % (number, account))   
    #appending to the empty array every time this loops
    for snap in snapshot:
        snapid = snap['SnapshotId']
        #snapshotid.append(snapid)
        age = snap['StartTime']#.strftime('%F')
        #snapshotage.append(age)
        print ("Snapshot %s was created on %s" % (snapid, age))
    return snapid, snapshot, age
    #print snapshotage
    

def describe_volumes():
    #initializing two arrays for snap id and age  
    snapshotid = []
    snapshotage = []
    volumeids = []
    instanceids = []
    instancename = []

    snapshot, snapid, age = describe_snapshot()
    
    #Iterate through the list of volumes
    for snap in snapshot:
        snapshotid.append(snapid)
        print snapshotid       
        snapshotage.append(age)
        volumeid = snap['VolumeId']
        volumes = client.describe_volumes(
            VolumeIds=[volumeid]
        )
        for volume in volumes:
            #if there are no attachments, itll print the print statement
            #this will probably append all volumes not just the ones associated to snapshots
            if volume['Attachments'] != []:
                        #If there are attachments to the volume, itll go through this else statement and append to volumeids array & instanceids array
                for attachments in volume['Attachments']:
                    instanceid = attachments['InstanceId']
                    instancelist = client.describe_instances(InstanceIds = [instanceid])['Reservations']
                    
                    instanceids.append(instanceid)
                        
                    for instances in instancelist:
                        for instance in instances['Instances']:
                            if instance['Tags'] == []: 

                                print("Volume %s is attached to instance ID %s with no tag name" % (volumeid, instanceid))
                            else:
                                for tag in instance['Tags']:
                                    if tag['Key'] == 'Name':
                                        name = tag['Value']
                                        instancename.append(name)
                                        print ("Volume %s  is attached to instance name %s %s" % (volumeid, name, instanceid))
        volumeids.append(volumeid)
        print ("The following volumes are not attached to an instance %s" % volumeid)
    #return snapshotid, snapshotage

        print volumeids
        print volumes
        print instanceids
        print instancename
    return snapshotid, snapshotage, volumeids, instanceids, instancename
    
def export_to_csv():
    with open('report.csv', 'w') as csvfile:
        fieldnames = ['Snapshots', 'Age', 'VolumeID', 'Associated to Instance Y/N', 'InstanceID', 'Instance Name']
        #fieldnames = ['first_name', 'last_name', 'Grade']
        
        #snapshotid, snapshotage = describe_snapshot()
        volumeids, snapshotid, snapshotage, instanceids, instancename = describe_volumes()

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
            
        writer.writerows(
            [
                {'Snapshots': snapshotid, 'Age': snapshotage, 'VolumeID': volumeids, 'Associated to Instance Y/N': '', 'InstanceID': instanceids, 'Instance Name': instancename

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
    # export_to_csv()

if __name__ == '__main__':
    lambda_handler()