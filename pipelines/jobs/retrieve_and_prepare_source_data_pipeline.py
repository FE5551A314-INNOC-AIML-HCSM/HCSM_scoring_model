from dagster import job
from pipelines.ops.data_file_ops import (
    download_csv_from_s3,
    convert_csv_to_parquet_gz,
    upload_folder_to_s3
)
from pipelines.resources.s3_manager import s3_resource

@job(resource_defs={"s3": s3_resource})
def retrieve_and_prepare_source_data_pipeline():
    download_csv_from_s3()
    convert_csv_to_parquet_gz()
    upload_folder_to_s3()