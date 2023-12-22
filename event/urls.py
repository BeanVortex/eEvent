from django.urls import path
from . import views
urlpatterns = [
    path("index", views.index, name="event_index"),
    path("organizer/add/", views.AddEventOrganizer.as_view()),
    path("organizer/events/", views.organizerEvents),
    path("organizer/<int:orgId>/event/<int:eid>/", views.viewEventAsOrganizer),
    path("organizer/discount/add/<int:eid>/", views.addDiscount),
    path("organizer/discount/delete/<int:did>/", views.deleteDiscount),
    path("organizer/edit/<int:eid>/", views.EditEventOrganizer.as_view()),
    path("organizer/delete/<int:eid>/", views.deleteEventOrganizer),

    path("attender/add/<int:eid>/", views.addEventAttender),
    path("attender/delete/<int:eid>/", views.deleteEventFromAttender),
    path("discount/apply/<int:eid>/", views.applyDiscount),
    path("<int:eid>/", views.viewEvent),

    path("search/", views.searchByTitle),
    path("all/", views.viewAllEvents)
]