from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'gender', 'city', 'budget', 'cleanliness',
            'sleep_schedule', 'introvert_extrovert',
            'bio', 'profile_pic'
        ]
