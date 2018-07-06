#!/usr/bin/python

import logging
import boto3
from timedelta from timedelta, 

logging = logging.getLogger()
logger.setLevel(logging.INFO)

#Variables
tag_key = 'Name'
tag_value = ''

# Check how many snapshots we have

ec2 = boto3.resource('ec2')
snapshot = ec2.Snapshot('id')

def describe_snapshots(event, context):
    for i in snapshot:
        print i
        print("These are the current snapshots %s" % i)
        #for every snapshot describe the snapshot if its associated to an instance
        ec2.describe_snapshots(
            Filters = [
                {
                    'Name':
                    'Values'
                }
            ]
        )

        



