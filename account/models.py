from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Create your models here.


class Comment(models.Model):
    comment = models.CharField(max_length=45, blank=True, null=True)


class Event(models.Model):
    event_type = models.CharField(max_length=200)

    participants = models.ManyToManyField(User, blank=True)
    start_date = models.DateField(
        default=timezone.now(), blank=True, null=True)
    end_date = models.DateField(default=timezone.now(), blank=True, null=True)

    upvotes = models.IntegerField(default=0, blank=True, null=True)
    comment = models.ManyToManyField(Comment, blank=True)

    def __str__(self):
        return self.event_type


class Request(models.Model):
    REQUEST_TYPE = (
        ('Join Event', 'Join Event'),
        ('Organizer Request', 'Organizer Request'),
    )
    REQUEST_STATUS = (
        ('Reviewing', 'Reviewing'),
        ('Accept', 'Accept'),
        ('Decline', 'Decline'),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="+")
    requestType = models.CharField(
        max_length=30, null=True, choices=REQUEST_TYPE, default="Join Event")
    event = models.ForeignKey(
        Event, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")

    status = models.CharField(max_length=30, null=True,
                              choices=REQUEST_STATUS, default="Reviewing")
    date_requested = models.DateTimeField(auto_now_add=True, blank=True)
    date_replied = models.DateTimeField(blank=True, null=True)
    replied_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")

    def __str__(self):
        return self.requestType + " - " + str(self.id)


class Organizer(models.Model):
    organizer = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, default=0)
    event = models.ManyToManyField(Event, blank=True)
    promotion_date = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.organizer_id.username


# class Administrator(models.Model):
#     admin = models.OneToOneField(
#         User, on_delete=models.CASCADE, primary_key=True, default=0)
#     event = models.ManyToManyField(Event, blank=True)

#     def __str__(self):
#         return self.admin_id.username
