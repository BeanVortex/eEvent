from django.db import models
from authorize.models import OrganizerUser, AttenderUser
# Create your models here.

class Event(models.Model):
    title           = models.TextField(max_length=100)
    description     = models.TextField()
    location        = models.TextField(max_length=200)
    price           = models.DecimalField(decimal_places=2, max_digits=20)
    starts_on       = models.DateTimeField()
    capacity        = models.IntegerField()
    organizer_user  = models.ForeignKey(OrganizerUser, on_delete=models.CASCADE)
    attender_users  = models.ManyToManyField(AttenderUser, blank=True)
    
    def __str__(self):
        return self.title
    


class Discount(models.Model):
    title           = models.TextField(max_length=100)
    code           = models.TextField(max_length=10, unique=True)
    percentage     = models.IntegerField()
    valid_until    = models.DateTimeField()
    rate_limit     = models.IntegerField()
    event          = models.ForeignKey(Event, on_delete=models.CASCADE)
    
 