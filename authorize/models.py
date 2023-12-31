from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from dateutil.parser import parse

class OrganizerUser(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    phone   = models.TextField(max_length=100)

    def getDisplayName(self):
        return self.user.first_name + " " + self.user.last_name


class AttenderUser(models.Model):
    user     = models.OneToOneField(User, on_delete=models.CASCADE)
    phone    = models.TextField(max_length=100)
    multiple = models.BooleanField(default=False)


class EmailConfirmation(models.Model):
    code        = models.TextField(max_length=100)
    expires_on  = models.DateTimeField()
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def is_valid(self):
        if type(self.expires_on) == type(""):
            expires_on = parse(self.expires_on)
            return timezone.now() < expires_on
        return timezone.now() < self.expires_on
