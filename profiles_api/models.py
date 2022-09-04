from warnings import catch_warnings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """ Manager for user profiles """

    def create_user(self, email, name, password=None):
        """ Create a new user profile """

        # Check if email value was passed in 
        if not email:
            raise ValueError("User mus have an email address")
        
        # Making the domain part lower cased
        email = self.normalize_email(email)

        # Creates a user with corresponding to User's email & name
        user = self.model(email=email, name=name)

        # Encrypted Password saved to the user's model
        user.set_password(password)
        user.save(using=self.db)

        return user
    
    def create_superuser(self, email, name, password):
        """ Create and save a new superuser with given details """
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Database model for user's in the system """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    # TO SEE IF USER IS ACTIVATED
    is_active = models.BooleanField(default=True)
    # IF USER IS STAFF AKA MOD
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    # Overwritting the placeholder of the form
    USERNAME_FIELD = 'email'

    # Required Form Field
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """ Retrieve full name of User """
        return self.name

    def get_short_name(self):
        """ Retrieve short name of User """
        return self.name

    def __str__(self):
        """ Return string representation of our user """
        return self.email





