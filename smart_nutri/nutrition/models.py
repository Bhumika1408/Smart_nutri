from django.db import models
import datetime

# Create your models here.
class UserProfile(models.Model):
    FAMILY_HISTORY_CHOICES=(
        ('diabetic','Diabetic'),
        ('non_diabetic','Non Diabetic')
    )
    DIET_CHOI = [
        ('vegetarian', 'Vegetarian'),
        ('non vegetarian', 'Non Vegetarian'),
        ('vegan', 'Vegan'),
    ]
    PHYSICAL_ACTIVITY_CHOICES = [
    ('sedentary', 'Sedentary (Minimal movement, mostly sitting)'),
    ('low_active', 'Low active (Light physical activity, occasional exercise)'),
    ('active', 'Active (Regular exercise, moderate physical activity)'),
    ('very_active', 'Very active (Intense daily physical activity or workouts)'),
]
    HEALTH_CHOICES=[
        ('diabetes','Diabetes'),
        ('cardiovacular','Cardivascular')
    ]

    name = models.CharField(max_length=50)
    age = models.IntegerField()
    height = models.IntegerField()  # Height in cm
    weight = models.FloatField()  # Weight in kg
    daily_insulin_level = models.FloatField(null=True, blank=True)
    health_condition_preferences=models.CharField(
        max_length=20,
        choices=HEALTH_CHOICES,
        null=True,
        blank=True
    )
    dietary_preferences = models.CharField(
        max_length=20,
        choices=DIET_CHOI,
        null=True,
        blank=True)
    family_history = models.CharField(
        max_length=20,
        choices=FAMILY_HISTORY_CHOICES,
        null=True,
        blank=True
    )

    physical_activity = models.CharField(max_length=20,choices=PHYSICAL_ACTIVITY_CHOICES, null=True, blank=True)
    alcohol_use = models.BooleanField(default=False)
    health_report = models.ImageField(upload_to='health_reports/', null=True, blank=True)

    def __str__(self):
        return self.name




class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    region = models.CharField(max_length=100, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    recipes_images = models.ImageField(upload_to='recipes_images/', null=True, blank=True)

    TYPE_OF_MEAL_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    type_of_meal = models.CharField(
        max_length=20,
        choices=TYPE_OF_MEAL_CHOICES,
        null=True,
        blank=True,
    )

    # Add the diet field
    DIET_CHOICES = [
        ('diabetic friendly', 'Diabetic Friendly'),
        ('vegetarian', 'Vegetarian'),
        ('non vegetarian', 'Non Vegetarian'),
        ('vegan', 'Vegan'),
    ]
    diet = models.CharField(
        max_length=50,
        choices=DIET_CHOICES,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


#Ingredients

class Meal_plan(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date=models.DateField(default=datetime.datetime.today)
    recipes = models.ManyToManyField(Recipe)

    # Field for ingredient substitutions
    #ingredient_substitutions = models.JSONField(null=True, blank=True)

    def __str__(self):
    
        return 'Meal Plan for {} on {}'.format(self.user.user.username, self.date)

