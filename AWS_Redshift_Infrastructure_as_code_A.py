# Infrastructure-as-code

import pandas as pd
import boto3
import json
import boto3
import configparser

LOG_DATA = config.get("S3","LOG_DATA")
SONG_DATA = config.get("S3","SONG_DATA")
ARN = config.get("IAM_ROLE","ARN")

# Load DataWarehouse Params from a file
config = configparser.ConfigParser()
config.read_file(open('dwh.cfg'))

KEY                    = config.get('AWS','KEY')
SECRET                 = config.get('AWS','SECRET')

IAM_ROLE_NAME=config.get('CLUSTER','IAM_ROLE_NAME')

CLUSTER_TYPE       = config.get("CLUSTER","CLUSTER_TYPE")
NUM_NODES          = config.get("CLUSTER","NUM_NODES")
NODE_TYPE          = config.get("CLUSTER","NODE_TYPE")

CLUSTER_IDENTIFIER = config.get("CLUSTER","CLUSTER_IDENTIFIER")

DB_NAME                 = config.get("CLUSTER","DB_NAME")
DB_USER            = config.get("CLUSTER","DB_USER")
DB_PASSWORD        = config.get("CLUSTER","DB_PASSWORD")
DB_PORT               = config.get("CLUSTER","DB_PORT")


# Create clients for EC2,S3,IAM and Redshift
ec2 = boto3.resource('ec2',
                    region_name = "us-west-2",
                    aws_access_key_id = KEY,
                    aws_secret_access_key = SECRET)

s3 = boto3.resource('s3',
                       region_name = "us-west-2",
                       aws_access_key_id=KEY,
                       aws_secret_access_key=SECRET
                   )

iam = boto3.client('iam',aws_access_key_id=KEY,
                     aws_secret_access_key=SECRET,
                     region_name="us-west-2"
                  )

redshift = boto3.client('redshift',
                       region_name = "us-west-2",
                       aws_access_key_id = KEY,
                       aws_secret_access_key = SECRET)

# check out the placeholder data in S3 data source bucket created by AWS
sampleDbBucket =  s3.Bucket("awssampledbuswest2")
for obj in sampleDbBucket.objects.filter(Prefix="ssbgz"):
    print(obj)