from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)


class UserManager(BaseUserManager):
    """Manager for Profiles."""
    def create_user(self, username, email, password=None, **extra_fields):
        """Create and return a new user."""
        if not username:
            raise ValueError('Username is required.')

        user = self.model(username=username,
                          email=self.normalize_email(email),
                          **extra_fields)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        """Create and return a new superuser."""
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Model for user."""
    username = models.CharField(max_length=25, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)

    # Auto-set new users to active.
    is_active = models.BooleanField(default=True)

    # Controls user access to the Django admin panel.
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username
