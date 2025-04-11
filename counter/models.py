from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Extended user fields
    age = models.PositiveIntegerField(null=True, blank=True)
    height = models.FloatField(help_text="Height in cm", null=True, blank=True)
    weight = models.FloatField(help_text="Weight in kg", null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'), 
        ('female', 'Female'),
        ('other', 'Other')
    ], null=True, blank=True)
    goals = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    def __str__(self):
        return self.username