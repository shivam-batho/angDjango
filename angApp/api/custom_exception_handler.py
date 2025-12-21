from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    logger.error("API exception occurred", exc_info=True)

    # 🔴 Unhandled exception → 500
    if response is None:
        return Response(
            {
                "success": False,
                "code": "SERVER_ERROR",
                "message": "Something went wrong. Please try again later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # 🔐 Authentication & JWT errors
    if isinstance(exc, AuthenticationFailed):
        detail = exc.detail

        if isinstance(detail, dict):
            message = detail.get("detail") or detail.get("message") or "Authentication failed"
        else:
            message = str(detail)

        return Response(
            {
                "success": False,
                "code": "AUTH_FAILED",
                "message": message
            },
            status=response.status_code
        )

    # 🧩 Other DRF API exceptions
    if isinstance(exc, APIException):
        detail = exc.detail
        message = detail.get("message") if isinstance(detail, dict) else str(detail)

        return Response(
            {
                "success": False,
                "code": exc.default_code.upper(),
                "message": message
            },
            status=response.status_code
        )

    # 📝 Validation errors
    message = "Invalid request"
    if hasattr(response, "data") and isinstance(response.data, dict):
        for value in response.data.values():
            if isinstance(value, list) and value:
                message = value[0]
                break

    return Response(
        {
            "success": False,
            "code": "VALIDATION_ERROR",
            "message": message
        },
        status=status.HTTP_400_BAD_REQUEST
    )
