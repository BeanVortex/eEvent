
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from event.views import viewAllEvents, organizerEvents, viewOrganizerDiscounts

class TestUrls(SimpleTestCase):
    def test_if_urls_are_resolved(self):
        viewAllEventsUrl = reverse("event_index")
        organizerEventsUrl = reverse("organizer_events")
        viewOrganizerDiscountsUrl = reverse("organizer_discounts")

        self.assertEqual(resolve(viewAllEventsUrl).func, viewAllEvents)
        self.assertEqual(resolve(organizerEventsUrl).func, organizerEvents)
        self.assertEqual(resolve(viewOrganizerDiscountsUrl).func, viewOrganizerDiscounts)
