from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Room(models.Model):
    capacity = models.IntegerField('capacity')
    name = models.CharField('name', max_length=24, null=True, blank=True)

    def __str__(self):
        return self.name or self.pk


class Event(models.Model):
    room = models.ForeignKey(
        Room, verbose_name='room', on_delete=models.PROTECT
    )
    is_public = models.BooleanField('is the event public?')
    date = models.DateField('date')

    def __str__(self):
        public = 'Public' if self.is_public else 'Private'
        return f'{public} event in {self.date} for {self.room}'

    @property
    def available_space(self):
        capacity = self.room.capacity
        occupied = self.space_set.filter(is_active=True).aggregate(
            Sum('capacity'))['capacity__sum'] or 0
        return capacity - occupied

    class Meta:
        unique_together = ['room', 'date']


class Space(models.Model):
    capacity = models.IntegerField('capacity')
    is_active = models.BooleanField(
        'is active? if not it is cancelled', default=True
    )
    event = models.ForeignKey(
        Event, verbose_name='event', on_delete=models.CASCADE
    )
