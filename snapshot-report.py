#!/usr/bin/python

from datetime import datetime, timedelta
import logging
import boto3
#import csv

logger = logging.getLogger()
logger.setLevel(logging.INFO)

tag_key='Name'
tag_value = 'Evelin-Test'
account='061682043522'

def describe_snapshot(ec2, snapshot):
    client = boto3.client('ec2')
    response = client.describe_snapshots(
        OwnerIds = [account]
    )
    number = len(response['Snapshots'])
    print("There are a total of %s Snapshots in account %s " % (number, account) )
    for snapshot in response['Snapshots']:
        print snapshot['VolumeId']
        for volume in snapshot['VolumeId']:
            response2 = client.describe_volumes()
            print volume 
            # for volume['Volumes']:
            #     print(volume['Attachments'])

    # for snapshot in response['Snapshots']:
    #     response2 = ec2.describe_volume ()
    #     print h
        # if response2['Volumes']['Attachments']

        
# with open('snapshot-report.csv', 'wb')


        # Filters = [
        #     {
        #         'Name': 'tag:' + tag_key,
        #         'Values': [tag_value]
        #     }
        # ]