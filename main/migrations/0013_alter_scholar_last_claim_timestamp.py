# Generated by Django 3.2.5 on 2021-07-30 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20210731_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholar',
            name='last_claim_timestamp',
            field=models.DateTimeField(null=True),
        ),
    ]
