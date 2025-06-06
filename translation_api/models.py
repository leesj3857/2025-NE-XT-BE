# translation_api/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class Category(models.Model):
    korean = models.CharField(max_length=255, unique=True)
    english = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.korean} → {self.english}"

class RegionName(models.Model):
    korean = models.CharField(max_length=100, unique=True)
    english = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.english} -> {self.korean}"
    
class CategoryLog(models.Model):
    korean = models.CharField(max_length=255)
    called_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.korean} at {self.called_at}"

class RegionLog(models.Model):
    english = models.CharField(max_length=255)
    called_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.english} at {self.called_at}"

class PlaceInfo(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    title = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    menu_or_ticket_info = models.JSONField(null=True, blank=True)
    price = models.CharField(max_length=50, null=True, blank=True)
    translated_reviews = models.JSONField(null=True, blank=True)

    class Meta:
        unique_together = ('name', 'address')

    def __str__(self):
        return f"{self.name} - {self.address}"


class PlaceLog(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    called_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} / {self.address} at {self.called_at}"

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

class EmailVerification(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=20)  # 'register' or 'reset'
    token = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)