# translation_api/models.py

from django.db import models

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