from django import forms
from .models import UserProfile

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']
