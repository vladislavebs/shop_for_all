import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import exceptions as exc

from shop_for_all.helpers.errors import (
    InvalidRequest,
    IntegrityErrorParser,
    IdNotFound,
    InternalError,
)
from shop_for_all.helpers.methods import get_index

GENERAL_ERRORS_MESSAGE = "Service is currently unavailable. Please come back later!"


EXCEPTIONS = {ObjectDoesNotExist: lambda exception: (str(exception), 404)}

# RelatedObjectDoesNotExist


class ExceptionHandlerMiddleware(MiddlewareMixin):
    @staticmethod
    def _process_exception(_, exception):
        for exception_type, exception_method in EXCEPTIONS.items():
            if isinstance(exception, exception_type):
                message, status, *key_name = exception_method(exception)
                key_name = get_index(key_name, 0, "detail")

                return JsonResponse({key_name: message}, status=status)

    @staticmethod
    def process_exception(_, response):
        traceback.print_exc()
        code = 500
        if isinstance(response, exc.ValidationError):
            code = InvalidRequest.code
        elif isinstance(response, IntegrityError):
            response = IntegrityErrorParser(response)
            code = response.code
        elif isinstance(response, IdNotFound):
            code = IdNotFound.code
        elif isinstance(response, ObjectDoesNotExist):
            code = IdNotFound.code
        elif isinstance(response, exc.AuthenticationFailed):
            code = exc.AuthenticationFailed.status_code
        elif isinstance(response, EmptyPage):
            code = 404
        elif isinstance(response, InternalError):
            pass
        else:
            response = InternalError(response)

        message = GENERAL_ERRORS_MESSAGE
        if hasattr(response, "message"):
            message = GENERAL_ERRORS_MESSAGE
        elif hasattr(response, "detail"):
            message = response.detail
        elif code != 500:
            message = str(response)

        return JsonResponse({"detail": message}, status=code)
