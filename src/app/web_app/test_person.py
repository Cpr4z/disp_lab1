import os
import json
import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "person_service.settings")
django.setup()

from django.test.client import RequestFactory
from views import web_app


@pytest.mark.django_db
def test_get_all_persons():
    fact = RequestFactory()
    request = fact.get('api/v1/persons/')
    response = web_app(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_existing_person_by_id():
    fact = RequestFactory()
    pers_data = {'name': 'pers1',
                 'age': 22,
                 'address': 'address1',
                 'work': 'work1'}
    request = fact.post('/api/v1/persons/', data=pers_data, content_type='application/json')
    response = web_app(request)
    location = response.headers['Location']
    pers_id = int(location[location.rfind('/') + 1:])
    request = fact.get('api/v1/persons/')
    response = web_app(request, pers_id)
    assert response.status_code == 200

    request = fact.delete('/api/v1/persons/')
    web_app(request, pers_id)


@pytest.mark.django_db
def test_get_not_existing_person_by_id():
    fact = RequestFactory()
    request = fact.get('api/v1/persons/')
    response = web_app(request, -1)
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_person_positive():
    fact = RequestFactory()
    pers_data = {'name': 'pers1',
                 'age': 22,
                 'address': 'address1',
                 'work': 'work1'}
    request = fact.post('/api/v1/persons/', data=pers_data, content_type='application/json')
    response = web_app(request)
    assert response.status_code == 201

    location = response.headers['Location']
    pers_id = int(location[location.rfind('/') + 1:])
    request = fact.delete('api/v1/persons/', pers_id)
    web_app(request, pers_id)


@pytest.mark.django_db
def test_post_person_invalid_data():
    fact = RequestFactory()
    pers_data = {'first_name': 'pers1'}
    request = fact.post('/api/v1/persons/', data=pers_data, content_type='application/json')
    response = web_app(request)
    assert response.status_code == 400


@pytest.mark.django_db
def delete_existing_person():
    fact = RequestFactory()
    pers_data = {'name': 'pers1',
                 'age': 22,
                 'address': 'address1',
                 'work': 'work1'}
    request = fact.post('/api/v1/persons/', data=pers_data, content_type='application/json')
    response = web_app(request)

    location = response.headers['Location']
    pers_id = int(location[location.rfind('/') + 1:])
    request = fact.delete('/api/v1/persons/')
    response = web_app(request, pers_id)
    assert response.status_code == 204


@pytest.mark.django_db
def delete_not_existing_person():
    fact = RequestFactory()
    request = fact.delete('/api/v1/persons/')
    response = web_app(request, -1)
    assert response.status_code == 204