from django.contrib import admin
from .models import UserProfile,Recipe,Meal_plan
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Recipe)
admin.site.register(Meal_plan)
