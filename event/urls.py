from django.urls import path
from . import views
urlpatterns = [
    path("", views.viewAllEvents, name="event_index"),
    
    path("organizer/add/", views.AddEventOrganizer.as_view(), name="organizer_add_event"),
    path("organizer/", views.organizerEvents),
    path("organizer/<int:oid>/", views.viewOrganizerEventsById),
    path("organizer/discount/add/", views.AddDiscount.as_view(), name="organizer_add_discount"),
    path("organizer/discount/delete/<int:did>/", views.deleteDiscount),
    path("organizer/edit/<int:eid>/", views.EditEventOrganizer.as_view()),
    
    path("attender/", views.attenderEvents),
    path("attender/delete/<int:eid>/", views.deleteEventFromAttender),
    path("discount/apply/<int:eid>/", views.applyDiscount),
    path("<int:eid>/", views.viewEvent),

    path("search/", views.searchByTitle)
]