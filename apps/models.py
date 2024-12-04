from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
from django.db.models import EmailField, BooleanField, Model, CharField, DateTimeField, ImageField, SlugField
from django.db.models import TextChoices, Model
from django.utils.text import slugify

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


class Books(Model):
    name = CharField(max_length=255)
    image = ImageField(upload_to='book_image/', blank=True, null=True)
    # size = PositiveIntegerField(default=0, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)
    slug = SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            original_slug = self.slug
            counter = 1
            while self.__class__.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name