from dagster import resource, String

@resource(config_schema={
    "local_resources_folder_path": String,
    "local_export_folder_path": String,
    "files": dict,
    "steps": dict,
    "general_settings": dict,
})
def path_config(context):
    """
    Wrap the base configuration as a Dagster resource.
    """
    return context.resource_config
