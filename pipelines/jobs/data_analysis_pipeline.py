from dagster import job

from pipelines.ops.analysis_ops import generic_dataframe_analyse
from pipelines.resources.s3_manager import s3_resource
from pipelines.resources.path_config import path_config

@job(resource_defs={"s3": s3_resource, "path_config": path_config})
def data_analysis_pipeline():
    generic_dataframe_analyse()
    # upload_results_to_s3(results=results)