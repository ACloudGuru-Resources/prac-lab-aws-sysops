import boto3
import json

# Assessment Task 1 - Check if Snapshot Exists
def task_snapshotexists(arn):
    clientRds = boto3.client('rds')
    
    # Attempts to 
    try:
        response = clientRds.describe_db_snapshots(DBSnapshotIdentifier=arn)
        
        if task_snapshotencrypted(response['DBSnapshotIdentifier']):
            return True
    except:
        return False

# Assessment Task 2 - Confirm encryption using Customer Managed Key
def task_snapshotencrypted(arn):
    clientKms = boto3.client('kms')
    clientRxs = boto3.client('rds')
    
    # Creates a list of Customer Managed Key ARN's
    keys = []
    for k in clientKms.list_keys():
        key = clientKms.describe_key(KeyID=k['KeyArn'])
        
        if key['ManagedBy'] == "CUSTOMER":
            keys.extend(key['Arn'])
    
    # Confirms whether Snapshot's KMS Key's ARN is Customer Managed
    try:
        response = clientRds.describe_db_snapshots(DBSnapshotIdentifier=arn)
        
        if snapshot['KmsKeyId'] in keys:
            return True
        else:
            raise
    except:
        return False

# Assesses whether a student has passed or failed the assessment. Each check
# performed iteratively. Can be modified to return values for partial
# completion
# 
# Return `True` for pass, and `False` for failure
def assessment_check(event, context):
    task1 = task_snapshotexists(event['arn'])
    task2 = task_snapshotencrypted(event['arn'])
    
    if task1 and task2:
        return True
    else:
        return False
    
# Passes the result back to the API for the Assessment Tool
def lambda_handler(event, context):
    result = assessment_check(event, context)
    
    if result:
        return {
            'statusCode': 200,
            'body': json.dumps('Successful!')
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps('Unsuccessful!')
        }
