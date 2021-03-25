from django.contrib import admin
from .models import Event, Organizer, Request

# Register your models here.

admin.site.register(Event)
admin.site.register(Organizer)
admin.site.register(Request)
