import datetime

from django.contrib.auth.models import User
from django.db.models import ProtectedError
from django.test import TestCase
from rest_framework.test import APIClient

from events.models import Room, Event, Space


class ModelsTestCase(TestCase):
    def setUp(self):
        """
        Setting up needed resources
        """
        self.today = datetime.datetime.now().date()

    def test_create_models(self):
        """
        Test to create an instance (row) of all models
        """
        room = Room.objects.create(
            capacity=200,
            name='Room 1'
        )
        event = Event.objects.create(
            date=self.today,
            room=room,
            is_public=True
        )
        Space.objects.create(
            capacity=200,
            event=event
        )

    def test_save_models(self):
        """
        Test to update all models
        """
        rooms = Room.objects.all()
        if not rooms:
            self.test_create_models()
            rooms = Room.objects.all()
        room = rooms.first()
        event = Event.objects.all().first()
        space = Space.objects.all().first()

        room.name = 'room 01'
        room.save()

        event.date = self.today + datetime.timedelta(days=1)
        event.save()

        space.capacity = 50
        space.save()

    def test_delete_models(self):
        """
        Test to delete all models
        """
        rooms = Room.objects.all()
        if not rooms:
            self.test_create_models()
            rooms = Room.objects.all()
        room = rooms.first()
        event = Event.objects.all().first()
        space = Space.objects.all().first()

        space.delete()
        event.delete()
        room.delete()


