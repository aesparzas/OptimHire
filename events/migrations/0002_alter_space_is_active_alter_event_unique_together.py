# Generated by Django 4.1.5 on 2023-01-26 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='space',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active? if not it is cancelled'),
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together={('room', 'date')},
        ),
    ]
