from dagster import repository
from pipelines.jobs.retrieve_and_prepare_source_data_pipeline import retrieve_and_prepare_source_data_pipeline
# from pipelines.jobs.data_analysis_pipeline import data_analysis_pipeline
from pipelines.resources.s3_manager import s3_resource

@repository
def my_dagster_repo():
    return [
        retrieve_and_prepare_source_data_pipeline
    ]
