import boto3
import yaml
import logging
from datetime import datetime, timedelta

# Load AWS config
with open('config/aws_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Setup logging
logging.basicConfig(filename='cost_optimizer.log', level=config['log_level'])

def optimize_aws():
    try:
        ce_client = boto3.client('ce', region_name=config['region'])
        ec2_client = boto3.client('ec2', region_name=config['region'])
        
        # Cost Analysis
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        response = ce_client.get_cost_and_usage(
            TimePeriod={'Start': start_date.strftime('%Y-%m-%d'), 'End': end_date.strftime('%Y-%m-%d')},
            Granularity='DAILY',
            Metrics=['UnblendedCost']
        )
        
        total_cost = 0
        for day in response['ResultsByTime']:
            cost = float(day['Total']['UnblendedCost']['Amount'])
            total_cost += cost
            logging.info(f"AWS Date: {day['TimePeriod']['Start']}, Cost: ${cost:.2f}")
        
        avg_cost = total_cost / 7
        logging.info(f"AWS Average Cost: ${avg_cost:.2f}")
        if avg_cost > config['cost_threshold']:
            logging.warning(f"AWS cost (${avg_cost:.2f}) exceeds threshold (${config['cost_threshold']})")
        
        # Auto-stop idle EC2 instances
        instances = ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        for reservation in instances.get('Reservations', []):
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                ec2_client.stop_instances(InstanceIds=[instance_id])
                logging.info(f"Stopped AWS instance: {instance_id}")
    except Exception as e:
        logging.error(f"AWS Error: {e}")

if __name__ == "__main__":
    logging.info("Starting AWS cost optimization...")
    optimize_aws()
    logging.info("AWS optimization complete.")