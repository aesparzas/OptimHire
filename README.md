# OptimHire Project
API in django REST framework
### Rules:
- There are N rooms with M capacity.
- There are two types of events: public and private.
- If the event is public, any customer can book a space.
- If the event is private, no one else can book a space in the room.
- A customer can book a space for an event, if the event is public and there is still space
available.
- A customer can cancel its booking and their space should be available again.
- A customer cannot book a space twice for the same event.
### Requirements:
- The business can create a room with M capacity
- The business can create events for every room.
- The business can delete a room if said room does not have any events.
- A customer can book a place for an event.
- A customer can cancel its booking for an event.
- A customer can see all the available public events.
### Considerations:
- For now, there is only one event per day.
- Each room has a different capacity.
- Think of each requirement as an endpoint for the API (a Django view).
### How you’ll be evaluated in order of importance:
- Does the project run, work and meet the requirements?
- How well structured and high quality is your code?
- Can you talk through your approach?
### Extra points:
- Throw in a couple of tests.
## Solution
### Running the project
To run the project create a virtual environment (venv suggested) and install the requirements in `requirements.txt`

`python venv venv`

`venv/bin/activate`

`pip install -r requirements.txt`

`python manage.py migrate`

`python manage.py runserver`

### Endpoints
- [POST] '/api/rooms/' just for business users
- [GET] '/api/rooms/' just for business users
- [GET] '/api/rooms/{pk}/' just for business users
- [PATCH] '/api/rooms/{pk}/' just for business users
- [DELETE] '/api/rooms/{pk}/' just for business users
- [POST] '/api/events/' just for business users
- [GET] '/api/events/'
- [GET] '/api/events/{pk}/'
- [PATCH] '/api/events/{pk}/' just for business users
- [DELETE] '/api/events/{pk}/' just for business users
- [POST] '/api/spaces/'
- [GET] '/api/spaces/'
- [GET] '/api/spaces/{pk}/'
- [DELETE] '/api/spaces/{pk}/'
### Considerations
The project considers staff users as business users and non-staff regular users
as customers. So to properly test the API, both of the users are needed.

### Testing the project
This project has unit test using Django and Django REST Framework utilities. To run the tests:

`python manage.py test`