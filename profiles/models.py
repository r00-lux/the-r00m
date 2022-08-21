from lib2to3.pytree import Base
from pyexpat import model
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)


class ProfileManager(BaseUserManager):
    def create_user(self, username, password):
        if not username:
            raise ValueError('Username required.')

        user = self.model(username=username)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class Profile(AbstractBaseUser, PermissionsMixin):
    """Model for user."""
    # email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = ProfileManager()

    USERNAME_FIELD = 'username'

    # REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username
