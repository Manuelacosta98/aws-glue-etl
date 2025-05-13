import aws_cdk as core
import aws_cdk.assertions as assertions

from stacks.glue_workflows_stack import GlueWorkflowsStack

def test_glue_workflows_stack_creates_workflow_and_trigger():
    app = core.App()
    # Mock glue_jobs as required by GlueWorkflowsStack
    class DummyJob:
        def __init__(self, name):
            self.name = name
            self.ref = "dummy-ref"
    glue_jobs = {"extract_data_job": DummyJob("extract_data_job")}
    stack = GlueWorkflowsStack(app, "TestGlueWorkflowsStack", glue_jobs=glue_jobs)
    template = assertions.Template.from_stack(stack)
    # Check at least one Glue Workflow is created
    resources = template.find_resources("AWS::Glue::Workflow")
    assert resources, "No Glue workflows found in the stack"
    # Check at least one Glue Trigger is created
    triggers = template.find_resources("AWS::Glue::Trigger")
    assert triggers, "No Glue triggers found in the stack"