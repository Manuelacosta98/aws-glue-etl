#!/usr/bin/env python3
import os
import aws_cdk as cdk

from stacks.glue_jobs_stack import GlueJobsStack
from stacks.glue_workflows_stack import GlueWorkflowsStack

app = cdk.App()

# Environment configuration
account = os.environ.get("CDK_DEFAULT_ACCOUNT", os.environ.get("AWS_ACCOUNT_ID"))
region = os.environ.get("CDK_DEFAULT_REGION", os.environ.get("AWS_REGION", "us-west-2"))

env = cdk.Environment(account=account, region=region)

# Define stacks
glue_jobs_stack = GlueJobsStack(
    app, 
    "GlueJobsStack", 
    env=env
)

glue_workflows_stack = GlueWorkflowsStack(
    app, 
    "GlueWorkflowsStack", 
    glue_jobs=glue_jobs_stack.glue_jobs,
    env=env
)

app.synth()