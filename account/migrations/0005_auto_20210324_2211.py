# Generated by Django 3.1.4 on 2021-03-24 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20210324_1221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='is_deleted',
        ),
        migrations.AlterField(
            model_name='request',
            name='requestType',
            field=models.CharField(choices=[('Join Event', 'Join Event'), ('Organizer Promotion', 'Organizer Promotion'), ('Admin Promotion', 'Admin Promotion')], default='Join Event', max_length=30, null=True),
        ),
    ]