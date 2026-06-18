"""Service-layer exceptions translated into HTTP errors by controllers."""


class ServiceError(Exception):
    """Base class for all business-logic errors."""

    status_code = 400


class NotFoundError(ServiceError):
    status_code = 404


class ValidationError(ServiceError):
    status_code = 422


class AuthError(ServiceError):
    status_code = 401
