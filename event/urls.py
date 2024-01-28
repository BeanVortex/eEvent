from django.urls import path
from . import views
urlpatterns = [
    path("", views.viewAllEvents, name="event_index"),
    
    path("organizer/add/", views.AddEventOrganizer.as_view(), name="organizer_add_event"),
    path("organizer/", views.organizerEvents, name="organizer_events"),
    path("organizer/sells/", views.organizerSells, name="organizer_sells"),
    path("organizer/delete/<int:eid>/", views.deleteOrganizerEvent),
    path("organizer/<int:oid>/", views.viewOrganizerEventsById),
    path("organizer/discounts/", views.viewOrganizerDiscounts, name="organizer_discounts"),
    path("organizer/discount/delete/<int:did>/", views.deleteOrganizerDiscount),
    path("organizer/discount/edit/<int:did>/", views.EditDiscountOrganizer.as_view()),
    path("organizer/discount/add/", views.AddDiscount.as_view(), name="organizer_add_discount"),
    path("organizer/edit/<int:eid>/", views.EditEventOrganizer.as_view(), name="organizer_edit_discount"),
    
    path("attender/", views.AttenderEvents.as_view(), name="attender_events"),
    path("attender/<int:eid>/", views.AttenderEvents.as_view(), name="attender_events_post"),
    path("attender/pay/<int:eid>/", views.AttenderPayEvents.as_view()),
    path("<int:eid>/", views.viewEvent),
    path("switch/", views.switch, name="switch"),

    path("search/", views.searchByTitle, name="search")
]
