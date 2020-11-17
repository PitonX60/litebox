from unittest import TestCase
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status as http_status
from autofixture import AutoFixture
from autofixture.generators import UUIDGenerator, EmailGenerator

from online_store.models import Shop

User = get_user_model()


class BaseTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        if self.client is not None:
            self.client.logout()
        cache.clear()
        super().tearDown()

    def authentication(self):
        self.token = Token()

        self.token.user = User.objects.create(
            username=f'User{UUIDGenerator().generate()}',
            first_name=f'Пользователь {UUIDGenerator().generate()}',
            password=make_password('1234'),
            is_superuser=False,
            is_active=True
        )
        self.token.save()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertTrue(User.objects.all().exists())


class TestShopView(BaseTest):
    def setUp(self):
        super().setUp()
        self.authentication()

    def test_get(self):
        url = reverse('api:shops')
        response = self.client.get(url, format='json')

        response_data = response.json()
        self.assertEquals(response.status_code, http_status.HTTP_200_OK)
        self.assertEqual(len(response_data.get('data')), response_data.get('total'))

    def test_post(self):
        url = reverse('api:shops')
        name = f'Магазин_{UUIDGenerator().generate()}'

        response = self.client.post(url, data={'name': name}, format='json')

        response_data = response.json()
        self.assertEquals(response.status_code, http_status.HTTP_201_CREATED)
        self.assertIn('data', response_data)
        self.assertIn('name', response_data.get('data'))
        self.assertEquals(response_data.get('data').get('name'), name)

    def test_put(self):
        name_old = f'Магазин_{UUIDGenerator().generate()}'
        name_new = f'Обновленный {name_old}'

        shop = AutoFixture(Shop, field_values={
            'name': name_old
        }).create_one()

        url = reverse('api:single_shops', kwargs={'pk': shop.pk})

        response = self.client.put(url, data={'name': name_new}, format='json')

        shop = Shop.objects.get(pk=shop.pk)

        response_data = response.json()
        self.assertEquals(response.status_code, http_status.HTTP_200_OK)
        self.assertEquals(response_data.get('data').get('name'), name_new)
        self.assertEquals(shop.name, name_new)

    def test_delete(self):
        shop = AutoFixture(Shop, field_values={
            'name': f'Магазин_{UUIDGenerator().generate()}'
        }).create_one()

        url = reverse('api:single_shops', kwargs={'pk': shop.pk})

        response = self.client.delete(url)
        self.assertEquals(response.status_code, http_status.HTTP_204_NO_CONTENT)
        self.assertFalse(Shop.objects.filter(pk=shop.pk).exists())
