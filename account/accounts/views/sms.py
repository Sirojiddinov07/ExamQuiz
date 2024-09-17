import typing
import uuid

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from rest_framework import request as rest_request
from rest_framework import response, status, throttling, views, viewsets

import services
from account.accounts import models
from account.accounts import serializers as sms_serializers
from account import views as http_views
from account.models import User
from account.auth import *
from account.serializers import UserSerializer
from exceptions import SmsException
from account import enums

class RegisterView(views.APIView, services.UserService):
    """Register new user"""

    serializer_class = RegisterSerializer
    throttle_classes = [throttling.UserRateThrottle]
    permission_classes = [permissions.AllowAny]

    def post(self, request: rest_request.Request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.data
        phone = data.get("phone")
        # Create pending user
        self.create_user(
            phone,
            data.get("username"),
            data.get("first_name"),
            data.get("last_name"),
            data.get("password"),
            data.get("region"),
            data.get("district"),
        )
        self.send_confirmation(
            phone
        )  # Send confirmation code for sms eskiz.uz
        return response.Response(
            {"detail": _(enums.Messages.SEND_MESSAGE) % {"phone": phone}},
            status=status.HTTP_202_ACCEPTED,
        )


class ConfirmView(views.APIView, services.UserService):
    """Confirm otp code"""

    serializer_class = ConfirmSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=serializer_class,
        summary="Auth confirm.",
        description="Auth confirm user.",
    )
    def post(self, request: rest_request.Request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)

        data = ser.data
        phone, code = data.get("phone"), data.get("code")

        try:
            # Check Sms confirmation otp code
            if services.SmsService.check_confirm(phone, code=code):
                # Create user
                token = self.validate_user(
                    User.objects.filter(phone=phone).first()
                )
                return response.Response(
                    data={
                        "detail": _(enums.Messages.OTP_CONFIRMED),
                        "token": token,
                    },
                    status=status.HTTP_202_ACCEPTED,
                )
        except SmsException as e:
            return response.Response(
                {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )  # Response exception for APIException
        except Exception as e:
            return response.Response(
                {"detail": e}, status=status.HTTP_400_BAD_REQUEST
            )  # Api exception for APIException


class ResetConfirmationCodeView(views.APIView, services.UserService):
    """Reset confirm otp code"""

    serializer_class = ResetConfirmationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request: rest_request.Request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)

        data = ser.data
        code, phone = data.get("code"), data.get("phone")
        try:
            res = services.SmsService.check_confirm(phone, code)
            if res:
                token = models.ResetToken.objects.create(
                    user=User.objects.filter(phone=phone).first(),
                    token=str(uuid.uuid4()),
                )
                return response.Response(
                    data={
                        "token": token.token,
                        "created_at": token.created_at,
                        "updated_at": token.updated_at,
                    },
                    status=status.HTTP_200_OK,
                )
            return response.Response(
                data={"detail": _(enums.Messages.INVALID_OTP)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except exceptions.SmsException as e:
            return response.Response(
                {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return response.Response(
                {"detail": e}, status=status.HTTP_400_BAD_REQUEST
            )


class ResetSetPasswordView(views.APIView, services.UserService):
    serializer_class = sms_serializers.SetPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.data
        token = data.get("token")
        password = data.get("password")
        token = models.ResetToken.objects.filter(token=token)
        if not token.exists():
            return response.Response(
                {"detail": _("Invalid token")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        phone = token.first().user.phone
        token.delete()
        self.change_password(phone, password)
        return response.Response(
            {"detail": _("password updated")}, status=status.HTTP_200_OK
        )


class ResendView(AbstractSendSms):
    """Resend Otp Code"""

    serializer_class = ResendSerializer


class ResetPasswordView(http_views.AbstractSendSms):
    """Reset user password"""

    serializer_class: typing.Type[ResetPasswordSerializer] = (
        ResetPasswordSerializer
    )


class MeView(viewsets.ViewSet):
    """Get user information"""

    serializer_class = UserSerializer

    def get(self, request: rest_request.Request):
        user = request.user
        return response.Response(UserSerializer(user).data)


class MeUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
