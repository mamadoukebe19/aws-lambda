import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Describe all running instances
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )
    
    instances_to_stop = []
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances_to_stop.append(instance['InstanceId'])
    
    # Stop running instances
    if instances_to_stop:
        ec2.stop_instances(InstanceIds=instances_to_stop)
        print(f'Stopped instances: {instances_to_stop}')
    else:
        print('No running instances to stop')
