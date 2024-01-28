from django.forms import Form
from django import forms
style_classes = "border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 mb-2 dark:focus:border-blue-500"


class OrganizerSignupForm(Form):
    firstName = forms.CharField(label="نام",widget=forms.TextInput(attrs={
        "class": style_classes
    }))
    lastName = forms.CharField(label="نام خانوادگی", widget=forms.TextInput(attrs={
        "class": style_classes
    }))
    email = forms.EmailField(label="ایمیل", widget=forms.EmailInput(attrs={
        "class": style_classes
    }))
    phone = forms.CharField(label="شماره همراه",widget=forms.NumberInput(attrs={
        "placeholder": "09123456789",
        "class": style_classes
    }))
    address = forms.CharField(label="آدرس فروشگاه", widget=forms.TextInput(attrs={
        "class": style_classes
    }))
    meli = forms.CharField(label="کد ملی",widget=forms.NumberInput(attrs={
        "placeholder": "136*****",
        "class": style_classes
    }))
    username = forms.CharField(label="نام کاربری",widget=forms.TextInput(attrs={
        "placeholder": "ross_bob",
        "class": style_classes
    }))
    password = forms.CharField(label="رمز عبور",widget=forms.PasswordInput(attrs={
        "class": style_classes
    }))


class AttenderSignupForm(Form):
    firstName = forms.CharField(label="نام",widget=forms.TextInput(attrs={
        "class": style_classes
    }))
    lastName = forms.CharField(label="نام خانوادگی",widget=forms.TextInput(attrs={
        "class": style_classes
    }))
    email = forms.EmailField(label="ایمیل",widget=forms.EmailInput(attrs={
        "class": style_classes
    }))
    phone = forms.CharField(label="شماره همراه",widget=forms.NumberInput(attrs={
        "placeholder": "09123456789",
        "class": style_classes
    }))
    meli = forms.CharField(label="کد ملی",widget=forms.NumberInput(attrs={
        "placeholder": "136*****",
        "class": style_classes
    }))
    images = forms.FileField(label="عکس گواهینامه", required=False, widget=forms.FileInput(attrs={
        "class" : style_classes
    }))
    username = forms.CharField(label="نام کاربری",widget=forms.TextInput(attrs={
        "placeholder": "ross_bob",
        "class": style_classes
    }))
    address = forms.CharField(label="آدرس", widget=forms.TextInput(attrs={
        "class": style_classes
    }))
    password = forms.CharField(label="رمز عبور",widget=forms.PasswordInput(attrs={
        "class": style_classes
    }))
