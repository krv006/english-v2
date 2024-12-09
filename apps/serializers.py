from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework.fields import EmailField, CharField
from rest_framework.serializers import ModelSerializer, Serializer

from apps.models import User, Books, Units, AdminSiteSettings, Test


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')  # Eslatma: bu yerda qavslar kiritildi

        # Tavsiya qilinmaydi, lekin agar vaqtincha kerak bo'lsa:
        # todo bunda write_only bolganda yoziladi lekin post va get qilganda korinmaydi swaggerda
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }

        # todo bunda read_only bolgani uchun faqat korsa boladi va ozgartirish kiritib bolmaydi
        # extra_kwargs = {
        #     "password": {
        #         "read_only": True,
        #     }
        # }

    def validate(self, attrs):
        password = attrs.get('password')
        if password:
            attrs['password'] = make_password(password)  # 'password' string sifatida ishlatiladi
        return super().validate(attrs)


class BooksModelSerializer(ModelSerializer):
    class Meta:
        model = Books
        exclude = ("slug", "created_at")


class UnitsModelSerializer(ModelSerializer):
    class Meta:
        model = Units
        fields = '__all__'

    def to_representation(self, instance: Units):
        repr = super().to_representation(instance)
        repr['book'] = BooksModelSerializer(instance.book, context=self.context).data
        return repr


class AdminSiteSettingsModelSerializer(ModelSerializer):
    class Meta:
        model = AdminSiteSettings
        fields = '__all__'


class TestModelSerializer(ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

    def to_representation(self, instance: Test):
        repr = super().to_representation(instance)
        repr['unit'] = UnitsModelSerializer(instance.unit, context=self.context).data
        return repr


# Register serializer
class RegisterSerializer(ModelSerializer):
    password = CharField(write_only=True)
    confirm_password = CharField(write_only=True)

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'password', 'confirm_password',

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


class LoginUserModelSerializer(Serializer):
    email = EmailField()
    password = CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            raise ValidationError("Invalid email or password")

        if not user.check_password(password):
            raise ValidationError("Invalid email or password")

        attrs['user'] = user
        return attrs


class LoginSerializer(Serializer):
    email = EmailField()
    verification_code = CharField(write_only=True)
