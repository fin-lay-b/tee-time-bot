import os

import boto3
import tempfile
import json


def get_cert_value(cert_arn: str) -> str:
    # cert_path = os.path.join(os.environ.get("LAMBDA_TASK_ROOT", ""), "cert.crt")
    client = boto3.client("ssm", region_name="eu-west-2", verify=False)
    response = client.get_parameter(Name=cert_arn, WithDecryption=True)
    return response["Parameter"]["Value"]


def create_cert_path(cert_value: str) -> str:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(cert_value.encode("utf-8"))
        return temp_file.name


def get_schedule(schedule_arn: str) -> dict:
    # cert_path = os.path.join(os.environ.get("LAMBDA_TASK_ROOT", ""), "cert.crt")
    client = boto3.client("ssm", region_name="eu-west-2", verify=False)
    response = client.get_parameter(Name=schedule_arn, WithDecryption=True)
    return json.loads(response["Parameter"]["Value"])
