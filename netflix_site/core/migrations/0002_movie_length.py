# Generated by Django 5.0.4 on 2024-05-14 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='length',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
