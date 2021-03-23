from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    comment = models.CharField(max_length=45, blank=True, null=True)


class Event(models.Model):
    event_type = models.CharField(max_length=200)

    participants = models.ManyToManyField(User, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    upvotes = models.IntegerField(default=0, blank=True, null=True)
    comment = models.ManyToManyField(Comment, blank=True)

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.event_type


class Organizer(models.Model):
    organizer = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, default=0)
    event = models.ManyToManyField(Event, blank=True)
    promotion_date = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.organizer_id.username


class Administrator(models.Model):
    admin = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, default=0)
    event = models.ManyToManyField(Event, blank=True)

    def __str__(self):
        return self.admin_id.username


class Requests(models.Model):
    REQUEST_TYPE = (
        ('Join Event', 'Join Event'),
        ('Promote to Organizer', 'Promote to Organizer'),
        ('Promote to Admin', 'Promote to Admin'),
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
