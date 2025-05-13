# AWS Glue Workflow Configuration Reference

This document explains the configuration options available for defining AWS Glue workflows using JSON files in this repository. These workflow definitions are used by the CDK stack to provision and manage Glue workflows, triggers, and job dependencies.

---

## Workflow JSON Structure

A typical workflow configuration file contains the following top-level keys:

| Key         | Description                                                                                  | Example Value                |
|-------------|----------------------------------------------------------------------------------------------|------------------------------|
| `Name`      | The name of the Glue workflow.                                                               | `"elt_workflow"`             |
| `Description` | A description of the workflow.                                                             | `"ETL workflow for Glue"`    |
| `triggers`  | List of triggers that start jobs or workflows.                                               | See [Triggers](#triggers)    |
| `Steps`     | List of workflow steps (jobs) and their dependencies.                                        | See [Steps](#steps)          |

---

## Triggers

Triggers define **how and when** Glue jobs or workflows are started. Each trigger can be of type `ON_DEMAND`, `SCHEDULED`, or `CONDITIONAL`.

### Trigger Options

| Key         | Description                                                                                  | Example Value                |
|-------------|----------------------------------------------------------------------------------------------|------------------------------|
| `name`      | Name of the trigger.                                                                         | `"DailyTrigger"`             |
| `type`      | Type of trigger: `"ON_DEMAND"`, `"SCHEDULED"`, or `"CONDITIONAL"`.                          | `"SCHEDULED"`                |
| `schedule`  | (For `SCHEDULED` only) Cron expression for schedule.                                         | `"cron(0 2 * * ? *)"`        |
| `predicate` | (For `CONDITIONAL` only) Conditions for triggering.                                          | See below                    |
| `actions`   | List of jobs to start when the trigger fires.                                                | `[{"jobName": "extract_data_job"}]` |

#### Example: SCHEDULED Trigger

```json
{
  "name": "DailyTrigger",
  "type": "SCHEDULED",
  "schedule": "cron(0 2 * * ? *)",
  "actions": [
    { "jobName": "extract_data_job" }
  ]
}
```

#### Example: ON_DEMAND Trigger

```json
{
  "name": "OnDemandTrigger",
  "type": "ON_DEMAND",
  "actions": [
    { "jobName": "extract_data_job" }
  ]
}
```

#### Example: CONDITIONAL Trigger

```json
{
  "name": "ConditionalTrigger",
  "type": "CONDITIONAL",
  "predicate": {
    "conditions": [
      {
        "jobName": "extract_data_job",
        "state": "SUCCEEDED"
      }
    ],
    "logical": "AND"
  },
  "actions": [
    { "jobName": "transform_data_job" }
  ]
}
```

---

## Steps

The `Steps` array defines the **sequence and dependencies** of jobs in the workflow.

| Key         | Description                                                                                  | Example Value                |
|-------------|----------------------------------------------------------------------------------------------|------------------------------|
| `Name`      | Step name (unique within the workflow).                                                      | `"Extract"`                  |
| `JobName`   | Name of the Glue job to run in this step.                                                    | `"extract_data_job"`         |
| `DependsOn` | (Optional) List of step names this step depends on.                                          | `["Extract"]`                |

#### Example Steps

```json
[
  {
    "Name": "Extract",
    "JobName": "extract_data_job"
  },
  {
    "Name": "Transform",
    "JobName": "transform_data_job",
    "DependsOn": ["Extract"]
  },
  {
    "Name": "Load",
    "JobName": "load_data_job",
    "DependsOn": ["Transform"]
  }
]
```

---

## Example Workflow Configurations

### On-Demand Workflow

```json
{
  "Name": "on_demand_workflow",
  "Description": "A default on-demand Glue workflow example",
  "triggers": [
    {
      "name": "OnDemandTrigger",
      "type": "ON_DEMAND",
      "actions": [
        { "jobName": "extract_data_job" }
      ]
    }
  ],
  "Steps": [
    { "Name": "Extract", "JobName": "extract_data_job" },
    { "Name": "Transform", "JobName": "transform_data_job", "DependsOn": ["Extract"] },
    { "Name": "Load", "JobName": "load_data_job", "DependsOn": ["Transform"] }
  ]
}
```

### Scheduled Workflow

```json
{
  "Name": "scheduled_workflow",
  "Description": "A default scheduled Glue workflow example",
  "triggers": [
    {
      "name": "DailyTrigger",
      "type": "SCHEDULED",
      "schedule": "cron(0 2 * * ? *)",
      "actions": [
        { "jobName": "extract_data_job" }
      ]
    }
  ],
  "Steps": [
    { "Name": "Extract", "JobName": "extract_data_job" },
    { "Name": "Transform", "JobName": "transform_data_job", "DependsOn": ["Extract"] },
    { "Name": "Load", "JobName": "load_data_job", "DependsOn": ["Transform"] }
  ]
}
```

### Conditional Workflow

```json
{
  "Name": "conditional_workflow",
  "Description": "A default conditional Glue workflow example",
  "triggers": [
    {
      "name": "ConditionalTrigger",
      "type": "CONDITIONAL",
      "predicate": {
        "conditions": [
          { "jobName": "extract_data_job", "state": "SUCCEEDED" }
        ],
        "logical": "AND"
      },
      "actions": [
        { "jobName": "transform_data_job" }
      ]
    }
  ],
  "Steps": [
    { "Name": "Extract", "JobName": "extract_data_job" },
    { "Name": "Transform", "JobName": "transform_data_job", "DependsOn": ["Extract"] },
    { "Name": "Load", "JobName": "load_data_job", "DependsOn": ["Transform"] }
  ]
}
```

---

## Building Your Own Workflow

- **Choose your trigger type**: `ON_DEMAND`, `SCHEDULED`, or `CONDITIONAL`.
- **Define your steps**: List all jobs and their dependencies.
- **Customize actions**: Specify which jobs each trigger should start.
- **Add predicates**: For conditional triggers, define the conditions for execution.

For more details, see the [AWS Glue Triggers documentation](https://docs.aws.amazon.com/glue/latest/dg/trigger-job.html) and [AWS Glue Workflows documentation](https://docs.aws.amazon.com/glue/latest/dg/orchestrate-using-workflows.html).