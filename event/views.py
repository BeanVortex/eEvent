from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from authorize.models import OrganizerUser, AttenderUser
from .models import Event, Discount, Attendance
from .forms import DiscountForm, EventForm
from datetime import datetime
from django.utils import timezone
import logging

log = logging.getLogger(__name__)

class AddEventOrganizer(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/auth/login"
    permission_required = "event.add_event"

    def get(self, req):
        form = EventForm()
        return render(req, "event/event_save.html", {"form": form})

    def post(self, req):
        form = EventForm(req.POST)
        try:
            if form.is_valid():
                title = form.cleaned_data["title"]
                description = form.cleaned_data["description"]
                location = form.cleaned_data["location"]
                price = form.cleaned_data["price"]
                start_date = form.cleaned_data["start_date"]
                start_time = form.cleaned_data["start_time"]
                starts_on = timezone.make_aware(datetime.combine(start_date, start_time))
                capacity = form.cleaned_data["capacity"]
                if capacity <= 0:
                    raise Exception("Capacity cannot be 0 or less")
                if price < 0:
                    raise Exception("Price cannot be less than 0")
                if timezone.now() > starts_on:
                    raise Exception("Date and time cannot be set in the past")
                orgId = req.user.id
                orgUser = OrganizerUser.objects.get(user_id=orgId)
                event = Event(title=title, description=description, location=location, price=price,
                              starts_on=starts_on, capacity=capacity, organizer_user=orgUser)
                event.save()
                log.info(f"Saved event: {event.id}")
            return redirect("event_index")
        except Exception as e:
            log.error(str(e))
            return render(req, "event/event_save.html", {"form": form, "status":"fail", "message": str(e)})



class EditEventOrganizer(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/auth/login/"
    permission_required = "event.change_event"

    def get(self, req, **kwargs):
        event = Event.events.getById(kwargs["eid"])
        initial_data = {
            "title": event.title,
            "description": event.description,
            "location": event.location,
            "price": event.price,
            "start_date": event.starts_on.date,
            "start_time": event.starts_on.time,
            "capacity": event.capacity}
        form = EventForm(initial=initial_data)
        return render(req, "event/event_save.html", {"form": form})

    def post(self, req, **kwargs):
        form = EventForm(req.POST)
        try:
            if form.is_valid():
                event = Event.events.getById(kwargs["eid"])
                event.title = form.cleaned_data["title"]
                event.description = form.cleaned_data["description"]
                event.location = form.cleaned_data["location"]
                event.price = form.cleaned_data["price"]
                start_date = form.cleaned_data["start_date"]
                start_time = form.cleaned_data["start_time"]
                starts_on = timezone.make_aware(datetime.combine(start_date, start_time))
                event.starts_on = starts_on
                event.capacity = form.cleaned_data["capacity"]
                if event.capacity <= 0:
                    raise Exception("Capacity cannot be 0 or less")
                if event.price < 0:
                    raise Exception("Price cannot be less than 0")
                if timezone.now() > starts_on:
                    raise Exception("Date and time cannot be set in the past")
                event.save()
                log.info(f"Successfully updated event {event.id}")
                return redirect("event_index")
        except Exception as e:
            log.error(str(e))
            return render(req, "event/event_save.html", {"form": form, "status":"fail", "message": str(e)})


@login_required(login_url="/auth/login")
def organizerEvents(req):
    organizer = get_object_or_404(OrganizerUser, user_id=req.user.id)
    events = Event.events.getAllByOrganizer(organizer)
    return render(req, "event/event_list.html", {"events": events, "organizer_name": organizer.getDisplayName()})


@login_required(login_url="/auth/login")
@permission_required(perm="event.delete_event")
def deleteOrganizerEvent(req, eid):
    try:
        organizer = get_object_or_404(OrganizerUser, user_id=req.user.id)
        event = Event.events.getByOrganizerAndId(organizer,eid)
        event.delete()
        events = Event.events.all()
        return render(req, "event/event_list.html", {"events": events, "organizer_name": organizer.getDisplayName()})
    except Exception as e:
        log.error(str(e))
        return redirect("index")


def viewOrganizerEventsById(req, oid):
    organizer = OrganizerUser.objects.get(id=oid)
    events = Event.events.getAllByOrganizer(organizer)
    return render(req, "event/event_list.html", {"events": events, "organizer_name": organizer.getDisplayName()})


@login_required(login_url="/auth/login/")
@permission_required(perm="event.view_discount")
def viewOrganizerDiscounts(req):
    organizer = get_object_or_404(OrganizerUser, user_id=req.user.id)
    discounts = Discount.discounts.getAllByOrganizer(organizer)
    return render(req, "event/discount_list.html", {"discounts": discounts, "organizer_name": organizer.getDisplayName()})


@login_required(login_url="/auth/login/")
@permission_required(perm="event.delete_discount")
def deleteOrganizerDiscount(req, did):
    try:
        organizer = get_object_or_404(OrganizerUser, user_id=req.user.id)
        discount = Discount.discounts.getByOrganizerAndId(organizer, did)
        discount.delete()
        discounts = Discount.discounts.getAllByOrganizer(organizer)
        log.info(f"Deleted discount: {discount.id}")
        return render(req, "event/discount_list.html", {"discounts": discounts, "organizer_name": organizer.getDisplayName()})
    except Exception as e:
        log.error(str(e))
        return redirect("index")
    

class EditDiscountOrganizer(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/auth/login/"
    permission_required = "event.change_discount"

    def get(self, req, **kwargs):
        discount = Discount.discounts.getById(kwargs["did"])
        initial_data = {
            "title": discount.title,
            "code": discount.code,
            "percentage": discount.percentage,
            "end_date": discount.valid_until.date,
            "end_time": discount.valid_until.time,
            "rate_limit": discount.rate_limit,
            "event": discount.event}
        form = DiscountForm(initial=initial_data)
        return render(req, "event/discount_save.html", {"form": form})

    def post(self, req, **kwargs):
        form = DiscountForm(req.POST)
        try:
            if form.is_valid():
                discount = Discount.discounts.getById(kwargs["did"])
                discount.title = form.cleaned_data["title"]
                discount.code = form.cleaned_data["code"]
                discount.percentage = form.cleaned_data["percentage"]
                end_date = form.cleaned_data["end_date"]
                end_time = form.cleaned_data["end_time"]
                valid_until = timezone.make_aware(datetime.combine(end_date, end_time))
                if timezone.now() > valid_until:
                    raise Exception("Date and time cannot be set in the past")
                discount.valid_until = valid_until
                event = int(form.cleaned_data["event"])
                if not event == discount.event.id:
                    raise Exception("You can't change the event")
                rate_limit = form.cleaned_data["rate_limit"]
                if rate_limit <= 0:
                    raise Exception("Rate limit cannot be 0 or less")
                if discount.rate > rate_limit:
                    raise Exception(f"You can't decrease rate limit, rate/rate limit !~ {discount.rate}/{rate_limit} ")
                discount.rate_limit = rate_limit
                discount.save()
                log.info(f"Discount updated: {discount.id}")
        except Exception as e:
            log.error(str(e))
            return render(req, 'event/discount_save.html', {'form': form, "status": "fail", "message": str(e)})
        return redirect("organizer_discounts")




class AddDiscount(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/auth/login/"
    permission_required = "event.add_discount"

    def get(self, req):
        form = DiscountForm()
        return render(req, 'event/discount_save.html', {'form': form})

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
                valid_until = timezone.make_aware(datetime.combine(end_date, end_time))

                if rate_limit <= 0:
                    raise Exception("Rate limit cannot be 0 or less")
                if timezone.now() > valid_until:
                    raise Exception("Date and time cannot be set in the past")
                eventId = form.cleaned_data["event"]
                event = Event.events.getById(eventId)
                organizer_user = OrganizerUser.objects.get(user_id=req.user.id)
                discount = Discount(title=title, code=code, percentage=percentage, valid_until=valid_until,
                                    rate_limit=rate_limit, organizer_user=organizer_user, event=event)
                discount.save()
                log.info(f"Discount saved: {discount.id}")
                return redirect("organizer_discounts")
            else:
                log.warning(f"Form is invalid: {discount.id}")
                return render(req, 'event/discount_save.html', {'form': form, "status": "fail", "message": "sent data is invalid"})
        except Exception as e:
            log.warning(str(e))
            return render(req, 'event/discount_save.html', {'form': form, "status": "fail", "message": str(e)})


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
        attender_user = get_object_or_404(AttenderUser, user_id=req.user.id)
        attender_user.events.remove(event)
        events = attender_user.events.all()
        log.info(f"Removed event {event.title} from attender user {attender_user.id}")
        return render(req, "event/event_list.html", {"events": events, "user_id": req.user.id})


class AttenderPayEvents(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/auth/login/"
    permission_required = "event.view_event"

    def get(self, req, **kwargs):
        event = Event.events.getById(kwargs['eid'])
        return render(req, "event/event_pay.html", {"event": event, "user_id": req.user.id})

    def post(self, req, **kwargs):
        message = ""
        try:
            event = Event.events.getById(kwargs['eid'])
            discount_code = req.POST["discount_code"]
            new_price = event.price
            attender_user = get_object_or_404(AttenderUser, user_id=req.user.id)
            countOfAttenders = Attendance.objects.filter(event_id=event.id).count()
            if countOfAttenders >= event.capacity:
                raise Exception(f"This event is full {countOfAttenders}/{event.capacity}")
            if not event.is_valid():
                raise Exception(f"This event has expired {event.starts_on}")
            
            attendance = Attendance.objects.filter(attender_user_id=attender_user.id, event_id=event.id)
            if attendance:
                raise Exception("You have already attended in this event")

            if discount_code:
                discount = Discount.discounts.getByCode(discount_code)
                if discount:
                    if discount.event == event:
                        if not discount.is_valid():
                            raise Exception(f"Code is invalid. rate: {discount.rate}/{discount.rate_limit} expiration: {discount.valid_until}")
                        percentage = discount.percentage
                        percentage_val = (event.price * percentage) / 100
                        new_price = event.price - percentage_val
                        discount.rate = discount.rate + 1
                        discount.save()
                        log.info(f"Applying discount {discount.id} on event {event.id} with user {attender_user.id}")
                    else:
                        message = "Code is invalid for this event"

            attendance = Attendance(paid=True, attender_user_id=attender_user.id, event_id=event.id)
            attendance.save()
            log.info(f"User {attender_user.id} attended in event {event.id}")
            return render(req, "event/event_pay.html", {"event": event, "user_id": req.user.id, "status": "success", "new_price": new_price})

        except Exception as e:
            message = str(e)

        log.error(message)
        return render(req, "event/event_pay.html", {"event": event, "user_id": req.user.id, "status": "fail", "message": message})


def viewEvent(req, eid):
    event = Event.events.getById(eid)
    if req.method == "POST" and req.user.is_authenticated:
        try:
            attender_user = get_object_or_404(AttenderUser, user_id=req.user.id)
            if attender_user.events.filter(id=eid).exists():
                raise Exception("You have already attended in this event")
            attender_user.events.add(event)
            log.info(f"Attender user {attender_user.id} successfully attended in {event.id}")
            return render(req, "event/event_details.html", {"event": event, "status": "success"})
        except Exception as e:
            log.error(str(e))
            return render(req, "event/event_details.html", {"event": event, "status": "fail", "message": str(e)})

    return render(req, "event/event_details.html", {"event": event})


def viewAllEvents(req):
    events = Event.events.all()
    return render(req, "event/event_list.html", {"events": events})


def searchByTitle(req):
    if req.method == "POST":
        title = req.POST['title_search']
        events = Event.events.allTitleContains(title)
        return render(req, "event/event_list.html", {"events": events})
