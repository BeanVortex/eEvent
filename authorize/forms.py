from django.forms import Form
from django import forms
style_classes = "border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 mb-2 dark:focus:border-blue-500"


class OrganizerSignupForm(Form):
    firstName = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Bob",
        "class": style_classes
    }))
    lastName = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Ross",
        "class": style_classes
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "placeholder": "ross_bob@mail.com",
        "class": style_classes
    }))
    phone = forms.CharField(widget=forms.NumberInput(attrs={
        "placeholder": "09123456789",
        "class": style_classes
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "ross_bob",
        "class": style_classes
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": style_classes
    }))


class AttenderSignupForm(Form):
    firstName = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Bob",
        "class": style_classes
    }))
    lastName = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Ross",
        "class": style_classes
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "placeholder": "ross_bob@mail.com",
        "class": style_classes
    }))
    phone = forms.CharField(widget=forms.NumberInput(attrs={
        "placeholder": "09123456789",
        "class": style_classes
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "ross_bob",
        "class": style_classes
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": style_classes
    }))
    multiple = forms.BooleanField(label="Multiple users", required=False, widget=forms.CheckboxInput(attrs={
        "class": "w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-blue-600 dark:ring-offset-gray-800"
    }))
