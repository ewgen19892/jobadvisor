"""JobAdvisor helpers."""
from os.path import join
from typing import Any


def upload_to(instance: Any, filename: str) -> str:
    """
    Get path for uploaded files.

    :param instance: Instance
    :param filename: uploaded file name
    :return: path
    """
    return join(instance.__class__.__name__.lower(), str(instance.pk), filename)
