import os
import json

from constructs import Construct
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_glue as glue,
)
from utils.functions import snake_to_camel_case


class GlueWorkflowsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, glue_jobs, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Store reference to jobs created in the jobs stack
        self.glue_jobs = glue_jobs
        
        # Find all workflow definitions in the workflows directory
        workflow_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "workflows")
        
        if os.path.exists(workflow_dir):
            for file in os.listdir(workflow_dir):
                if file.endswith(".json"):
                    workflow_name = file.replace(".json", "")
                    workflow_path = os.path.join(workflow_dir, file)
                    
                    # Read workflow definition
                    with open(workflow_path, 'r') as f:
                        workflow_def = json.load(f)

                    
                    # Create Glue Workflow
                    workflow = glue.CfnWorkflow(
                        self, f"GlueWorkflow{snake_to_camel_case(workflow_name)}",
                        name=workflow_name,
                        description=workflow_def.get("description", f"Workflow for {workflow_name}")
                    )
                    
                    # Parse jobs from workflow definition and create triggers
                    self._create_triggers_from_workflow_def(workflow_def, workflow)

        # add  outputs for the workflows
        for workflow in self.glue_jobs.values():
            CfnOutput(
                self, f"WorkflowOutput{workflow.name}",
                value=workflow.ref,
                description=f"ARN of the Glue Workflow {workflow.name}"
            )
        
    def _create_triggers_from_workflow_def(self, workflow_def, workflow):
        """Create triggers based on the workflow definition"""
        triggers = workflow_def.get("triggers", [])
        
        for idx, trigger_def in enumerate(triggers):
            trigger_name = trigger_def.get("name", f"Trigger-{idx}")
            trigger_type = trigger_def.get("type", "ON_DEMAND").upper()
            actions = trigger_def.get("actions", [])
            
            # Convert job names to job references from the jobs stack
            actions_with_refs = []
            for action in actions:
                if action.get("jobName") in self.glue_jobs:
                    action["jobName"] = self.glue_jobs[action["jobName"]].name
                    actions_with_refs.append(action)

            predicate = None
            # Only CONDITIONAL triggers should have predicates
            if trigger_type == "CONDITIONAL" and "predicate" in trigger_def:
                predicate_def = trigger_def["predicate"]
                conditions = predicate_def.get("conditions", [])
                for condition in conditions:
                    if condition.get("jobName") in self.glue_jobs:
                        condition["jobName"] = self.glue_jobs[condition["jobName"]].name
                predicate = glue.CfnTrigger.PredicateProperty(
                    conditions=[
                        glue.CfnTrigger.ConditionProperty(
                            job_name=condition.get("jobName"),
                            logical_operator=condition.get("logicalOperator", "EQUALS"),
                            state=condition.get("state", "SUCCEEDED")
                        ) for condition in conditions
                    ],
                    logical=predicate_def.get("logical", "AND")
                )
            
            trigger_props = {
                "name": trigger_name,
                "type": trigger_type,
                "workflow_name": workflow.name,
                "actions": [
                    glue.CfnTrigger.ActionProperty(
                        job_name=action["jobName"],
                        arguments=action.get("arguments", {})
                    ) for action in actions_with_refs
                ]
            }
            
            # Only CONDITIONAL triggers should have predicates
            if trigger_type == "CONDITIONAL":
                trigger_props["predicate"] = predicate
            
            # Only SCHEDULED triggers should have a schedule
            if trigger_type == "SCHEDULED":
                trigger_props["schedule"] = trigger_def.get("schedule", "cron(0 0 * * ? *)")
            
            glue.CfnTrigger(
                self, f"Trigger{snake_to_camel_case(trigger_name)}",
                **trigger_props
            )