from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class OrganizerUser(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    phone   = models.TextField(max_length=100)

    def getDisplayName(self):
        return self.user.first_name + " " + self.user.last_name


class AttenderUser(models.Model):
    user     = models.OneToOneField(User, on_delete=models.CASCADE)
    phone    = models.TextField(max_length=100)
    multiple = models.BooleanField(default=False)
