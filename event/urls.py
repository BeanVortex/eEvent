from django.urls import path
from . import views
urlpatterns = [
    path("event/index", views.index, name="event_index"),
    path("event/organizer/add/", views.AddEventOrganizer.as_view()),
    path("event/organizer/edit/<int:eid>/", views.EditEventOrganizer.as_view()),
    path("event/organizer/delete/<int:eid>/", views.deleteEventOrganizer),
    path("event/attender/add/<int:eid>/", views.addEventAttender),
    path("event/attender/delete/<int:eid>/", views.deleteEventFromAttender),
    path("event/discount/apply/<int:eid>/", views.applyDiscount),
    path("event/discount/delete/<int:eid>/", views.deleteDiscount),
    path("event/<int:eid>/", views.viewEvent),
    path("event/all/", views.viewAllEvents),
]