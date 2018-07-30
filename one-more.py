#!/usr/bin/python

from datetime import datetime, timedelta, date
import logging
import boto3
import csv

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#variables
tag_key = 'Name'
account = '061682043522'
client = boto3.client('ec2')
s3bucket = "evelin-test"

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
        snapshotage = snapshot['StartTime']#.strftime
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
        print volume    
    return volume

snapshotvolumearray = get_volume()
volume_exist(snapshotvolumearray)

def display(snapshotlistarray, snapshotagearray, snapshotvolumearray, volumeexistarray):
    print (snapshotlistarray, snapshotagearray, snapshotvolumearray, volumeexistarray)
snapshotlistarray = get_snapshots()
snapshotagearray = get_age()
snapshotvolumearray = get_volume()
volumeexistarray = volume_exist()
display(snapshotlistarray, snapshotagearray, snapshotvolumearray, volumeexistarray)