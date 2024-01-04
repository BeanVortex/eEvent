from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from authorize.models import OrganizerUser
from event.models import *
from datetime import  timedelta
from django.utils import timezone

class AddEventOrganizerTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user.user_permissions.add(Permission.objects.get(codename='add_event'))
        self.orgUser = OrganizerUser.objects.create(user=self.user)

    def test_add_event_organizer(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('organizer_add_event'), {
            'title': 'New Event',
            'description': 'New Description',
            'location': 'New Location',
            'price': 200,
            'start_date': (timezone.now() + timedelta(days=1)).date(),
            'start_time': (timezone.now() + timedelta(days=1)).time(),
            'capacity': 10
        })
        self.assertEqual(response.status_code, 302)  # Check redirect
        self.assertEqual(Event.events.count(), 1)  # Check that one event was created
        self.assertEqual(Event.events.get().title, 'New Event')  # Check that the event has the correct title

class OrganizerEventsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.orgUser = OrganizerUser.objects.create(user=self.user)
        self.event1 = Event.events.create(title="Test Event 1", description="Test Description 1", location="Test Location 1", price=100, starts_on=timezone.now() + timedelta(days=1), capacity=10, organizer_user=self.orgUser)
        self.event2 = Event.events.create(title="Test Event 2", description="Test Description 2", location="Test Location 2", price=200, starts_on=timezone.now() + timedelta(days=2), capacity=20, organizer_user=self.orgUser)

    def test_organizer_events(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('organizer_events'))
        self.assertEqual(response.status_code, 200)  # Check that the response is OK
        self.assertContains(response, 'Test Event 1')  # Check that the first event is in the response
        self.assertContains(response, 'Test Event 2')  # Check that the second event is in the response

class EditEventOrganizerTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user.user_permissions.add(Permission.objects.get(codename='change_event'))
        self.orgUser = OrganizerUser.objects.create(user=self.user)
        self.event = Event.events.create(title="Test Event", description="Test Description", location="Test Location", price=100, starts_on=timezone.now() + timedelta(days=1), capacity=10, organizer_user=self.orgUser)

    def test_edit_event_organizer(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('organizer_edit_discount', kwargs={'eid': self.event.id}), {
            'title': 'Updated Event',
            'description': 'Updated Description',
            'location': 'Updated Location',
            'price': 200,
            'start_date': (timezone.now() + timedelta(days=2)).date(),
            'start_time': (timezone.now() + timedelta(days=2)).time(),
            'capacity': 20
        })
        self.assertEqual(response.status_code, 302)  # Check redirect
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, 'Updated Event')  # Check that the event title was updated


class AddDiscountTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user.user_permissions.add(Permission.objects.get(codename='add_discount'))
        self.orgUser = OrganizerUser.objects.create(user=self.user)
        self.event = Event.events.create(title="Test Event", description="Test Description", location="Test Location", price=100, starts_on=timezone.now() + timedelta(days=1), capacity=10, organizer_user=self.orgUser)

    def test_add_discount(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('organizer_add_discount'), {
            'title': 'New Discount',
            'code': 'NEW',
            'percentage': 10,
            'rate_limit': 5,
            'end_date': (timezone.now() + timedelta(days=2)).date(),
            'end_time': (timezone.now() + timedelta(days=2)).time(),
            'event': self.event.id
        })
        response2 = self.client.post(reverse('organizer_add_discount'), {
            'title': 'New Discount2',
            'code': 'NEW2',
            'percentage': 10,
            'rate_limit': 5,
            'end_date': (timezone.now() + timedelta(days=2)).date(),
            'end_time': (timezone.now() + timedelta(days=2)).time(),
            'event': self.event.id
        })
        self.assertEqual(response.status_code, 302)  # Check redirect
        self.assertEqual(response2.status_code, 302)  # Check redirect
        self.assertEqual(Discount.discounts.count(), 2)  # Check that one discount was created
        self.assertEqual(Discount.discounts.all()[0].title, 'New Discount')  # Check that the discount has the correct title
        self.assertEqual(Discount.discounts.all()[1].title, 'New Discount2')  # Check that the discount2 has the correct title
