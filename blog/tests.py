from django.test import TestCase, Client


class BlogTest(TestCase):
    def test_blog_index(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(200, response.status_code)
