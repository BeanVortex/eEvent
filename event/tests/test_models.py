from django.test import TestCase
from authorize.models import OrganizerUser, AttenderUser
from event.models import Event, Attendance, Discount
from datetime import  timedelta
from django.utils import timezone
from django.contrib.auth.models import User

class EventModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.orgUser = OrganizerUser.objects.create(user=self.user)
        self.event = Event.events.create(title="Test Event", description="Test Description", location="Test Location", price=100, starts_on=timezone.now() + timedelta(days=1), capacity=10, organizer_user=self.orgUser)

    def test_event_is_valid(self):
        self.assertTrue(self.event.is_valid())

class AttendanceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.orgUser = OrganizerUser.objects.create(user=self.user)
        self.attUser = AttenderUser.objects.create(user=self.user)
        self.event = Event.events.create(title="Test Event", description="Test Description", location="Test Location", price=100, starts_on=timezone.now() + timedelta(days=1), capacity=10, organizer_user=self.orgUser)
        self.attendance = Attendance.objects.create(attender_user=self.attUser, event=self.event, paid=True)

    def test_attendance_paid(self):
        self.assertTrue(self.attendance.paid)

class DiscountModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.orgUser = OrganizerUser.objects.create(user=self.user)
        self.event = Event.events.create(title="Test Event", description="Test Description", location="Test Location", price=100, starts_on=timezone.now() + timedelta(days=1), capacity=10, organizer_user=self.orgUser)
        self.discount = Discount.discounts.create(title="Test Discount", code="TEST", percentage=10, valid_until=timezone.now() + timedelta(days=2), rate_limit=5, rate=0, event=self.event, organizer_user=self.orgUser)

    def test_discount_is_valid(self):
        self.assertTrue(self.discount.is_valid())
