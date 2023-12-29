from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from authorize.models import OrganizerUser, AttenderUser
from .models import Event, Discount
from .forms import DiscountForm, NewEventForm
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone


class AddEventOrganizer(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/auth/login"
    permission_required = "event.add_event"

    def get(self, req):
        form = NewEventForm()
        return render(req, "event/event_new.html", {"form": form})

    def post(self, req):
        form = NewEventForm(req.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            location = form.cleaned_data["location"]
            price = form.cleaned_data["price"]
            start_date = form.cleaned_data["start_date"]
            start_time = form.cleaned_data["start_time"]
            starts_on = datetime.combine(start_date, start_time)
            aware_datetime = timezone.make_aware(starts_on)
            capacity = form.cleaned_data["capacity"]
            orgId = req.user.id
            orgUser = OrganizerUser.objects.get(user_id=orgId)
            event = Event(title=title, description=description, location=location, price=price,
                          starts_on=aware_datetime, capacity=capacity, organizer_user=orgUser)
            event.save()
        return redirect("event_index")


@login_required(login_url="/auth/login")
def organizerEvents(req):
    organizer = get_object_or_404(OrganizerUser, user_id=req.user.id)
    events = Event.objects.filter(organizer_user=organizer)
    return render(req, "event/event_list.html", {"events": events, "organizer_name": organizer.user.first_name + " " + organizer.user.last_name})


def viewOrganizerEventsById(req, oid):
    organizer = OrganizerUser.objects.get(id=oid)
    events = Event.objects.filter(organizer_user=organizer)
    return render(req, "event/event_list.html", {"events": events, "organizer_name": organizer.user.first_name + " " + organizer.user.last_name})


class AddDiscount(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/auth/login/"
    permission_required = "event.add_discount"

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


@login_required(login_url="/auth/login/")
def attenderEvents(req):
    attender_user = get_object_or_404(AttenderUser, user_id=req.user.id)
    events = attender_user.events.all()
    return render(req, "event/event_list.html", {"events": events})


def viewEvent(req, eid):
    event = Event.objects.get(pk=eid)
    if req.method == "POST" and req.user.is_authenticated:
        try:
            attender_user = get_object_or_404(
                AttenderUser, user_id=req.user.id)
            if attender_user.events.filter(id=eid).exists():
                raise Exception("You have already attended in this event")
            attender_user.events.add(event)
        except Exception as e:
            return render(req, "event/event_details.html", {"event": event, "status": "fail", "message": str(e)})

        return render(req, "event/event_details.html", {"event": event, "status": "success"})
    return render(req, "event/event_details.html", {"event": event})


def viewAllEvents(req):
    events = Event.objects.all()
    return render(req, "event/event_list.html", {"events": events})


@login_required(login_url="/auth/login")
@permission_required(perm="event.delete_discount")
def deleteDiscount(req, did):
    pass


class EditEventOrganizer(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/auth/login/"
    permission_required = "event.edit_event"

    def get(self, req):
        pass

    def post(self, req):
        pass


def deleteEventFromAttender(req, eid):
    # todo get user data from authentication
    pass


def applyDiscount(req, eid):
    # todo get discount data from req
    pass


def searchByTitle(req):
    pass
