from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
from django.db.models import EmailField, BooleanField, Model, CharField, DateTimeField
from django.db.models import TextChoices, Model

from apps.managers import CustomUserManager


class User(AbstractUser):
    class Type(TextChoices):
        OPERATOR = 'operator', 'Operator'
        ADMIN = 'admin_side', 'Admin_side'
        USER = 'user', 'User'

    username = None
    first_name = None
    last_name = None
    email = EmailField(unique=True)
    name = CharField(max_length=255)
    is_active = BooleanField(default=False)
    reset_token = CharField(max_length=64, null=True, blank=True)
    type = CharField(max_length=25, choices=Type.choices, default=Type.USER, verbose_name="user type")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
