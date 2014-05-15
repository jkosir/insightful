from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from accounts.managers import EmailUserManager


class AnalyticsUser(AbstractBaseUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    objects = EmailUserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email