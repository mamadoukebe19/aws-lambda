import boto3
import os

# Initialize the EC2 client
ec2 = boto3.client('ec2')

def stop_instance(instance_id):
    try:
        # Stop the specified EC2 instance
        response = ec2.stop_instances(InstanceIds=[instance_id])
        print(f'Successfully stopped instance {instance_id}')
        return response
    except Exception as e:
        print(f'Error stopping instance {instance_id}: {str(e)}')
        raise

def lambda_handler(event, context):
    # Retrieve instance ID from the event, or fallback to environment variable
    instance_id = event.get('instance_id', os.getenv('INSTANCE_ID'))

    if not instance_id:
        raise ValueError('No EC2 instance ID provided in the event or environment variable.')

    # Stop the EC2 instance
    return stop_instance(instance_id)
