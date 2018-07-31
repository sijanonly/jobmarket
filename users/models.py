# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

# from bookings.models import Address

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Model to create a User.

    :id: User uuid.
    :username: Username of the user.
    :email: User email.
    :first_name: User first name.
    :last_name: User last name.
    :numbers: User's primary and emergency phone numbers.
    :user_type: Whether the User is a parent or a sitter.
    :date_created: User creation date.
    :date_modified: User modified date.
    :is_admin: Whether or not the User is of admin status.
    :is_superuser: Whether or not the User is of superuser status.
    :is_staff: Whether or not the User is of staff status.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)

    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)

    avatar = models.URLField(max_length=500, blank=True, null=True)

    is_owner = models.BooleanField('project owner status', default=False)
    is_freelancer = models.BooleanField('freelancer status', default=False)

    # user_type = models.CharField(max_length=7, choices=CHOICES, default=OWNER)

    has_payment = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['first_name', 'last_name']
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        """
        Instance method to get full name of a User.
        """
        if self.first_name:
            first_name = ' '.join(
                [i.capitalize() for i in self.first_name.split(' ')])
            last_name = ' '.join(
                [i.capitalize() for i in self.last_name.split(' ')
                 if self.last_name])
            full_name = [first_name, last_name]
            full_name = ' '.join(
                [i.strip() for i in full_name if i.strip()])
            return full_name
        else:
            return "%s" % (self.email)

    