from django.forms import Form
from django import forms
from .models import Event

style_classes = "mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'
    
class EventForm(Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Awesome Event",
        "class" : style_classes
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        "placeholder": "Description for Awesome Event",
        "class" : style_classes
    }))
    location = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Location of Awesome Event",
        "class" : style_classes
    }))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={
        "class" : style_classes
    }))
    start_date = forms.DateField(widget=DateInput(attrs={
        "class" : style_classes 
        }))
    start_time = forms.TimeField(widget=TimeInput(attrs={
        "class" : style_classes
        }))
    capacity = forms.IntegerField(widget=forms.NumberInput(attrs={
        "placeholder": "Determine capacity of the event",
        "class" : style_classes
    }))


class DiscountForm(Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Discount Title",
        "class" : style_classes
    }))
    code = forms.CharField(widget=forms.Textarea(attrs={
        "placeholder": "Discount code",
        "class" : style_classes
    }))
    percentage = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class" : style_classes
    }))
    end_date = forms.DateField(widget=DateInput(attrs={
        "class" : style_classes 
        }))
    end_time = forms.TimeField(widget=TimeInput(attrs={
        "class" : style_classes
        }))
    rate_limit = forms.IntegerField(widget=forms.NumberInput(attrs={
        "placeholder": "Determine capacity of the discount",
        "class" : style_classes
    }))
    event = forms.ChoiceField(choices=[], widget=forms.Select(attrs={
        'class': 'form-select '+ style_classes
    }))

    def __init__(self, *args, **kwargs):
        super(DiscountForm, self).__init__(*args, **kwargs)
        events = Event.events.all()
        event_choices = [(event.id, event.title) for event in events]
        self.fields['event'].choices = event_choices
