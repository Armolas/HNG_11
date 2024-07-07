from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import uuid

class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("Please enter a valid email address")

    def create_user(self, email, firstName, lastName, password, **extra_fields):
        from .models import Organisation
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError("an email is required")
        if not firstName:
            raise ValueError("first name is required")
        if not lastName:
            raise ValueError("last name is required")
        if not password:
            raise ValueError("password is required")
        userId = uuid.uuid4()
        user = self.model(userId=userId, email=email, firstName=firstName, lastName=lastName, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        org_name = f"{user.firstName}'s Organisation"
        org = Organisation.objects.create(org_name)
        org.users.add(user)
        org.save()
        return user

    def create_superuser(self, email, firstName, lastName, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('is staff must be true for admin user')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is superuser must be true for admin user')

        user = self.create_user(email, firstName, lastName, password, **extra_fields)
        user.save(using=self._db)
        return user

class OrgManager(models.Manager):
    def create(self, name, **extra_fields):
        if not name:
            raise ValueError("Organisation name is required")
        orgId = uuid.uuid4()
        org = self.model(orgId=orgId, name=name, **extra_fields)
        org.save(using=self._db)
        return org
