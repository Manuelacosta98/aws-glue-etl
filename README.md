# Glue ETL Repository

This repository contains the infrastructure and code for AWS Glue ETL (Extract, Transform, Load) jobs and workflows. The project is structured to facilitate easy deployment and management of Glue jobs using AWS CDK and GitHub Actions.

## Project Structure

```
glue-etl
├── .github
│   └── workflows
│       └── deploy.yml              # GitHub Actions workflow for deployment
├── build
│   └── dockerfile                  # Dockerfile for custom build images
├── config
│   ├── README.md
│   ├── base
│   │   ├── default_python_job_config.json
│   │   └── default_spark_job_config.json
│   └── examples
│       ├── python_job_config.json
│       └── spark_job.json
├── infra
│   ├── .gitignore
│   ├── app.py                      # CDK app entry point
│   ├── cdk.json                    # CDK configuration
│   ├── README.md
│   ├── requirements.txt            # Python dependencies for CDK
│   ├── requirements-dev.txt        # Dev dependencies for CDK
│   ├── source.bat
│   └── stacks
│       ├── __init__.py
│       ├── glue_jobs_stack.py      # CDK stack for Glue jobs
│       ├── glue_workflows_stack.py # CDK stack for Glue workflows
│       ├── infra_stack.py          # Main infra stack
│       └── tests
│           ├── __init__.py
│           └── unit
│               ├── __init__.py
│               └── test_infra_stack.py
├── jobs
│   ├── extract
│   │   └── extract_data.py         # Data extraction script
│   ├── transform
│   │   └── transform_data.py       # Data transformation script
│   └── load
│       └── load_data.py            # Data loading script
├── shared                          # Shared code/resources (if any)
├── tests
│   ├── test_extract.py             # Unit tests for extraction script
│   ├── test_transform.py           # Unit tests for transformation script
│   └── test_load.py                # Unit tests for loading script
├── workflows
│   └── elt_workflow.json           # JSON configuration for Glue ETL workflow
├── requirements.txt                # Python dependencies for ETL jobs
├── docker-compose.yml              # Docker Compose configuration
└── README.md                       # Project documentation
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/glue-etl.git
   cd glue-etl
   ```

2. **Install Dependencies**
   Ensure you have Python and pip installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AWS CDK**
   - Navigate to the `infra` directory:
   ```bash
   cd infra
   ```
   - Install CDK dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   - Bootstrap your AWS environment (if not already done):
   ```bash
   cdk bootstrap
   ```

4. **Deploy Infrastructure**
   - Deploy the CDK stacks:
   ```bash
   cdk deploy
   ```

5. **Run ETL Jobs**
   You can run the ETL jobs by executing the respective Python scripts located in the `jobs` directory.

## Usage Guidelines

- Modify the Python scripts in the `jobs` directory as needed for your ETL processes.
- Update the CDK stacks in the `infra/stacks` directory to manage your AWS resources.
- Use the GitHub Actions workflow defined in `.github/workflows/deploy.yml` for automated deployments.

## Contributing

Feel free to submit issues or pull requests to improve the project. Please ensure that your contributions adhere to the project's coding standards and guidelines.
