from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class EmailUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email (as username) and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_active=True, last_login=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, **extra_fields)
