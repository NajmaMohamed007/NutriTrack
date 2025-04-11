from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'profile_picture')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('age', 'height', 'weight', 'gender', 'goals')
        widgets = {
            'goals': forms.Textarea(attrs={'rows': 3}),
        
        }