from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# Meal time choices for FoodLog model
MEAL_TIME_CHOICES = [
    ('breakfast', 'Breakfast'),
    ('lunch', 'Lunch'),
    ('dinner', 'Dinner'),
    ('snack', 'Snack'),
]

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    height = models.FloatField(help_text="Height in cm", null=True, blank=True)
    weight = models.FloatField(help_text="Weight in kg", null=True, blank=True)
    gender = models.CharField(
        max_length=20,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
            ('prefer_not_to_say', 'Prefer not to say')
        ],
        null=True,
        blank=True
    )
    goals = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    gender = models.CharField(
        max_length=20,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
            ('prefer_not_to_say', 'Prefer not to say')
        ],
        null=True,
        blank=True
    )
    calorie_goal = models.PositiveIntegerField(default=2000)
    protein_goal = models.PositiveIntegerField(default=50)
    carb_goal = models.PositiveIntegerField(default=300)
    fat_goal = models.PositiveIntegerField(default=70)
    sodium_goal = models.PositiveIntegerField(default=2300)  # Default 2300mg (FDA recommendation)
    sugar_goal = models.PositiveIntegerField(default=25)     # Default 25g (WHO recommendation)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    water_goal = models.PositiveIntegerField(default=8)      # Default 8 glasses

    def __str__(self):
        return self.user.username

class FoodLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=255)
    calories = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()
    sodium = models.PositiveIntegerField(default=0)  # in milligrams
    sugar = models.PositiveIntegerField(default=0)   # in grams
    amount = models.FloatField(help_text="Amount in grams")
    meal_time = models.CharField(max_length=20, choices=MEAL_TIME_CHOICES, default='snack')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']  # Newest entries first by default
        verbose_name = 'Food Log'
        verbose_name_plural = 'Food Logs'

    def __str__(self):
        return f"{self.food_name} ({self.amount}g) - {self.user.username}"

class WaterIntake(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Water intake at {self.date}"

# Automatically create and save Profile when a CustomUser is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()