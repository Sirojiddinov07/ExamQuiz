from rest_framework import generics, response, status
import exceptions as ex

from typing import Type

from django.utils.translation import gettext as _
from rest_framework import permissions, request, throttling, views

from account import enums
import services
from account.auth import ResendSerializer
from account import views as http_views


class AbstractSendSms(views.APIView, http_views.ApiResponse):
    serializer_class = ResendSerializer
    throttle_classes = [throttling.UserRateThrottle]
    permission_classes = [permissions.AllowAny]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = services.UserService()

    def post(self, rq: Type[request.Request]):
        ser = self.serializer_class(data=rq.data)
        ser.is_valid(raise_exception=True)
        phone = ser.data.get("phone")
        self.service.send_confirmation(phone)
        return self.success(_(enums.Messages.SEND_MESSAGE) % {"phone": phone})


class ApiResponse:
    def __init__(self): ...

    def response(
        self,
        success=True,
        message="",
        data=None,
        status_code=status.HTTP_200_OK,
        **kwargs,
    ):
        if data is None:
            data = {}
        response_data = {
            "success": success,
            "message": message,
            "data": data,
            **kwargs,
        }

        return response.Response(data=response_data, status=status_code)

    def success(
        self, message="", data=None, status_code=status.HTTP_200_OK, **kwargs
    ):
        return self.response(True, message, data, status_code, **kwargs)

    def error(
        self,
        message="",
        data=None,
        error_code=0,
        status_code=status.HTTP_400_BAD_REQUEST,
        exception=None,
        **kwargs,
    ):
        if isinstance(exception, ex.BreakException):
            raise exception
        return self.response(
            False, message, data, status_code, error_code=error_code, **kwargs
        )  # noqa


class ListApiView(generics.ListAPIView, ApiResponse):
    def list(self):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return self.success(data=serializer.data)


class CreateApiView(generics.CreateAPIView, ApiResponse):
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return self.success(
            self.message
            if hasattr(self, "message")
            else "Successfully created"
        )  # noqa
