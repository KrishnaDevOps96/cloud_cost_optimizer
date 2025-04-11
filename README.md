# cloud_cost_optimizer
A production-ready tool to monitor and optimize cloud costs for **AWS** and **GCP**.This project separates AWS and GCP logic into distinct modules, enabling independent usage and deployment. it includes automation, logging, and containerization.
---

## Features
- **AWS**:
  - Monitors daily costs (7-day window) via Cost Explorer.
  - Auto-stops idle EC2 instances.
- **GCP**:
  - Analyzes costs via BigQuery billing export.
  - Auto-stops idle Compute Engine instances.
- **Shared**:
  - Configurable via YAML.
  - Logs actions for auditing.
  - Dockerized for portability.
## Quick Start
- Clone: `git clone https://github.com/your-username/cloud_cost_optimizer.git`
-  AWS: Run `pip install -r requirements/aws_requirements.txt && python aws_cost_optimizer.py`
-  GCP: Set `GOOGLE_APPLICATION_CREDENTIALS`, then `pip install -r requirements/gcp_requirements.txt && python gcp_cost_optimizer.py`

---

## Prerequisites
- Python 3.9+
- AWS account and GCP account
- AWS CLI and GCP SDK installed

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/cloud-cost-optimizer.git
cd cloud-cost-optimizer
```
### 2. AWS Setup
- Install dependencies: `pip install -r requirements/aws_requirements.txt`
- Configure AWS: `aws configure`
- Update `config/aws_config.yaml` with your region.
### 3. GCP Setup
- Install dependencies: `pip install -r requirements/gcp_requirements.txt`
- Set up billing export to BigQuery (GCP Docs).
- Create a service account with `Compute Admin` and `BigQuery User` roles, download the JSON key.
- Update `config/gcp_config.yaml` with your project ID, zone, and key path.
## Running the Tool
### AWS
```bash
python aws_cost_optimizer.py
```
Or with Docker:
```bash
docker build -f Dockerfile.aws -t aws-cost-optimizer .
docker run aws-cost-optimizer
```
### GCP
```bash
python gcp_cost_optimizer.py
```
Or with Docker (mount the service account key):
```bash
docker build -f Dockerfile.gcp -t gcp-cost-optimizer .
docker run -v /path/to/service-account-key.json:/app/service-account-key.json gcp-cost-optimizer
```
## Project Structure
```
automated-cost-optimizer/
├── aws_cost_optimizer.py    # AWS logic
├── gcp_cost_optimizer.py    # GCP logic
├── config/
│   ├── aws_config.yaml      # AWS settings
│   └── gcp_config.yaml      # GCP settings
├── requirements/
│   ├── aws_requirements.txt # AWS deps
│   └── gcp_requirements.txt # GCP deps
├── Dockerfile.aws           # AWS Docker
├── Dockerfile.gcp           # GCP Docker
├── README.md
└── cost_optimizer.log       # Logs
```
## Permissions
### AWS IAM:
- `ce:GetCostAndUsage` (Cost Explorer)
- `ec2:DescribeInstances`, `ec2:StopInstances` (EC2)

### GCP IAM:
- `compute.instances.list`, `compute.instances.stop` (Compute Admin)
- `bigquery.jobs.create`, `bigquery.tables.getData` (BigQuery User)
## Customization
- Adjust `cost_threshold` in config files.
- Change regions/zones as needed.
## Troubleshooting
- **AWS Errors**: Verify IAM permissions and AWS CLI configuration.
- **GCP Errors**: Ensure BigQuery billing export and service account key are set up correctly.
- Still stuck? Check the [issue tracker](https://github.com/Krishna_DevOps96/cloud_cost_optimizer/issues) or open a new issue.
## Future Enhancements
- Schedule via AWS Lambda or GCP Cloud Functions.
- Send cost alerts via SNS or Pub/Sub.
- Build a CLI with `argparse` for easier interaction.
- Add multi-cloud support (e.g., Azure).
- Create a web dashboard for cost visualization.
## Contributing
Want to improve this tool? Fork the repo, make your changes, and submit a pull request. For major changes, open an issue first to discuss. Check out [Future Enhancements](#future-enhancements) for ideas!
