"""
AGT Auth Service v1.0 — Exception handler DRF custom.
"""
import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(response.data, dict) and "detail" not in response.data:
            response.data = {"detail": response.data}
        elif isinstance(response.data, list):
            response.data = {"detail": response.data}
    else:
        logger.exception("Unhandled exception", exc_info=exc)
        response = Response(
            {"success": False, "error": {"code": "INTERNAL_ERROR", "message": "Erreur interne du serveur."}},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
