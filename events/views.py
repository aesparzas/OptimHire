from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from events.models import Room, Event, Space
from events.serializers import RoomModelSerializer, EventModelSerializer, \
    SpaceModelSerializer


class RoomViewSet(viewsets.ModelViewSet):
    """
    ViewSet with GET, POST, PATCH and DELETE mothods for each room
    Only available to business users (admin users)
    """

    queryset = Room.objects.all()
    serializer_class = RoomModelSerializer
    permission_classes = [permissions.IsAdminUser]


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet with GET, POST, PATCH and DELETE mothods for each event
    Only available to business users (admin users)
    When list is consumed, it can show all the public events if the user
    is not an admin (customer)
    """

    queryset = Event.objects.all()
    serializer_class = EventModelSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def list(self, request, *args, **kwargs):
        if not request.user and request.user.is_staff:
            qs = Event.objects.filter(is_public=True)
        else:
            qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class SpaceViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Space ViewSet to be accesed by customers to create a space (booking) or
    cancel it.
    List amd Retrieve methods can be requested just by Admin users
    """
    serializer_class = SpaceModelSerializer
    queryset = Space.objects.all()

    def get_permissions(self):
        if self.request.method == 'get':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def destroy(self, request, pk=None):
        obj = get_object_or_404(self.get_queryset(), pk=pk)
        obj.is_active = False
        obj.save()
        return Response(self.get_serializer(obj).data)
