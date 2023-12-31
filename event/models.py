from django.utils import timezone
from django.db import models
from authorize.models import OrganizerUser, AttenderUser
from .managers import EventManager, DiscountManager
# Create your models here.


class Event(models.Model):
    title = models.TextField(max_length=100)
    description = models.TextField()
    location = models.TextField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    starts_on = models.DateTimeField()
    capacity = models.IntegerField()
    organizer_user = models.ForeignKey(OrganizerUser, on_delete=models.CASCADE)
    attender_users = models.ManyToManyField(AttenderUser, through='Attendance', related_name="events", blank=True)

    events = EventManager()

    def __str__(self):
        return self.title

    def is_valid(self):
        return timezone.now() < self.starts_on


class Attendance(models.Model):
    attender_user = models.ForeignKey(AttenderUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)


class Discount(models.Model):
    title = models.TextField(max_length=100)
    code = models.TextField(max_length=10, unique=True)
    percentage = models.IntegerField()
    valid_until = models.DateTimeField()
    rate_limit = models.IntegerField()
    rate = models.IntegerField(default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    organizer_user = models.ForeignKey(OrganizerUser, on_delete=models.CASCADE)

    discounts = DiscountManager()

    def is_valid(self):
        return timezone.now() < self.valid_until and self.rate < self.rate_limit
