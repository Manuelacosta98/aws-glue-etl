import os
import json

from constructs import Construct
from aws_cdk import (
    Stack,
    RemovalPolicy,
    CfnOutput,
    aws_glue as glue,
    aws_iam as iam,
    aws_s3 as s3,
    aws_s3_assets as s3_assets
)
from utils.functions import discover_jobs, get_final_job_config, get_job_props_from_config

jobs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "jobs")
config_base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "jobs", "base")
default_python_config_path = os.path.join(config_base_dir, "default_python_job_config.json")
default_spark_config_path = os.path.join(config_base_dir, "default_spark_job_config.json")

class GlueJobsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        glue_role = iam.Role(
            self, "GlueJobRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSGlueServiceRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
            ]
        )
        
        scripts_bucket = s3.Bucket(
            self, "GlueScriptsBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )
        

        # Load default configs
        with open(default_python_config_path, "r") as f:
            default_python_config = json.load(f)
        with open(default_spark_config_path, "r") as f:
            default_spark_config = json.load(f)

        self.glue_jobs = {}

        # Use the discover_jobs function
        jobs = discover_jobs(jobs_dir)

        for job_info in jobs:
            job_name = job_info["job_name"]
            job_path = job_info["job_path"]
            config_path = job_info["config_path"]
            folder = job_info["folder"]

            # Load job_config.json if present
            job_config = {}
            if config_path:
                with open(config_path, "r") as f:
                    job_config = json.load(f)

            # Get the final config using the utility function
            config = get_final_job_config(job_config, default_python_config, default_spark_config)
            config["script_location"] = job_path

            # Upload script to S3
            script_asset = s3_assets.Asset(
                self, f"{job_name}Asset",
                path=job_path
            )

            # Use the helper to get job_props
            job_props = get_job_props_from_config(
                config=config,
                glue_role_arn=glue_role.role_arn,
                script_asset=script_asset,
                folder=folder,
                scripts_bucket=scripts_bucket
            )
            job_props["name"] = job_name  # Ensure job name is set

            job = glue.CfnJob(
                self, f"GlueJob{job_name.title().replace('_', '')}",
                **job_props
            )
            self.glue_jobs[job_name] = job

        CfnOutput(self, "GlueJobsCreated", value=json.dumps(list(self.glue_jobs.keys())))
        CfnOutput(self, "GlueScriptsBucketName", value=scripts_bucket.bucket_name)