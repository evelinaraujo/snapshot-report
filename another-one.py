#!/usr/bin/python

import json
from datetime import datetime, timedelta, date
import logging
import boto3
import csv

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#variables
tag_key = 'Name'
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
    print("There are a total of %s Snapshots in account %s " % (snapshotnumber, account))   

    for snapshot in snapshotlist:
        snapshotID = snapshot['SnapshotId']
        snapshotlistarray.append(snapshotID)
        
        snapshotage = snapshot['StartTime']#.strftime
        snapshotagearray.append(snapshotage)

        snapshotvolume = snapshot['VolumeId']
        snapshotvolumearray.append(snapshotvolume)

    return snapshotlistarray, snapshotagearray, snapshotvolumearray

def describe_volume(snapshotvolumearray):
    print(snapshotvolumearray)
    
snapshotvolumearray = describe_snapshot()
describe_volume(snapshotvolumearray)

# def yoyo (snapshotlistarray, snapshotagearray, snapshotvolumearray):    
#     print(snapshotlistarray,snapshotagearray,snapshotvolumearray)
# snapshotlistarray,snapshotagearray,snapshotvolumearray = describe_snapshot()
# yoyo(snapshotlistarray,snapshotagearray,snapshotvolumearray)


#    describe_snapshot()
   # lambda_handler()    

# def newUser():    
#     Username = raw_input('Choose a username? ')
#     return Username
# def reg_user(newUser):
#     '''Make 3 users an save to a list'''
#     l = []
#     for i in range(3):
#         l.append(newUser())        
#     return l   
    
# if __name__ == '__main__':     
#     print reg_user(newUser)