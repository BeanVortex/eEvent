from django.forms import Form
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'
class NewEventForm(Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Awesome Event",
        "class" : "mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        "placeholder": "Description for Awesome Event",
        "class" : "mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
    }))
    location = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Location of Awesome Event",
        "class" : "mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
    }))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={
        "class" : "mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
    }))
    start_date = forms.DateField(widget=DateInput(attrs={
        "class" : "mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"    }))
    start_time = forms.TimeField(widget=TimeInput(attrs={
        "class" : "mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"    }))
    capacity = forms.IntegerField(widget=forms.NumberInput(attrs={
        "placeholder": "Determine capacity of event",
        "class" : "mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
    }))
