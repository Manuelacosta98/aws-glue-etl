import aws_cdk as core
import aws_cdk.assertions as assertions

from stacks.glue_jobs_stack import GlueJobsStack

def test_glue_jobs_stack_creates_jobs():
    app = core.App()
    stack = GlueJobsStack(app, "TestGlueJobsStack")
    template = assertions.Template.from_stack(stack)
    # Check at least one Glue Job is created
    resources = template.find_resources("AWS::Glue::Job")
    assert resources, "No Glue jobs found in the stack"