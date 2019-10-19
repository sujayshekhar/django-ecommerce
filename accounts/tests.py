# -*- coding: utf-8 -*-

from django.urls import reverse
from django.urls import resolve
from django.test import TestCase
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User
from accounts.views import register_request

# Create your tests here.


class register_tests(TestCase):
    def setUp(self):
        url = reverse('accounts:register')
        self.response = self.client.get(url)

    def test_register_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_register_url_resolves_register_view(self):
        view = resolve('/fr/inscription/')
        self.assertEquals(view.func, register_request)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, UserCreationForm)
