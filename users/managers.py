from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, username, email, password, **kwargs):
        """
        Create and save a User.

        Args:
            email (string): email_id used by the user
            password (string): password used by the user
            city (string): city of th user
            zip_code (string): zip code of the user
            user_type (string): user can be one of (parent/sitter)
            **kwargs: contaitns dictionary other user fields

        Returns:
            user: current created user

        Raises:
            ValueError: When required fields are missing, it will raised.
        """
        # Ensure that an email address is set
        if not email:
            raise ValueError("Users must have a valid email address.")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=kwargs.get('first_name'),
            last_name=kwargs.get('last_name')
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password=None, **kwargs):
        """
        Create and save a superuser User.

        Used for `python manage.py createsuperuser`
        """

        # create default data for superuser
        user = self.create_user(
            username, email, password, **kwargs)

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

