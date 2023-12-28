from django.shortcuts import render
from event.models import Event

def index(req):
    events = Event.objects.all().values()
    return render(req, "event/event_list.html", {"events": events})