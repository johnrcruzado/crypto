# Generated by Django 3.2.5 on 2021-07-30 10:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_scholar_last_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholar',
            name='last_update',
            field=models.DateField(default=datetime.datetime(2021, 7, 30, 18, 29, 5, 122689)),
        ),
    ]
