from django.forms import Form
from django import forms
from .models import Event

style_classes = "mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'
    
class EventForm(Form):
    title = forms.CharField(label="عنوان:", widget=forms.TextInput(attrs={
        "class" : style_classes
    }))
    description = forms.CharField(label="توضیحات", widget=forms.Textarea(attrs={
        "class" : style_classes
    }))
    price = forms.DecimalField(label="قیمت:", widget=forms.NumberInput(attrs={
        "class" : style_classes
    }))
    capacity = forms.IntegerField(label="تعداد", widget=forms.NumberInput(attrs={
        "class" : style_classes
    }))
    images = forms.FileField(required=False, label="عکس قطعه", widget=forms.FileInput(attrs={
        "class" : style_classes
    }))


class DiscountForm(Form):
    title = forms.CharField(label="عنوان", widget=forms.TextInput(attrs={
        "class" : style_classes
    }))
    code = forms.CharField(label="کد تخفیف", widget=forms.Textarea(attrs={
        "class" : style_classes
    }))
    percentage = forms.IntegerField(label="درصد", widget=forms.NumberInput(attrs={
        "class" : style_classes
    }))
    end_date = forms.DateField(label="تاریخ انقضا", widget=DateInput(attrs={
        "class" : style_classes 
        }))
    end_time = forms.TimeField(label="زمان انقضا", widget=TimeInput(attrs={
        "class" : style_classes
        }))
    rate_limit = forms.IntegerField(label="تعداد", widget=forms.NumberInput(attrs={
        "placeholder": "Determine capacity of the discount",
        "class" : style_classes
    }))
    event = forms.ChoiceField(choices=[], label="برای قطعه:", widget=forms.Select(attrs={
        'class': 'form-select '+ style_classes
    }))

    def __init__(self, oid, *args, **kwargs):
        super(DiscountForm, self).__init__(*args, **kwargs)
        events = Event.events.getAllByOrganizer(oid)
        event_choices = [(event.id, event.title) for event in events]
        self.fields['event'].choices = event_choices
