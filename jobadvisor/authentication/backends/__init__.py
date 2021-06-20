"""Authentication backends."""
from .facebook import FacebookBackend
from .google import GoogleBackend
from .linkedin import LinkedinBackend

__all__: list = [
    "FacebookBackend",
    "GoogleBackend",
    "LinkedinBackend",
]
