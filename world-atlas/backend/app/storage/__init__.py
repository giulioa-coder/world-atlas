"""
Storage module abstraction.

Provides a unified interface for different storage backends.
"""

from app.storage.local import LocalStorage

__all__ = ["LocalStorage"]

# Future exports:
# from app.storage.s3 import S3Storage
# __all__ = ["LocalStorage", "S3Storage"]
