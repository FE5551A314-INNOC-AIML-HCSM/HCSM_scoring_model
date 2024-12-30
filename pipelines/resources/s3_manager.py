from dagster import resource, String
import boto3

@resource(config_schema={
    "aws_access_key_id": String,
    "aws_secret_access_key": String,
    "region": String,
})
def s3_resource(context):
    return boto3.client(
        "s3",
        aws_access_key_id=context.resource_config["aws_access_key_id"],
        aws_secret_access_key=context.resource_config["aws_secret_access_key"],
        region_name=context.resource_config["region"],
    )
