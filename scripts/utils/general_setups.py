import sys
import os
import importlib

def setup_notebook_environment():
    """
    Set up the Python path for the notebook and dynamically reload modules.
    """
    # Add the parent directory of 'pipelines' to the Python path
    parent_dir = os.path.abspath("..")
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)

def reload_and_import(module_name, attribute_name=None):
    """
    Reload a module and optionally import an attribute (e.g., function or class).

    Args:
        module_name (str): The module to reload (e.g., 'pipelines.resources.path_config').
        attribute_name (str, optional): The specific attribute to import (e.g., 'get_base_config').

    Returns:
        module or attribute: The reloaded module or imported attribute.
    """
    module = importlib.import_module(module_name)
    importlib.reload(module)
    if attribute_name:
        return getattr(module, attribute_name)
    return module
