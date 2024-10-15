import boto3

# Initialize AWS clients
ec2 = boto3.client('ec2')
eks = boto3.client('eks')

def clean_vpcs():
    print("Cleaning custom VPCs...")
    vpcs = ec2.describe_vpcs()['Vpcs']
    
    for vpc in vpcs:
        vpc_id = vpc['VpcId']
        
        if vpc['IsDefault']:  # Skip the default VPC
            continue
        
        print(f"Deleting VPC {vpc_id}")
        try:
            ec2.delete_vpc(VpcId=vpc_id)
        except Exception as e:
            print(f"Error deleting VPC {vpc_id}: {e}")

def clean_ec2_instances():
    print("Terminating EC2 instances...")
    instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    
    instance_ids = [i['InstanceId'] for r in instances['Reservations'] for i in r['Instances']]
    
    if instance_ids:
        ec2.terminate_instances(InstanceIds=instance_ids)
        print(f"Terminated instances: {instance_ids}")
    else:
        print("No running instances found.")

def clean_eks_clusters():
    print("Deleting EKS clusters...")
    clusters = eks.list_clusters()['clusters']
    
    for cluster in clusters:
        print(f"Deleting EKS cluster: {cluster}")
        try:
            eks.delete_cluster(name=cluster)
        except Exception as e:
            print(f"Error deleting EKS cluster {cluster}: {e}")

def clean_ebs_volumes():
    print("Deleting unattached EBS volumes...")
    volumes = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])['Volumes']
    
    for volume in volumes:
        volume_id = volume['VolumeId']
        print(f"Deleting EBS volume: {volume_id}")
        try:
            ec2.delete_volume(VolumeId=volume_id)
        except Exception as e:
            print(f"Error deleting volume {volume_id}: {e}")

def clean_snapshots():
    print("Deleting snapshots...")
    snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']
    
    for snapshot in snapshots:
        snapshot_id = snapshot['SnapshotId']
        print(f"Deleting snapshot: {snapshot_id}")
        try:
            ec2.delete_snapshot(SnapshotId=snapshot_id)
        except Exception as e:
            print(f"Error deleting snapshot {snapshot_id}: {e}")

def clean_elastic_ips():
    print("Releasing Elastic IPs...")
    addresses = ec2.describe_addresses()['Addresses']
    
    for address in addresses:
        allocation_id = address.get('AllocationId')
        if allocation_id:
            print(f"Releasing Elastic IP: {allocation_id}")
            try:
                ec2.release_address(AllocationId=allocation_id)
            except Exception as e:
                print(f"Error releasing Elastic IP {allocation_id}: {e}")

def lambda_handler(event, context):
    # Clean up resources
    clean_vpcs()
    clean_ec2_instances()
    clean_eks_clusters()
    clean_ebs_volumes()
    clean_snapshots()
    clean_elastic_ips()
    
    return "AWS account cleanup complete."
