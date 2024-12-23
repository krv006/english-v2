from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db.models import EmailField, BooleanField, Model, CharField, DateTimeField, ImageField, SlugField, \
    FileField, ForeignKey, CASCADE
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


class Units(Model):
    name = CharField(max_length=255)
    book = ForeignKey('apps.Books', CASCADE, related_name='units')
    file = FileField(upload_to='units_files/', validators=[
        FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'txt'])
    ])

    def __str__(self):
        return f"Unit: {self.name} (Book: {self.book.name})"


class Test(Model):
    en = CharField(max_length=255)
    uz = CharField(max_length=255)
    audio_file = FileField(upload_to='test_audio/', validators=[
        FileExtensionValidator(allowed_extensions=['mp3', 'wav'])
    ])
    unit = ForeignKey('apps.Units', CASCADE, related_name='tests')

    def __str__(self):
        return f"Test in English: {self.en} (Unit: {self.unit.name})"


class AdminSiteSettings(Model):
    created_by = ImageField(upload_to='created_by/')
    connection = CharField(max_length=255)
