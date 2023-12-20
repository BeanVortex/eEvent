from django.forms import ModelForm, Form
from django import forms
from .models import OrganizerUser
from .models import AttenderUser


class OrganizerSignupForm(ModelForm):
    class Meta:
        model = OrganizerUser
        fields = "__all__"


class AttenderSignupForm(ModelForm):
    class Meta:
        model = AttenderUser
        fields = "__all__"


class LoginForm(Form):
    username = forms.CharField(label="username")
    password = forms.CharField(label="password", widget=forms.PasswordInput)
