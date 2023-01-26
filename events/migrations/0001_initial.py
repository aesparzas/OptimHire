# Generated by Django 4.1.5 on 2023-01-26 00:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_public', models.BooleanField(verbose_name='is the event public?')),
                ('date', models.DateField(verbose_name='date')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacity', models.IntegerField(verbose_name='capacity')),
                ('name', models.CharField(blank=True, max_length=24, null=True, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacity', models.IntegerField(verbose_name='capacity')),
                ('is_active', models.BooleanField(verbose_name='is active? if not it is cancelled')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event', verbose_name='event')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.room', verbose_name='room'),
        ),
    ]