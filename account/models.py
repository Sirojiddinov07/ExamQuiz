import math
from datetime import datetime, timedelta

from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.translation import gettext_lazy as _
from account.managers import UserManager


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




class District(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
class RoleChoice(models.TextChoices):
    """
    User Role Choice
    """

    SUPERUSER = "superuser", _("Superuser")
    ADMIN = "admin", _("Admin")
    USER = "user", _("User")

class User(auth_models.AbstractUser):
    phone = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(
        max_length=255,
        choices=RoleChoice,
        default=RoleChoice.USER,
    )
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        auth_models.Group,
        related_name='account_user_set',  # Update related_name for groups
        blank=True,
        help_text=_('The groups this user belongs to.'),
    )
    user_permissions = models.ManyToManyField(
        auth_models.Permission,
        related_name='account_user_permissions_set',  # Update related_name for user_permissions
        blank=True,
        help_text=_('Specific permissions for this user.'),
    )
    USERNAME_FIELD = "phone"
    objects = UserManager()

    def __str__(self):
        return self.phone


class SmsConfirm(models.Model):
    SMS_EXPIRY_SECONDS = 120
    RESEND_BLOCK_MINUTES = 10
    TRY_BLOCK_MINUTES = 2
    RESEND_COUNT = 5
    TRY_COUNT = 10

    code = models.IntegerField()
    try_count = models.IntegerField(default=0)
    resend_count = models.IntegerField(default=0)
    phone = models.CharField(max_length=20)
    expire_time = models.DateTimeField(null=True, blank=True)
    unlock_time = models.DateTimeField(null=True, blank=True)
    resend_unlock_time = models.DateTimeField(null=True, blank=True)

    def sync_limits(self):
        if self.resend_count >= self.RESEND_COUNT:
            self.try_count = 0
            self.resend_count = 0
            self.resend_unlock_time = datetime.now() + timedelta(
                minutes=self.RESEND_BLOCK_MINUTES
            )
        elif self.try_count >= self.TRY_COUNT:
            self.try_count = 0
            self.unlock_time = datetime.now() + timedelta(
                minutes=self.TRY_BLOCK_MINUTES
            )

        if (
            self.resend_unlock_time is not None
            and self.resend_unlock_time.timestamp()
            < datetime.now().timestamp()
        ):
            self.resend_unlock_time = None

        if (
            self.unlock_time is not None
            and self.unlock_time.timestamp() < datetime.now().timestamp()
        ):
            self.unlock_time = None
        self.save()

    def is_expired(self):
        return (
            self.expire_time.timestamp() < datetime.now().timestamp()
            if hasattr(self.expire_time, "timestamp")
            else None
        )

    def is_block(self):
        return self.unlock_time is not None

    def reset_limits(self):
        self.try_count = 0
        self.resend_count = 0
        self.unlock_time = None

    def interval(self, time):
        expire = time.timestamp() - datetime.now().timestamp()
        minutes = math.floor(expire / 60)
        expire -= minutes * 60
        expire = math.floor(expire)

        return f"{minutes:02d}:{expire:02d}"

    def __str__(self) -> str:
        return f"{self.phone} | {self.code}"
