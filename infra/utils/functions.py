import os


def snake_to_camel_case(snake_str):
    """
    Converts a snake_case string to CamelCase (first letter uppercase).
    Example: 'my_variable_name' -> 'MyVariableName'
    """
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)

def discover_jobs(jobs_dir):
    """
    Walks the jobs directory and returns a list of dicts:
    [
        {
            "job_name": ...,
            "job_path": ...,
            "config_path": ...,
            "folder": ...,
        },
        ...
    ]
    Only includes files ending with _job.py and their job_config.json if present.
    """
    jobs = []
    if os.path.exists(jobs_dir):
        for root, dirs, files in os.walk(jobs_dir):
            for file in files:
                if file.endswith("_job.py"):
                    job_name = file.replace(".py", "")
                    job_path = os.path.join(root, file)
                    config_path = os.path.join(root, "job_config.json")
                    jobs.append({
                        "job_name": job_name,
                        "job_path": job_path,
                        "config_path": config_path if os.path.exists(config_path) else None,
                        "folder": os.path.basename(root)
                    })
    return jobs

# Deep update utility
def _deep_update(d, u):
    for k, v in u.items():
        if isinstance(v, dict) and isinstance(d.get(k), dict):
            _deep_update(d[k], v)
        else:
            d[k] = v

def get_final_job_config(job_config, default_python_config, default_spark_config):
    """
    Returns the final config for a job, starting from the default config
    (python or spark) and overwriting with values from job_config.
    """
    # Determine job type
    job_type = job_config.get("type", "python")
    if job_type == "spark":
        config = default_spark_config.copy()
    else:
        config = default_python_config.copy()

    # Overwrite defaults with job_config
    _deep_update(config, job_config)
    return config

def get_job_props_from_config(config, glue_role_arn, script_asset, folder, scripts_bucket):
    """
    Given the final config, returns a dict of job_props for glue.CfnJob.
    """
    default_arguments = config.get("default_arguments", {})
    default_arguments["--TempDir"] = f"s3://{scripts_bucket.bucket_name}/temporary/"

    glue_version = config.get("glue_version", "3.0")
    timeout = config.get("timeout_minutes", 60)
    max_retries = config.get("max_retries", 2)
    worker_type = config.get("worker_type", None)
    number_of_workers = config.get("number_of_workers", None)
    python_version = config.get("python_version", "3.10")
    job_type = config.get("type", "python")

    command_props = {
        "script_location": f"s3://{script_asset.s3_bucket_name}/{script_asset.s3_object_key}"
    }
    if job_type == "spark":
        command_props["name"] = "glueetl"
        command_props["python_version"] = python_version
    else:
        command_props["name"] = "pythonshell"
        command_props["python_version"] = python_version

    job_props = dict(
        role=glue_role_arn,
        command={"Name": command_props["name"], "ScriptLocation": command_props["script_location"], "PythonVersion": command_props["python_version"]},
        default_arguments=default_arguments,
        glue_version=glue_version,
        max_retries=max_retries,
        timeout=timeout,
        tags={"JobFolder": folder}
    )
    if worker_type:
        job_props["worker_type"] = worker_type
    if number_of_workers:
        job_props["number_of_workers"] = number_of_workers

    return job_props