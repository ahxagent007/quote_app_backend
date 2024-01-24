from django.db import models
from django.utils.translation import gettext_lazy
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser

class CustomUser(BaseUserManager):
    def create_superuser(self, password, **other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')

        other_fields.setdefault('role', 'ADMIN')
        return self.create_user(password, **other_fields)

    def create_user(self, password=None, **other_fields):

        other_fields.setdefault('is_active', True)
        user.set_password(password)
        user.save()
        return user


class user(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, null=False, unique=True)
    phone_model = models.CharField(max_length=255, null=False, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUser()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_model']

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

class otp(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, null=False, unique=True)
    otp = models.CharField(max_length=255, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