class APITestCase(TestCase):
    room_id = None
    space_id = None
    event_id = None

    def setUp(self):
        """
        Setting up needed resources
        """
        self.today = datetime.datetime.now().date().isoformat()
        self.client = APIClient()
        # creating customer user
        User.objects.create_user(
            username='customer', password='7h8j9k0l'
        )
        # creating business user
        User.objects.create_superuser(
            username='business', password='7h8j9k0l'
        )
    
    def test_post_rooms(self):
        """
        Test correct response for POST in rooms endpoint only for
        business users
        """
        body = {
            'capacity': 500,
            'name': 'room 01'
        }
        # testing without logging in
        response = self.client.post('/api/rooms/', body)
        self.assertEqual(response.status_code, 403)
        # testing logging in as customer
        self.client.login(username='customer', password='7h8j9k0l')
        response = self.client.post('/api/rooms/', body)
        self.assertEqual(response.status_code, 403)
        # testing logging in as admin
        self.client.login(username='business', password='7h8j9k0l')
        response = self.client.post('/api/rooms/', body)
        self.assertEqual(response.status_code, 201)
        self.room_id = response.data['id']
        self.client.logout()

    def test_patch_rooms(self):
        """
        Test correct response for PATCH in rooms endpoint only for
        business users
        """
        if not self.room_id:
            self.test_post_rooms()
        body = {
            'name': 'room 1'
        }
        pk = self.room_id
        # testing without logging in
        response = self.client.patch(f'/api/rooms/{pk}/', body)
        self.assertEqual(response.status_code, 403)
        # testing logging in as customer
        self.client.login(username='customer', password='7h8j9k0l')
        response = self.client.patch(f'/api/rooms/{pk}/', body)
        self.assertEqual(response.status_code, 403)
        # testing logging in as admin
        self.client.login(username='business', password='7h8j9k0l')
        response = self.client.patch(f'/api/rooms/{pk}/', body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'room 1')
        self.client.logout()
    
    def test_get_rooms(self):
        """
        Test correct response for GET in rooms endpoint only for
        business users
        """
        # testing without logging in
        response = self.client.get('/api/rooms/')
        self.assertEqual(response.status_code, 403)
        # testing logging in as customer
        self.client.login(username='customer', password='7h8j9k0l')
        response = self.client.get('/api/rooms/')
        self.assertEqual(response.status_code, 403)
        # testing logging in as admin
        self.client.login(username='business', password='7h8j9k0l')
        response = self.client.get('/api/rooms/')
        self.assertEqual(response.status_code, 200)
        self.client.logout()
    
    def test_delete_rooms_wo_event(self):
        """
        Test correct response for DELETE in rooms endpoint for a room
        without event
        """
        if not self.room_id:
            self.test_post_rooms()
        pk = self.room_id
        # testing without logging in
        response = self.client.delete(f'/api/rooms/{pk}/')
        self.assertEqual(response.status_code, 403)
        # testing logging in as customer
        self.client.login(username='customer', password='7h8j9k0l')
        response = self.client.delete(f'/api/rooms/{pk}/')
        self.assertEqual(response.status_code, 403)
        # testing logging in as admin
        self.client.login(username='business', password='7h8j9k0l')
        response = self.client.delete(f'/api/rooms/{pk}/')
        self.assertEqual(response.status_code, 204)
        self.room_id = None
        self.client.logout()
    
    def test_post_events(self):
        """
        Test correct response for POST in events endpoint only for
        business users
        """
        if not self.room_id:
            self.test_post_rooms()
        body = {
            'is_public': True,
            'room': self.room_id,
            'date': self.today
        }
        # testing without logging in
        response = self.client.post('/api/events/', body)
        self.assertEqual(response.status_code, 403)
        # testing logging in as customer
        self.client.login(username='customer', password='7h8j9k0l')
        response = self.client.post('/api/events/', body)
        self.assertEqual(response.status_code, 403)
        # testing logging in as admin
        self.client.login(username='business', password='7h8j9k0l')
        response = self.client.post('/api/events/', body)
        self.assertEqual(response.status_code, 201)
        self.event_id = response.data['id']
        self.client.logout()

    def test_patch_events(self):
        """
        Test correct response for PATCH in events endpoint only for
        business users
        """
        if not self.room_id:
            self.test_post_events()
        body = {
            'is_public': False
        }
        pk = self.event_id
        # testing without logging in
        response = self.client.patch(f'/api/events/{pk}/', body)
        self.assertEqual(response.status_code, 403)
        # testing logging in as customer
        self.client.login(username='customer', password='7h8j9k0l')
        response = self.client.patch(f'/api/events/{pk}/', body)
        self.assertEqual(response.status_code, 403)
        # testing logging in as admin
        self.client.login(username='business', password='7h8j9k0l')
        response = self.client.patch(f'/api/events/{pk}/', body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['is_public'], False)
        self.client.logout()
    
    def test_get_events_admin(self):
        """
        Test correct response for GET in events endpoint
        """
        # testing without logging in
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, 403)
        # testing logging in as customer
        self.client.login(username='business', password='7h8j9k0l')
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_get_events_customer(self):
        """
        Test correct response for GET in events endpoint as customer.
        Must show only public events
        """
        # testing without logging in
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, 403)
        # testing logging in as customer
        self.client.login(username='customer', password='7h8j9k0l')
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, 200)
        for r in response.data:
            self.assertTrue(r['is_public'])
        self.client.logout()
    
    def test_delete_events_wo_spaces(self):
        """
        Test correct response for DELETE in events endpoint for an event
        without spaces
        """
        if not self.event_id:
            self.test_post_events()
        pk = self.event_id
        # testing without logging in
        response = self.client.delete(f'/api/events/{pk}/')
        self.assertEqual(response.status_code, 403)
        # testing logging in as customer
        self.client.login(username='customer', password='7h8j9k0l')
        response = self.client.delete(f'/api/events/{pk}/')
        self.assertEqual(response.status_code, 403)
        # testing logging in as admin
        self.client.login(username='business', password='7h8j9k0l')
        response = self.client.delete(f'/api/events/{pk}/')
        self.assertEqual(response.status_code, 204)
        self.event_id = None
        self.client.logout()
    
    def test_post_spaces(self):
        """
        Test correct response for POST in spaces endpoint
        """
        if not self.event_id:
            self.test_post_events()
        body = {
            'capacity': 100,
            'event': self.event_id,
        }
        # testing without logging in
        response = self.client.post('/api/spaces/', body)
        self.assertEqual(response.status_code, 403)
        # testing logging in as customer
        self.client.login(username='customer', password='7h8j9k0l')
        response = self.client.post('/api/spaces/', body)
        self.assertEqual(response.status_code, 201)
        self.space_id = response.data['id']
        self.client.logout()

    def test_get_spaces(self):
        """
        Test correct response for GET in spaces endpoint
        """
        # testing without logging in
        response = self.client.get('/api/spaces/')
        self.assertEqual(response.status_code, 403)
        # testing logging in as customer
        self.client.login(username='customer', password='7h8j9k0l')
        response = self.client.get('/api/spaces/')
        self.assertEqual(response.status_code, 200)
        self.client.logout()
    
    def test_cancel_space(self):
        """
        Test correct response for DELETE in spaces endpoint, it shouldn't be
        deleted but cancelled
        """
        if not self.space_id:
            self.test_post_spaces()
        pk = self.space_id
        # testing without logging in
        response = self.client.delete(f'/api/spaces/{pk}/')
        self.assertEqual(response.status_code, 403)
        # testing logging in as customer
        self.client.login(username='customer', password='7h8j9k0l')
        response = self.client.delete(f'/api/spaces/{pk}/')
        self.assertEqual(response.status_code, 200)
        self.space_id = None
        self.assertEqual(response.data['is_active'], False)
        self.client.logout()

    def test_cant_delete_room_with_events(self):
        """
        Testing trying to delete a room with events in DB
        """
        self.test_post_events()
        pk = self.room_id
        exception = None
        # testing logging in as admin
        self.client.login(username='business', password='7h8j9k0l')
        try:
            response = self.client.delete(f'/api/rooms/{pk}/')
        except Exception as e:
            exception = e
        self.assertIsInstance(exception, ProtectedError)
        self.client.logout()
