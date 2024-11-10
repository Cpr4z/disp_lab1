from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Person


class PersonTestCase(APITestCase):
    def setUp(self):
        """Создание начальной записи"""
        self.person = Person.objects.create(
            name = 'John Smith',
            age = 18,
            address = '123 Main Street',
            work = 'Engineer'
        )
        self.base_url = reverse('person-list')

    def test_get_person_list(self):
        """Тестирование получения списка всех персон (GET api/v1/persons/)"""
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 1)

    def test_get_person_by_id(self):
        """Тестирование получения person по его id (GET api/v1/persons/{id})"""
        url = reverse('person-detail', args=[self.person.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], self.person.name)
        self.assertEqual(response.json()['address'], self.person.address)
        self.assertEqual(response.json()['work'], self.person.work)
        self.assertEqual(response.json()['age'], self.person.age)

    def test_create_person(self):
        """Тестирование создания объекта person (POST api/v1/persons/)"""
        data = {
            'name': 'Tim Doe',
            'address': '123 New Street',
            'work': 'Doctor',
            'age': 30
        }
        response = self.client.post(self.base_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Person.objects.count(), 2)

    def test_update_person(self):
        """Тестирование обновления persons (PATCH api/v1/persons/{id}/)"""
        url = reverse('person-detail', args=[self.person.id])
        data = {'age': 45}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.person.refresh_from_db()
        self.assertEqual(self.person.age, 45)

    def test_delete_person(self):
        """Тестирование удаления persons (DELETE api/v1/persons/{id}/)"""
        url = reverse('person-detail', args=[self.person.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.count(), 0)