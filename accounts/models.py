# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.base_user import (BaseUserManager, AbstractBaseUser)


# Create your models here.

class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        """
            Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """docstring for User"""

    email = models.EmailField(verbose_name='email address', max_length=225, unique=True)
    pseudo = models.CharField(verbose_name='pseudo', max_length=30, blank=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    phone_number = models.CharField(verbose_name='phone number', max_length=8, default='+225 00 000 000')
    is_active = models.BooleanField(verbose_name='active', default=True)
    is_admin = models.BooleanField(verbose_name='administrateur', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'account'
        verbose_name_plural = 'accounts'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_short_name(self):
        '''Returns the short name for the user.'''
        return self.pseudo

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''Sends an email to this User.'''
        send_mail(subject, message, from_email, [self.email], **kwargs)
