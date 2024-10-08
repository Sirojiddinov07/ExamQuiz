import typing
from datetime import datetime

from django.contrib.auth import hashers
from rest_framework_simplejwt import tokens

import exceptions
from account import models
from services import base_service, sms
from utils import exception


class UserService(base_service.BaseService, sms.SmsService):
    def get_token(self, user):
        refresh = tokens.RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def create_user(self, phone, username, first_name,  last_name, password, region, district):
        models.User.objects.update_or_create(
            phone=phone,
            defaults={
                "phone": phone,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "region": region,
                "district": district,
                "password": hashers.make_password(password),
            },
        )

    def send_confirmation(self, phone) -> bool:
        try:
            self.send_confirm(phone)
            return True
        except exceptions.SmsException as e:
            exception.ResponseException(
                e, data={"expired": e.kwargs.get("expired")}
            )  # noqa
            return False
        except Exception as e:
            exception.ResponseException(e)
            return False

    def validate_user(self, user: typing.Union[models.User]) -> dict:
        """
        Create user if user not found
        """
        user.validated_at = datetime.now()
        user.save()
        token = self.get_token(user)
        return token

    def is_validated(self, user: typing.Union[models.User]) -> bool:
        """
        User is validated check
        """
        if user.validated_at is not None:
            return True
        return False

    def change_password(self, phone, password):
        """
        Change password
        """
        user = models.User.objects.filter(phone=phone).first()
        user.set_password(password)
        user.save()
