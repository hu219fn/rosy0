from django.contrib.auth import forms as formsAuth
from django.contrib.auth.models import User

class SignupForm(formsAuth.UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']