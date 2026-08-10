"""
Custom application exceptions.
"""

from typing import Any, Optional


class AppException(Exception):
    """Base application exception."""
    
    def __init__(self, message: str, code: str = "APP_ERROR", details: Optional[dict] = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundException(AppException):
    """Resource not found exception."""
    
    def __init__(self, resource: str, identifier: Any):
        super().__init__(
            message=f"{resource} with identifier '{identifier}' not found",
            code="NOT_FOUND",
            details={"resource": resource, "identifier": identifier}
        )


class ValidationException(AppException):
    """Data validation exception."""
    
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            details={"field": field} if field else {}
        )


class ConflictException(AppException):
    """Resource conflict exception."""
    
    def __init__(self, message: str):
        super().__init__(
            message=message,
            code="CONFLICT"
        )


class ProcessingException(AppException):
    """Background processing exception."""
    
    def __init__(self, message: str, task_id: Optional[str] = None):
        super().__init__(
            message=message,
            code="PROCESSING_ERROR",
            details={"task_id": task_id} if task_id else {}
        )


class AIProviderException(AppException):
    """AI provider error exception."""
    
    def __init__(self, message: str, provider: Optional[str] = None):
        super().__init__(
            message=message,
            code="AI_PROVIDER_ERROR",
            details={"provider": provider} if provider else {}
        )
