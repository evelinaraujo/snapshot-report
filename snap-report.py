#!/usr/bin/python

import json
from datetime import datetime, timedelta, date
import logging
import boto3
import csv

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#tag key variable
tag_key='Name'
account='061682043522'
client = boto3.client('ec2')
s3bucket = "evelin-test"

def describe_snapshot():
    #arrays
    snapshotlistarray = []
    snapshotagearray = []
    snapshotvolumearray = []
    #storing the dictionary of snapshots in snapshot variable
    snapshotlist = client.describe_snapshots(OwnerIds = [account])['Snapshots']
    snapshotnumber = len(snapshotlist)
    # literally kind of useless within the csv file
    print("There are a total of %s Snapshots in account %s " % (snapshotnumber, account))   
    
    for snapshot in snapshotlist: 
        #printing the snapshot id of every snapshot
        snapshotID = snapshot['SnapshotId']
        snapshotlistarray.append(snapshotID)
        #print snapshotID
        snapshotage = snapshot['StartTime']#.strftime
        snapshotagearray.append(snapshotage)

        snapshotvolume = snapshot['VolumeId']
        snapshotvolumearray.append(snapshotvolume)
    
       # print ("Snapshot %s was created on %s" % (snapshotID, snapshotage))
 #   print snapshotvolumearray
    return snapshotlistarray, snapshotagearray, snapshotvolumearray
    
def describe_volumes():
    volumeexist = []
    instanceIds = []
    snapshotvolumearray = describe_snapshot()
   # print(snapshotlistarray,snapshotagearray, snapshotvolumearray)
    # for every  volume in the snapshot array, try describing the volume to check whether it exists
    # if it exists, go into the next loop and check the attachments for snapshot name attached to it
    for snapshotvolume in snapshotvolumearray:
      #  print snapshotvolume
        for snap in snapshotvolume:
            try:
                volumes = client.describe_volumes(
                    VolumeIds = [snap]
                )['Volumes']
                print volumes
                for volume in volumes:
                    print volume['Attachments']
                    try:
                        for snapvolume in volume['Attachments']:
                            #snapshotvolume contains the whole dict of each volume
                            volumeid = snapvolume['VolumeId'] 
                            print snapvolume
                            instanceid = snapvolume['InstanceId']
                            #print instanceid
                            volumeexist.append(volumeid)
                            instanceIds.append(instanceid)
                            # client.describe_instances(
                            #     InstanceIds = 
                            # )
                            #print volumeexist
                            # print instanceIds
                    except Exception as e:
                        print 'no attachments'
                
            #if the volume doesn't exist, append volume does not exist
            except Exception as f:
                # a snapshot can exist with volume associated but volume doesnt exist
                volumeexist.append('Volume does not exist')
           # print ("Volume %s does not exist" % snapshotvolume)    
    print volumeexist
    return instanceIds, volumeexist
  
def export_to_csv():
    with open('report.csv', 'w') as csvfile:
            fieldnames = ['Snapshots', 'Age', 'VolumeID', 'Volume Exist?', 'Associated to Instance Y/N', 'InstanceID', 'Instance Name']
            #fieldnames = ['first_name', 'last_name', 'Grade']
            
            snapshotlistarray, snapshotagearray, snapshotvolumearray = describe_snapshot()
            instanceIds, volumeexist = describe_volumes()

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            mywriter = csv.writer(csvfile)
            writer.writeheader()
            
            rows = zip(snapshotlistarray, snapshotagearray, snapshotvolumearray, volumeexist)
            for row in rows:
                mywriter.writerow(row)
    print("writing complete")



def lambda_handler():
    describe_snapshot()
    describe_volumes()
    export_to_csv()

if __name__ == '__main__':
    lambda_handler()
    