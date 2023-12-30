from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from authorize.models import OrganizerUser, AttenderUser
from .models import Event, Discount, Attendance
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


class AttenderEvents(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/auth/login/"
    permission_required = "event.view_event"

    def get(self, req, **kwargs):
        if 'eid' in kwargs:
            return redirect("attender_events")
        attender_user = get_object_or_404(AttenderUser, user_id=req.user.id)
        events = attender_user.events.all()
        return render(req, "event/event_list.html", {"events": events, "user_id": req.user.id})

    def post(self, req, **kwargs):
        event = get_object_or_404(Event, id=kwargs['eid'])
        attender_user = get_object_or_404(
            AttenderUser, user_id=req.user.id)
        attender_user.events.remove(event)
        events = attender_user.events.all()
        return render(req, "event/event_list.html", {"events": events, "user_id": req.user.id})


class AttenderPayEvents(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/auth/login/"
    permission_required = "event.view_event"

    def get(self, req, **kwargs):
        event = Event.objects.get(id=kwargs['eid'])
        return render(req, "event/event_pay.html", {"event": event, "user_id": req.user.id})

    def post(self, req, **kwargs):
        message = ""
        try:
            event = Event.objects.get(id=kwargs['eid'])
            discount_code = req.POST["discount_code"]
            new_price = event.price
            attender_user = get_object_or_404(AttenderUser, user_id=req.user.id)
            countOfAttenders = Attendance.objects.filter(event_id=event.id).count()
            if countOfAttenders >= event.capacity:
                raise Exception(f"This event is full {countOfAttenders}/{event.capacity}")
            if event.is_valid():
                raise Exception(f"This event has expired {event.starts_on}")
            if discount_code:
                discount = Discount.objects.get(code=discount_code)
                if discount.event == event:
                    if not discount.is_valid():
                        raise Exception(f"Code is invalid. rate: {discount.rate}/{discount.rate_limit} expiration: {discount.valid_until}")
                    percentage = discount.percentage
                    percentage_val = (event.price * percentage) / 100
                    new_price = event.price - percentage_val
                    discount.rate = discount.rate + 1
                    discount.save() 
                else:
                    message = "Code is invalid for this event"

            else:
                attendance = Attendance.objects.filter(attender_user_id=attender_user.id, event_id=event.id)
                if attendance:
                    raise Exception("You have already attended in this event")
            attendance = Attendance(paid=True, attender_user_id=attender_user.id, event_id=event.id)
            attendance.save()
            return render(req, "event/event_pay.html", {"event": event, "user_id": req.user.id, "status": "success", "new_price": new_price})
        except Exception as e:
            message = str(e)
        return render(req, "event/event_pay.html", {"event": event, "user_id": req.user.id, "status": "fail", "message": message})


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
