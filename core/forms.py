from django import forms
from django.contrib.auth.models import User
from .models import Feedback, Profile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['city', 'latitude', 'longitude', 'gender','college_id', 'budget', 'cleanliness', 'sleep_schedule', 'introvert_extrovert', 'bio', 'profile_pic']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }