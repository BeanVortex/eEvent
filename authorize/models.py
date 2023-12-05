from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class OrganizerUser(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    phone   = models.TextField(max_length=100)


class AttenderUser(models.Model):
    user     = models.OneToOneField(User, on_delete=models.CASCADE)
    phone    = models.TextField(max_length=100)
    multiple = models.BooleanField(default=False)
