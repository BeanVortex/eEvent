from django.db import models
from authorize.models import OrganizerUser, AttenderUser
# Create your models here.

class Event(models.Model):
    location        = models.TextField(max_length=200)
    price           = models.DecimalField(decimal_places=2, max_digits=20)
    start_date      = models.DateTimeField()
    valid_until     = models.DateTimeField()
    capacity        = models.IntegerField()
    organizer_user  = models.ForeignKey(OrganizerUser, on_delete=models.CASCADE)
    attender_users  = models.ManyToManyField(AttenderUser, blank=True)


class Discount(models.Model):
    code           = models.TextField(max_length=10)
    percentage     = models.DecimalField(decimal_places=2, max_digits=2)
    valid_until    = models.DateTimeField()
    rate_limit     = models.IntegerField()
    event          = models.ForeignKey(Event, on_delete=models.CASCADE)
    organizer_user = models.ForeignKey(OrganizerUser, on_delete=models.CASCADE)
 