from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from django.test import TestCase


# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        self.userName = 'hello2'
        self.passWord = 'passwordTest'
        self.emailTest = 'hello@gmail.com'

    def test_created_successfully(self):
        res = self.client.post('/signup', data={
            'username': self.userName,
            'password': self.passWord,
            'email': self.emailTest
        })
        self.assertRedirects(res, '/signin', 302)
        users = get_user_model().objects.get(username=self.userName)
        self.assertNotEqual(users, ObjectDoesNotExist)

    def test_login_successfully(self):
        res = self.client.post('/signin', data={
            'username': self.userName,
            'password': self.passWord
        })
        self.assertEqual(res.status_code, 200)

    def test_logout_successfully(self):
        res = self.client.get('/signout')
        self.assertRedirects(res, '/home', 302)
