from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Participant(User):

    def __str__(self):
        return self.participant_id.username

    class Meta:
        db_table = "participants"


class Event(models.Model):
    event_id = models.AutoField(primary_key=True, verbose_name='event_id')
    event_type = models.CharField(max_length=200)
    event_description = models.CharField(max_length=200)
    participants = models.ManyToManyField(Participant, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.event_type

    class Meta:
        db_table = "event"


class Organizer(models.Model):
    organizer = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, default=0)
    event = models.ManyToManyField(Event, blank=True)

    def __str__(self):
        return self.organizer_id.username

    class Meta:
        db_table = "organizer"


class Administrator(models.Model):
    admin = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, default=0)
    event = models.ManyToManyField(Event, blank=True)

    def __str__(self):
        return self.admin_id.username

    class Meta:
        db_table = "administrator"
