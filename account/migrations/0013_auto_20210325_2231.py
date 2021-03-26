# Generated by Django 3.1.7 on 2021-03-25 14:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20210325_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 3, 25, 14, 31, 12, 442864, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 3, 25, 14, 31, 12, 442864, tzinfo=utc), null=True),
        ),
        migrations.DeleteModel(
            name='Administrator',
        ),
    ]