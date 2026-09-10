from urllib.parse import urlencode

from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthenticationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = 'household-test-password-42'
        cls.member = get_user_model().objects.create_user(
            username='household_member',
            password=cls.password,
        )

    def test_household_pages_require_login(self):
        for name in ['core:home', 'core:history', 'core:categories']:
            with self.subTest(page=name):
                url = reverse(name)
                response = self.client.get(url)
                expected = reverse('login') + '?' + urlencode({'next': url})
                self.assertRedirects(response, expected)

    def test_login_returns_member_to_requested_page(self):
        destination = reverse('core:history')
        login_page = self.client.get(reverse('login'), {'next': destination})
        self.assertEqual(login_page.status_code, 200)
        self.assertContains(login_page, f'name="next" value="{destination}"')

        response = self.client.post(reverse('login'), {
            'username': self.member.username,
            'password': self.password,
            'next': destination,
        })

        self.assertRedirects(response, destination)
        self.assertEqual(self.client.session[SESSION_KEY], str(self.member.pk))
        self.assertContains(self.client.get(destination), 'Completed chores')

    def test_post_logout_ends_access_to_household_pages(self):
        self.client.force_login(self.member)
        self.assertEqual(self.client.get(reverse('core:home')).status_code, 200)

        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('login'))
        self.assertNotIn(SESSION_KEY, self.client.session)
        for name in ['core:home', 'core:history', 'core:categories']:
            with self.subTest(page=name):
                url = reverse(name)
                expected = reverse('login') + '?' + urlencode({'next': url})
                self.assertRedirects(self.client.get(url), expected)
