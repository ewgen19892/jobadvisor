"""JobAdvisor app."""
from .celery import app as celery_app

__version__: str = "1.0.3"

__all__: list = ["celery_app", "__version__"]
