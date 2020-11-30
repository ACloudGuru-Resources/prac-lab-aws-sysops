import boto3
import json


# Assessment Task 1 - Check an RDS Snapshot specified ARN exists

def task_snapshotexists(arn):
    clientRds = boto3.client('rds')
    
    # Attempts to get the RDS snapshot with that ARN
    try:
        snapshot = clientRds.describe_db_snapshots(DBSnapshotIdentifier=arn)
        return True
    except:
        return False


# Assessment Task 2 - Confirm EBS encryption using any Customer Managed Key on 
# an RDS Snapshot

def task_snapshotencrypted(arn):
    # Initializes boto clients for KMS and RDS
    clientKms = boto3.client('kms')
    clientRds = boto3.client('rds')
    
    # Encapsulates in a `try` in case an error is thrown
    try:
        # Checks the KMS Key Details used to encrypt the snapshot
        snapshot = clientRds.describe_db_snapshots(DBSnapshotIdentifier=arn)
        key = clientKms.describe_key(KeyId=snapshot['DBSnapshots'][0]['KmsKeyId'])
        
        # Confirms that the key is customer-managed
        if (key['KeyMetadata']['KeyManager'] == 'CUSTOMER'):
            return True
        else:
            return False
    except:
        return False


# Assesses whether a student has passed or failed the assessment. Each check
# performed iteratively. The `tasks` array is updated to list the functions that
# validate the students work as a boolean

def assess_tasks(event, context):
    # Modify array to include commands for each task
    tasks = [
        task_snapshotexists(event['queryStringParameters']['arn']),
        task_snapshotencrypted(event['queryStringParameters']['arn'])
        ]
    
    # If any task is False, whole function immediately returns False
    for t in tasks:
        if t is False:
            return False
    
    # If no tasks are false, the assessment is successful
    return True

def lambda_handler(event, context):
    result = assess_tasks(event, context)
    
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
