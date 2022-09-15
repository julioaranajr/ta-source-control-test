import logging

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ec2_client = boto3.client("ec2")

def handler(event, context):
    """This function should cleanup unattached network interfaces
    describe nifs
    deleted unatttached
    """
    logger.info("Initialising NIF cleanup process...")
    response = ec2_client.describe_network_interfaces(
      Filters=[
        {
            'Name': 'status',
            'Values': [
                'available',
            ]
        }
      ]
    )
    nif_ids = [nif["NetworkInterfaceId"] for nif in response["NetworkInterfaces"]]
    for nif_id in nif_ids:
        try:
            ec2_client.delete_network_interface(NetworkInterfaceId=nif_id, DryRun=True)
            logger.info(f"NIF {nif_id} been deleted")
        except (ClientError, IndexError) as e:
            logger.exception(f"Expected exception: {e}")