from django.shortcuts import render, HttpResponse
from django.views import View
from .models import Event, Discount

def index(req):
    return HttpResponse("Event index")


class AddEventOrganizer(View):
    def get(self, req):
        pass
    def post(self, req):
        pass

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