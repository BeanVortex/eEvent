from django.shortcuts import redirect, render, HttpResponse
from django.views import View

from authorize.models import OrganizerUser
from .models import Event, Discount
from .forms import NewEventForm
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

def organizerEvents(req):
    pass


def viewEventAsOrganizer(req, orgId, eid):
    pass


def addDiscount(req, eid):
    pass


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
    pass
