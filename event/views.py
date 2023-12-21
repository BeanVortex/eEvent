from django.shortcuts import render, HttpResponse
from django.views import View

def index(req):
    return HttpResponse("Event index")


class AddEventOrganizer(View):
    def get(self, req):
        pass
    def post(self, req):
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

def deleteDiscount(req, eid):
    # todo get discount data from req
    pass

def viewEvent(req, eid):
    pass

def viewAllEvents(req):
    pass