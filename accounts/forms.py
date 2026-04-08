from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
import re

User = get_user_model()

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone_number", "password1", "password2"]
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            raise forms.ValidationError("Le nom d'utilisateur ne peut contenir que des caractères alphanumériques, des underscores (_) ou des tirets (-).")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée.")
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not re.match(r'^[a-zA-Z-]+$', first_name):
            raise forms.ValidationError("Le prénom ne peut contenir que des lettres ou des tirets (-).")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not re.match(r'^[a-zA-Z-]+$', last_name):
            raise forms.ValidationError("Le nom de famille ne peut contenir que des lettres ou des tirets (-).")
        return last_name