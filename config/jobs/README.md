# AWS Glue Job Configuration Reference

This document explains the configuration options available in the `default_python_job_config.json` and `default_spark_job_config.json` files for AWS Glue jobs.

---

## Common Options

| Key                   | Description                                                                                  | Example Value                          |
|-----------------------|----------------------------------------------------------------------------------------------|----------------------------------------|
| `name`                | The name of the Glue job.                                                                    | `"my_glue_job"`                        |
| `description`         | A description of the job.                                                                    | `"ETL job for processing data"`        |
| `type`                | The job type: `"python"` for Python shell jobs, `"spark"` for Spark jobs.                    | `"python"` or `"spark"`                |
| `glue_version`        | The AWS Glue version to use. Determines available features and supported Python/Spark versions.| `"5.0"`                                |
| `number_of_workers`   | Number of worker nodes to use for the job.                                                   | `1`, `2`, etc.                         |
| `worker_type`         | The type of worker nodes. See below for valid values per job type.                           | `"G.025X"`, `"G.1X"`, `"G.2X"`         |
| `timeout_minutes`     | Maximum job run time in minutes before timeout.                                              | `60`                                   |
| `max_retries`         | Number of times to retry the job if it fails.                                                | `0`, `1`, etc.                         |
| `connections`         | List of Glue connections to use.                                                             | `["connection_name1"]`                 |
| `max_concurrent_runs` | Maximum number of concurrent runs for this job.                                              | `1`                                    |
| `script_location`     | Path to the main script for the job.                                                         | `"jobs/extract/extract_data.py"`       |

---

## Python Shell Job Specific Options (`default_python_job_config.json`)

| Key              | Description                                                                                  | Example Value      |
|------------------|----------------------------------------------------------------------------------------------|--------------------|
| `python_version` | Python version to use. For Glue 5.0, only `"3.10"` is supported.                             | `"3.10"`           |

### `default_arguments` (Python Shell)

| Key                               | Description                                                                                  | Example Value                                  |
|-----------------------------------|----------------------------------------------------------------------------------------------|------------------------------------------------|
| `--job-language`                  | Language for the job script. Always `"python"` for Python shell jobs.                        | `"python"`                                     |
| `--additional-python-modules`     | Comma-separated list of additional Python packages to install.                               | `"pandas==1.3.0,numpy==1.21.0"`                |
| `--TempDir`                       | S3 path for temporary files.                                                                 | `"s3://aws-glue-temporary/"`                   |
| `--enable-continuous-cloudwatch-log` | Enables continuous logging to CloudWatch.                                                   | `"true"`                                       |

---

## Spark Job Specific Options (`default_spark_job_config.json`)

### `worker_type` (Spark)

- `"Standard"`: Legacy worker type (not recommended for new jobs).
- `"G.1X"`: 4 vCPUs, 16 GB memory per worker.
- `"G.2X"`: 8 vCPUs, 32 GB memory per worker.

### `default_arguments` (Spark)

| Key                               | Description                                                                                  | Example Value                                  |
|-----------------------------------|----------------------------------------------------------------------------------------------|------------------------------------------------|
| `--enable-metrics`                | Enables job metrics collection.                                                              | `"true"`                                       |
| `--job-language`                  | Language for the job script. `"python"` or `"scala"`.                                       | `"python"`                                     |
| `--enable-spark-ui`               | Enables the Spark UI for monitoring.                                                         | `"true"`                                       |
| `--spark-event-logs-path`         | S3 path for Spark event logs (for Spark UI).                                                 | `"s3://aws-glue-assets-.../sparkHistoryLogs/"`  |
| `--additional-python-modules`     | Comma-separated list of additional Python packages to install.                               | `"pandas==1.3.0,numpy==1.21.0"`                |
| `--extra-py-files`                | S3 path(s) to additional Python files or zip archives to include.                            | `"s3://bucket/path/to/dependencies.zip"`        |
| `--TempDir`                       | S3 path for temporary files.                                                                 | `"s3://aws-glue-temporary/"`                   |
| `--enable-continuous-cloudwatch-log` | Enables continuous logging to CloudWatch.                                                   | `"true"`                                       |
| `--enable-job-insights`           | Enables Glue job insights for performance recommendations.                                   | `"true"`                                       |

---

## Example Minimal Configs

### Python Shell Job

```json
{
  "name": "minimal_python_shell_job",
  "type": "python",
  "glue_version": "5.0",
  "python_version": "3.10",
  "worker_type": "G.025X",
  "number_of_workers": 1,
  "script_location": "jobs/extract/extract_data.py"
}
```

### Spark Job

```json
{
  "name": "minimal_spark_job",
  "type": "spark",
  "glue_version": "5.0",
  "worker_type": "G.1X",
  "number_of_workers": 2,
  "script_location": "jobs/extract/extract_data.py"
}
```

---

## References

- [AWS Glue Job Parameters](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html)
- [AWS Glue Versions](https://docs.aws.amazon.com/glue/latest/dg/release-notes.html)
- [AWS Glue Worker Types](https://docs.aws.amazon.com/glue/latest/dg/add-job.html#job-worker-type)