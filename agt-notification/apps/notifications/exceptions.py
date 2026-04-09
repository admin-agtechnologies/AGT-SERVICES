import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        logger.exception("Unhandled exception", exc_info=exc)
        response = Response({"success": False, "error": {"code": "INTERNAL_ERROR", "message": "Erreur interne."}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response
