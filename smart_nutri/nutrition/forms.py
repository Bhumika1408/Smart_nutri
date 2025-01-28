from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'name', 'age', 'height', 'weight', 'daily_insulin_level','health_condition_preferences',
            'dietary_preferences', 'family_history', 'physical_activity',
            'alcohol_use',  'health_report'
        ]
