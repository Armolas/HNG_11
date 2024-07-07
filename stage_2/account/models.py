from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager, OrgManager
# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    userId = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True, null=False, verbose_name='Email Address')
    firstName = models.CharField(max_length=100, verbose_name='First Name')
    lastName = models.CharField(max_length=100, verbose_name='Last Name')
    phone = models.CharField(max_length=30, verbose_name='Phone Number')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD='email'

    REQUIRED_FIELDS= ["firstName", "lastName"]

    objects = UserManager()

    @property
    def get_full_name(self):
        return f"{self.firstName} {self.lastName}"

    def __str__(self):
        return self.email

class Organisation(models.Model):
    orgId = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField()
    users = models.ManyToManyField(User, related_name='organisations')
    
    REQUIRED_FIELDS = ['name']

    objects = OrgManager()

    def __str__(self):
        return self.name
