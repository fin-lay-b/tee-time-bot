import boto3
import tempfile


def get_cert_value(cert_arn: str) -> str:
    client = boto3.client("ssm")
    response = client.get_parameter(Name=cert_arn, WithDecryption=True)
    return response["Parameter"]["Value"]


def create_cert_path(cert_value: str) -> str:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(cert_value.encode("utf-8"))
        return temp_file.name
