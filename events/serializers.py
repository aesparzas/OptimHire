from rest_framework import serializers

from events.models import Room, Event, Space


class RoomModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class EventModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class SpaceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = '__all__'

    def validate_capacity(self, val):
        """
        Check if the capacity of the event is greater or equals the capacity
        of the space (booking)
        :param val: Value to be validated
        :raises: ValidationError if the value does not match the conditions
        :return: Validated value
        """
        event = Event.objects.get(pk=self.initial_data['event'])
        if val > event.available_space:
            raise serializers.ValidationError(
                "Space capacity cannot be greater than event's available space"
            )
        return val
