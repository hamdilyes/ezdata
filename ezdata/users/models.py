from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone


class MyAccountManager(BaseUserManager):
    def create_user(self, email, entite, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, entite=entite,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, entite, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, entite=entite,
                          is_superuser=True,
                          is_staff=True, is_admin=True, **other_fields)
        user.set_password(password)
        user.save()
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    entite = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['entite']

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Utilisateur'

    def __str__(self):
        return self.email
