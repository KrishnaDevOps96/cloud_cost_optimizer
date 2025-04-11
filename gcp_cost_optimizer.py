from google.cloud import compute_v1, bigquery
from google.oauth2 import service_account
import yaml
import logging
from datetime import datetime, timedelta

# Load GCP config
with open('config/gcp_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Setup logging
logging.basicConfig(filename='cost_optimizer.log', level=config['log_level'])

def optimize_gcp():
    try:
        credentials = service_account.Credentials.from_service_account_file(config['credentials_file'])
        
        # Cost Analysis with BigQuery
        bq_client = bigquery.Client(credentials=credentials, project=config['project_id'])
        query = f"""
        SELECT
          DATE(usage_start_time) as date,
          SUM(cost) as daily_cost
        FROM `{config['bigquery_dataset']}.{config['bigquery_table']}`
        WHERE usage_start_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
        GROUP BY date
        ORDER BY date
        """
        results = bq_client.query(query).result()
        
        total_cost = 0
        for row in results:
            total_cost += row.daily_cost
            logging.info(f"GCP Date: {row.date}, Cost: ${row.daily_cost:.2f}")
        
        avg_cost = total_cost / 7
        logging.info(f"GCP Average Cost: ${avg_cost:.2f}")
        if avg_cost > config['cost_threshold']:
            logging.warning(f"GCP cost (${avg_cost:.2f}) exceeds threshold")
        
        # Auto-stop idle GCP instances
        compute_client = compute_v1.InstancesClient(credentials=credentials)
        instances = compute_client.list(project=config['project_id'], zone=config['zone'])
        for instance in instances:
            if instance.status == "RUNNING":
                compute_client.stop(project=config['project_id'], zone=config['zone'], instance=instance.name)
                logging.info(f"Stopped GCP instance: {instance.name}")
    except Exception as e:
        logging.error(f"GCP Error: {e}")

if __name__ == "__main__":
    logging.info("Starting GCP cost optimization...")
    optimize_gcp()
    logging.info("GCP optimization complete.")