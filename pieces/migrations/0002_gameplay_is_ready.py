# Generated by Django 4.2.14 on 2024-08-08 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pieces', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameplay',
            name='is_ready',
            field=models.BooleanField(default=False),
        ),
    ]
