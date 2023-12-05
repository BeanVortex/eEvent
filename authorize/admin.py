from django.contrib import admin
from .models import AttenderUser, OrganizerUser
# Register your models here.

admin.site.register(AttenderUser)
admin.site.register(OrganizerUser)