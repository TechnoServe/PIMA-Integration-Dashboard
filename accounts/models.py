from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, **other_fields):

        if not email:
            raise ValueError("Please, Provide the email")
        email = self.normalize_email(email)
        user =  self.model(email=email, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **other_fields):
        other_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **other_fields)

    def create_superuser(self, email, password=None, **other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **other_fields)



class User(AbstractBaseUser, PermissionsMixin):

    ORGANIZATIONS = (
        ('ORG1','ORG1'),
        ('ORG2','ORG2'),
        ('ORG3','ORG3'),
    )
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True ,blank=True)
    organization = models.CharField(null=True, blank=True, choices=ORGANIZATIONS, max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    objects =  CustomUserManager()

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []    

    def __str__(self):
        return self.email