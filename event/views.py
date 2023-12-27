from django.shortcuts import redirect, render, HttpResponse
from django.views import View

from authorize.models import OrganizerUser
from .models import Event, Discount
from .forms import DiscountForm, NewEventForm
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

def index(req):
    return HttpResponse("Event index")


class AddEventOrganizer(View):
    def get(self, req):
        # todo check if user is organizer
        form = NewEventForm()
        return render(req, "event/event_new.html", {"form": form})
    

    def post(self, req):
        form = NewEventForm(req.POST)
        if form.is_valid():
            # todo check if user is organizer
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            location= form.cleaned_data["location"]
            price = form.cleaned_data["price"]
            start_date = form.cleaned_data["start_date"]
            start_time = form.cleaned_data["start_time"]
            starts_on = datetime.combine(start_date, start_time)
            aware_datetime = timezone.make_aware(starts_on)
            capacity = form.cleaned_data["capacity"]
            orgId = req.user.id
            orgUser = OrganizerUser.objects.get(user_id=orgId)
            event = Event(title=title, description=description, location=location, price=price, starts_on=aware_datetime, capacity=capacity, organizer_user=orgUser)
            event.save()
        return redirect("event_index")

def organizerEvents(req, oid):
    events = Event.objects.all().values().filter(organizer_user=oid)
    return render(req, "event/event_list.html", {"events": events})


def viewEventAsOrganizer(req, orgId, eid):
    pass


class AddDiscount(View):
    def get(self, req):
        form = DiscountForm()
        return render(req, 'event/discount_form.html', {'form': form})
    
    def post(self, req):
        form = DiscountForm(req.POST)
        try:
            if form.is_valid():
                title = form.cleaned_data["title"]
                code = form.cleaned_data["code"]
                percentage = form.cleaned_data["percentage"]
                rate_limit = form.cleaned_data["rate_limit"]
                end_date = form.cleaned_data["end_date"]
                end_time = form.cleaned_data["end_time"]
                valid_until = datetime.combine(end_date, end_time)
                aware_datetime = timezone.make_aware(valid_until)
                eventId = form.cleaned_data["event"]
                event = Event.objects.get(id=eventId)
                discount = Discount(title=title, code=code, percentage=percentage, valid_until=aware_datetime,
                                    rate_limit=rate_limit, event=event)
                discount.save()
                return render(req, 'event/discount_form.html', {'form': form, "status": "success"})
            else:
                return render(req, 'event/discount_form.html', {'form': form, "status": "fail"})
        except Exception as e:
            return render(req, 'event/discount_form.html', {'form': form, "status": "fail", "message": str(e)})


def deleteDiscount(req, did):
    pass


class EditEventOrganizer(View):
    def get(self, req):
        pass

    def post(self, req):
        pass


def deleteEventOrganizer(req, eid):
    # todo get user data from authentication
    pass


def addEventAttender(req, eid):
    # todo get user data from authentication
    pass


def deleteEventFromAttender(req, eid):
    # todo get user data from authentication
    pass


def applyDiscount(req, eid):
    # todo get discount data from req
    pass


def viewEvent(req, eid):
    event = Event.objects.get(pk=eid)
    return render(req, "event/event_details.html", {"event": event})


def searchByTitle(req):
    pass


def viewAllEvents(req):
    events = Event.objects.all().values()
    return render(req, "event/event_list.html", {"events": events})
